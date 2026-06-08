#!/usr/bin/env python3
"""
Detect whether a source map already exists in the workspace and where.

Exit code 0 = found, 1 = not found, 2 = error.
On stdout: JSON {"mode": "create"|"update", "md_path": "...", "json_path": "..."}

Standard detection order (per Codex-style x_temp preference):
1. x_temp/SOURCE_MAP.md + x_temp/source_map.json
2. SOURCE_MAP.md + source_map.json (workspace root)
3. .codex/source_map.json (rare)
"""
import json
import os
import sys
from pathlib import Path

# (md_path, json_path) detection candidates, in priority order
CANDIDATES = [
    ("x_temp/SOURCE_MAP.md", "x_temp/source_map.json"),
    ("SOURCE_MAP.md", "source_map.json"),
    (".codex/SOURCE_MAP.md", ".codex/source_map.json"),
]




# Force UTF-8 on stdout/stderr so non-ASCII paths / content never crash
# the parent process when this script is invoked via subprocess on
# Windows code pages like GBK / cp936.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass


def detect(workspace_root: str) -> dict:
    """Return detection result as a dict. Always succeeds (returns mode='create' if nothing found)."""
    root = Path(workspace_root).resolve()
    for md_rel, json_rel in CANDIDATES:
        md_path = root / md_rel
        json_path = root / json_rel
        if md_path.exists() and json_path.exists():
            return {
                "mode": "update",
                "md_path": str(md_path),
                "json_path": str(json_path),
                "found_at": str(md_path.parent),
            }
        if md_path.exists() or json_path.exists():
            # Partial — treat as update but warn
            return {
                "mode": "update",
                "md_path": str(md_path),
                "json_path": str(json_path),
                "found_at": str(md_path.parent),
                "partial": True,
            }
    return {
        "mode": "create",
        "md_path": str(root / CANDIDATES[0][0]),
        "json_path": str(root / CANDIDATES[0][1]),
        "found_at": None,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: detect_existing.py <workspace_root>", file=sys.stderr)
        sys.exit(2)
    workspace = sys.argv[1]
    if not os.path.isdir(workspace):
        print(f"Workspace not found: {workspace}", file=sys.stderr)
        sys.exit(2)
    result = detect(workspace)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["mode"] == "update" else 1)


if __name__ == "__main__":
    main()
