#!/usr/bin/env python3
"""minimax-web-search: call the upstream minimax-coding-plan-mcp's web_search tool.

This is the entry point invoked by the Codex ``minimax-web-search`` skill
(via ``exec_command``). It:

1. Resolves the MiniMax API key (from env or ~/.codex config files).
2. Spawns ``uvx minimax-coding-plan-mcp`` and talks JSON-RPC.
3. Calls the ``web_search`` tool with the user's query.
4. Prints a one-screen summary (title, link, snippet) and writes the
   full raw response to ``/tmp/minimax-mcp/result-*.json`` for debugging.

Default result count: 15.

Usage:
    search.py "MiniMax-M3 release date"
    search.py "2026 AI 模型最新进展" --max 20
    search.py "test" --max 5 --print        # full JSON to stdout
    search.py "test" --timeout 120          # 2-minute timeout
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import sys
from pathlib import Path

# Allow running this script directly (``python3 scripts/search.py ...``)
# by ensuring the scripts/ dir is on sys.path so we can import siblings.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib_key import resolve  # type: ignore  # noqa: E402
from mcp_client import McpClient, McpError  # type: ignore  # noqa: E402

DEFAULT_MAX_RESULTS = 15
RESULT_DIR = Path(os.environ.get("MINIMAX_MCP_RESULT_DIR", "/tmp/minimax-mcp"))


def _save_result(tool: str, request: dict, response: dict) -> Path:
    """Write a JSON file for reproducibility / debugging."""
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    ts = _dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    existing = list(RESULT_DIR.glob(f"result-{ts}-*.json"))
    idx = len(existing)
    path = RESULT_DIR / f"result-{ts}-{idx:02d}.json"
    path.write_text(
        json.dumps(
            {"tool": tool, "request": request, "response": response, "ts": ts},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return path


def _find_json_object(text: str) -> str | None:
    """Find a balanced JSON object in `text`, handling nested braces + strings."""
    for i in range(len(text)):
        if text[i] != "{":
            continue
        depth = 0
        in_str = False
        escape = False
        for j in range(i, len(text)):
            c = text[j]
            if in_str:
                if escape:
                    escape = False
                elif c == "\\":
                    escape = True
                elif c == '"':
                    in_str = False
                continue
            if c == '"':
                in_str = True
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return text[i : j + 1]
    return None


def _parse_search_payload(text: str) -> dict | None:
    """Find the first JSON object that looks like a MiniMax search response."""
    if not text:
        return None
    text = text.strip()
    candidate = _find_json_object(text)
    if not candidate:
        return None
    try:
        obj = json.loads(candidate)
    except json.JSONDecodeError:
        return None
    if isinstance(obj, dict) and ("organic" in obj or "related_searches" in obj):
        return obj
    return None


def _summarize_search(parsed: dict, max_items: int) -> str:
    """Render the parsed payload as a one-screen numbered list."""
    lines: list[str] = []
    organic = parsed.get("organic") or []
    for i, item in enumerate(organic[:max_items], 1):
        title = item.get("title", "") or ""
        link = item.get("link", "") or ""
        snippet = (item.get("snippet", "") or "")[:140]
        lines.append(f"  {i}. {title}")
        if link:
            lines.append(f"     {link}")
        if snippet:
            lines.append(f"     {snippet}")
    if not lines:
        lines.append("  (no organic results)")
    related = parsed.get("related_searches") or []
    if related:
        lines.append("")
        lines.append(
            "  related: "
            + ", ".join(
                (r.get("query") or "") for r in related[:5] if isinstance(r, dict)
            )
        )
    base = parsed.get("base_resp") or {}
    if base:
        lines.append(
            f"  status: code={base.get('status_code')} "
            f"msg={base.get('status_msg')}"
        )
    return "\n".join(lines)


def _extract_text(result: dict) -> str:
    """Concat all text fields from an MCP tool result."""
    chunks: list[str] = []
    for item in result.get("content", []):
        if isinstance(item, dict) and item.get("type") == "text":
            chunks.append(item.get("text", ""))
    if chunks:
        return "\n".join(chunks)
    sc = result.get("structuredContent")
    if isinstance(sc, dict) and sc.get("type") == "text":
        return sc.get("text", "")
    return json.dumps(result, ensure_ascii=False)


def main() -> int:
    p = argparse.ArgumentParser(
        prog="minimax-web-search",
        description=(
            "Web search via the upstream minimax-coding-plan-mcp tool. "
            "Returns top organic results (default: 15)."
        ),
    )
    p.add_argument("query", help="Search query string")
    p.add_argument(
        "--max",
        type=int,
        default=DEFAULT_MAX_RESULTS,
        help=f"Max organic results to print (default: {DEFAULT_MAX_RESULTS})",
    )
    p.add_argument(
        "--timeout",
        type=float,
        default=60.0,
        help="Per-call timeout in seconds (default: 60)",
    )
    p.add_argument(
        "--print",
        action="store_true",
        help="Print full JSON-RPC response to stdout instead of summary",
    )
    args = p.parse_args()

    # 1. Resolve key
    api_key, api_host = resolve()
    env = {"MINIMAX_API_KEY": api_key, "MINIMAX_API_HOST": api_host}

    # 2. Call MCP web_search
    request_payload = {"query": args.query}
    try:
        with McpClient(env) as client:
            raw = client.call_tool(
                "web_search", request_payload, timeout_s=args.timeout
            )
    except McpError as e:
        print(f"minimax-web-search: {e}", file=sys.stderr)
        return 1

    # 3. Save raw response (always, for debugging)
    path = _save_result("web_search", request_payload, raw)

    # 4. Print
    if args.print:
        sys.stdout.write(json.dumps(raw, ensure_ascii=False, indent=2) + "\n")
        return 0

    text = _extract_text(raw)
    parsed = _parse_search_payload(text)
    if parsed is not None:
        n = len(parsed.get("organic") or [])
        print(f"[minimax-web-search] {n} results for: {args.query!r}")
        print(_summarize_search(parsed, max_items=args.max))
        print(f"\nfull JSON: {path}")
    else:
        # Couldn't parse — show first 800 chars
        print(f"[minimax-web-search] raw text (no JSON detected):")
        print(text[:800])
        print(f"\nfull result: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
