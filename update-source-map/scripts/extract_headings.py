#!/usr/bin/env python3
"""
Extract H2 and H3 heading lists from a single .md file.

Useful when an agent wants to quickly summarize one file without a full scan.
Returns JSON to stdout: {"path": "...", "h2_titles": [...], "h3_titles": [...], "h2_count": N, "h3_count": M}

Usage:
    python3 extract_headings.py <file.md>
"""
import json
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: extract_headings.py <file.md>", file=sys.stderr)
        sys.exit(2)
    path = Path(sys.argv[1])
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(2)
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        print(f"Read error: {e}", file=sys.stderr)
        sys.exit(2)
    h2, h3 = [], []
    for line in content.splitlines():
        s = line.lstrip()
        if s.startswith("## ") and not s.startswith("### "):
            h2.append(s[3:].strip())
        elif s.startswith("### ") and not s.startswith("#### "):
            h3.append(s[4:].strip())
    print(json.dumps({
        "path": str(path),
        "h2_titles": h2,
        "h3_titles": h3,
        "h2_count": len(h2),
        "h3_count": len(h3),
    }, ensure_ascii=False, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
