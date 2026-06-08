"""Resolve the MiniMax API key and host from env / config files.

Priority (highest first):
    1. ``$MINIMAX_API_KEY`` env var
    2. ``$MINIMAX_API_HOST`` env var (optional override)
    3. ``~/.codex/config.toml`` — any ``[model_providers.<X>]`` block,
       pick up ``experimental_bearer_token`` as the key and ``base_url``
       (with ``/v1`` stripped) as the host.
    4. ``~/.codex/switch_model/minimax/config.toml`` — same fields, for
       users who manage per-model config under ``switch_model/``.

This module is intentionally self-contained (stdlib only) so it can be
copied between skills without dragging in any package dependencies.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import Final

DEFAULT_API_HOST: Final = "https://api.minimax.io"

# Config locations, tried in order if env vars are not set.
_CONFIG_PATHS: Final = (
    Path.home() / ".codex" / "config.toml",
    Path.home() / ".codex" / "switch_model" / "minimax" / "config.toml",
)


def die(msg: str, code: int = 1) -> "None":
    print(f"minimax-skill: {msg}", file=sys.stderr)
    raise SystemExit(code)


def _read_kv(text: str, key: str) -> str | None:
    """Find ``key = "value"`` or ``key = 'value'`` anywhere in text."""
    km = re.search(rf'{key}\s*=\s*"([^"]+)"', text)
    if not km:
        km = re.search(rf"{key}\s*=\s*'([^']+)'", text)
    return km.group(1) if km else None


def _read_provider_block(text: str, provider_id: str) -> str | None:
    """Extract a [model_providers.<id>] block (greedy until next [...] header)."""
    pat = rf"\[model_providers\.{re.escape(provider_id)}\][^\[]*"
    m = re.search(pat, text)
    return m.group(0) if m else None


def _read_mcp_env_block(text: str) -> str | None:
    """Extract the first [mcp_servers.<X>.env] block, if any."""
    m = re.search(r"\[mcp_servers\.[^\]]+(?:\.env)?\][^\[]*", text)
    return m.group(0) if m else None


def _read_config_file(path: Path) -> dict[str, str]:
    """Return {'key': ..., 'host': ...} from one config file, or empty dict."""
    if not path.exists():
        return {}
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        print(f"minimax-skill: warning: cannot read {path}: {e}", file=sys.stderr)
        return {}

    out: dict[str, str] = {}

    # 1. [model_providers.minimax] block (canonical case for this skill)
    for provider_id in ("minimax", "MiniMax"):
        block = _read_provider_block(text, provider_id)
        if not block:
            continue
        if "key" not in out:
            v = _read_kv(block, "experimental_bearer_token")
            if v:
                out["key"] = v
        if "host" not in out:
            v = _read_kv(block, "base_url")
            if v:
                out["host"] = v
        if "key" in out and "host" in out:
            break

    # 2. Any other [model_providers.X] block (fallback)
    if "key" not in out:
        for m in re.finditer(r"\[model_providers\.[^\]]+\][^\[]*", text):
            block = m.group(0)
            v = _read_kv(block, "experimental_bearer_token")
            if v:
                out["key"] = v
                if "host" not in out:
                    h = _read_kv(block, "base_url")
                    if h:
                        out["host"] = h
                break

    # 3. [mcp_servers.X.env] block (legacy / explicit env)
    if "key" not in out:
        mcp_block = _read_mcp_env_block(text)
        if mcp_block:
            v = _read_kv(mcp_block, "MINIMAX_API_KEY")
            if v:
                out["key"] = v
            if "host" not in out:
                h = _read_kv(mcp_block, "MINIMAX_API_HOST")
                if h:
                    out["host"] = h

    return out


def resolve(
    env: dict[str, str] | None = None,
    config_paths: tuple[Path, ...] = _CONFIG_PATHS,
) -> tuple[str, str]:
    """Return ``(api_key, api_host)``.

    Raises ``SystemExit(1)`` if no key can be found.
    """
    env = env if env is not None else dict(os.environ)

    # 1-2. Env vars win
    key = env.get("MINIMAX_API_KEY", "").strip()
    host = env.get("MINIMAX_API_HOST", "").strip()

    # 3-4. Fall back to config files (try each, take the first hit)
    if not key or not host:
        for path in config_paths:
            cfg = _read_config_file(path)
            if not key and "key" in cfg:
                key = cfg["key"]
            if not host and "host" in cfg:
                host = cfg["host"]
            if key and host:
                break

    if not key:
        die(
            "MINIMAX_API_KEY not found. Tried:\n"
            "  - $MINIMAX_API_KEY env\n"
            + "\n".join(f"  - {p}" for p in config_paths)
            + "\nFix one of:\n"
            "  - export MINIMAX_API_KEY=sk-cp-...\n"
            "  - keep [model_providers.minimax].experimental_bearer_token "
            "in ~/.codex/config.toml\n"
            "  - keep [model_providers.minimax].experimental_bearer_token "
            "in ~/.codex/switch_model/minimax/config.toml"
        )

    # Normalize host: strip /v1 suffix, add https:// if missing
    host = host.rstrip("/")
    if host.endswith("/v1"):
        host = host[: -len("/v1")]
    if not host.startswith(("http://", "https://")):
        host = "https://" + host
    if not host:
        host = DEFAULT_API_HOST

    return key, host
