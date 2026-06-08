#!/usr/bin/env python3
"""minimax-image-understand: call upstream minimax-coding-plan-mcp's understand_image.

This is the entry point invoked by the Codex ``minimax-image-understand``
skill (via ``exec_command``). It:

1. Resolves the MiniMax API key (from env or ~/.codex config files).
2. Spawns ``uvx minimax-coding-plan-mcp`` and talks JSON-RPC.
3. Calls the ``understand_image`` tool with the user's prompt and image
   source (URL or local path; the MCP server handles base64 conversion).
4. Prints the model's description and writes the full raw response to
   ``/tmp/minimax-mcp/result-*.json`` for debugging.

Usage:
    image.py "Describe this image" "https://example.com/x.jpg"
    image.py "理解这张图" "/Users/me/Desktop/photo.png"
    image.py "OCR this" "https://..." --print      # full JSON to stdout
    image.py "..." "..." --timeout 120            # 2-minute timeout
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib_key import resolve  # type: ignore  # noqa: E402
from mcp_client import McpClient, McpError  # type: ignore  # noqa: E402

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
        prog="minimax-image-understand",
        description=(
            "Image understanding via the upstream minimax-coding-plan-mcp "
            "tool. Supports URLs and local file paths (JPEG, PNG, WebP)."
        ),
    )
    p.add_argument("prompt", help="What to analyze / describe")
    p.add_argument("source", help="Image URL or local file path")
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

    # 1. Validate image source (cheap check before spawning MCP)
    src = args.source
    if not src.startswith(("http://", "https://", "data:")):
        # Local file — verify it exists
        path = Path(src).expanduser()
        if not path.exists():
            print(
                f"minimax-image-understand: file not found: {path}",
                file=sys.stderr,
            )
            return 1
        # Verify format (JPEG/PNG/WebP only)
        ext = path.suffix.lower()
        if ext not in {".jpg", ".jpeg", ".png", ".webp"}:
            print(
                f"minimax-image-understand: unsupported format {ext!r} "
                f"(supported: .jpg .jpeg .png .webp)",
                file=sys.stderr,
            )
            return 1

    # 2. Resolve key
    api_key, api_host = resolve()
    env = {"MINIMAX_API_KEY": api_key, "MINIMAX_API_HOST": api_host}

    # 3. Call MCP understand_image
    request_payload = {"prompt": args.prompt, "image_source": src}
    try:
        with McpClient(env) as client:
            raw = client.call_tool(
                "understand_image", request_payload, timeout_s=args.timeout
            )
    except McpError as e:
        print(f"minimax-image-understand: {e}", file=sys.stderr)
        return 1

    # 4. Save raw response
    path = _save_result("understand_image", request_payload, raw)

    # 5. Print
    if args.print:
        sys.stdout.write(json.dumps(raw, ensure_ascii=False, indent=2) + "\n")
        return 0

    text = _extract_text(raw)
    print(f"[minimax-image-understand] prompt={args.prompt!r}")
    print(f"  source: {args.source}")
    print(f"  result: {text[:1500]}")
    print(f"\nfull JSON: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
