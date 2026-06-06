#!/usr/bin/env python3
"""
Scan a workspace and emit a file inventory with per-file metadata.

For .md files: extract H2/H3 heading skeletons + word/char/line counts.
For .pdf files: only metadata (binary, contents not parsed).
Other extensions: skipped by default.

Output: JSON to stdout, or to --output <path>.

Usage:
    python3 scan_workspace.py <workspace_root> [--output inventory.json] [--exclude "notes.assets,x_temp"]
"""
import argparse
import datetime
import json
import os
import sys
from pathlib import Path

DEFAULT_EXCLUDES = {".DS_Store", "node_modules", "__pycache__", ".git", ".venv", "venv", "dist", "build"}
DEFAULT_EXCLUDE_DIRS = {"notes.assets", "x_temp", "x_temp_*"}
DEFAULT_EXTS = {".md", ".pdf"}


def is_excluded_dir(name: str, custom_excludes: set) -> bool:
    if name in DEFAULT_EXCLUDE_DIRS:
        return True
    if name in custom_excludes:
        return True
    for pat in DEFAULT_EXCLUDE_DIRS:
        if "*" in pat and __import__("fnmatch").fnmatch(name, pat):
            return True
    return False


def extract_headings(content: str) -> dict:
    """Return H2 and H3 title lists + counts from a markdown string."""
    h2 = []
    h3 = []
    for line in content.splitlines():
        s = line.lstrip()
        if s.startswith("## ") and not s.startswith("### "):
            h2.append(s[3:].strip())
        elif s.startswith("### ") and not s.startswith("#### "):
            h3.append(s[4:].strip())
    return {"h2_titles": h2, "h3_titles": h3, "h2_count": len(h2), "h3_count": len(h3)}


def scan(workspace_root: str, extensions: set, custom_excludes: set) -> list:
    """Walk the workspace and return a list of file records."""
    inventory = []
    for dirpath, dirnames, filenames in os.walk(workspace_root):
        # Filter excluded dirs in-place
        dirnames[:] = [d for d in dirnames if not is_excluded_dir(d, custom_excludes)]
        for fname in sorted(filenames):
            if fname in DEFAULT_EXCLUDES:
                continue
            if fname in custom_excludes:
                continue
            ext = os.path.splitext(fname)[1].lower()
            if ext not in extensions:
                continue
            full = Path(dirpath) / fname
            try:
                rel = str(full.relative_to(workspace_root))
            except ValueError:
                rel = str(full)
            try:
                st = full.stat()
            except OSError as e:
                continue
            record = {
                "rel_path": rel,
                "filename": fname,
                "type": ext[1:].upper(),
                "size_bytes": st.st_size,
                "mtime": datetime.date.fromtimestamp(st.st_mtime).isoformat(),
                "folder": str(full.parent.relative_to(workspace_root)) if str(full.parent) != workspace_root else ".",
            }
            if ext == ".md":
                try:
                    content = full.read_text(encoding="utf-8", errors="replace")
                except Exception:
                    content = ""
                record["chars"] = len(content)
                record["words"] = len(content.split())
                record["lines"] = content.count("\n") + 1
                record.update(extract_headings(content))
            inventory.append(record)
    return inventory


def main():
    p = argparse.ArgumentParser(description="Scan a workspace and emit file inventory as JSON")
    p.add_argument("workspace_root", help="Root directory to scan")
    p.add_argument("--output", "-o", help="Write JSON to this path instead of stdout")
    p.add_argument("--exclude", "-e", default="", help="Comma-separated additional names to exclude")
    p.add_argument("--ext", default="md,pdf", help="Comma-separated extensions to include (default: md,pdf)")
    args = p.parse_args()
    if not os.path.isdir(args.workspace_root):
        print(f"Workspace not found: {args.workspace_root}", file=sys.stderr)
        sys.exit(2)
    exts = {"." + x.strip().lstrip(".").lower() for x in args.ext.split(",") if x.strip()}
    custom_excludes = {x.strip() for x in args.exclude.split(",") if x.strip()}
    inv = scan(args.workspace_root, exts, custom_excludes)
    payload = {
        "workspace_root": os.path.abspath(args.workspace_root),
        "scanned_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "files": inv,
        "totals": {
            "files_total": len(inv),
            "md_files": sum(1 for r in inv if r["type"] == "MD"),
            "pdf_files": sum(1 for r in inv if r["type"] == "PDF"),
        },
    }
    out = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"Wrote {args.output} ({len(inv)} files)", file=sys.stderr)
    else:
        print(out)
    sys.exit(0)


if __name__ == "__main__":
    main()
