#!/usr/bin/env python3
"""
Top-level CLI: detect → scan → build. One-shot entry point.

Usage:
    python3 regenerate.py <workspace_root> \\
        [--output-dir x_temp] \\
        [--force-mode create|update]  # default: auto-detect

Auto-detection rules (delegated to detect_existing.py):
1. If <workspace>/x_temp/SOURCE_MAP.md AND <workspace>/x_temp/source_map.json exist → update
2. If <workspace>/SOURCE_MAP.md AND <workspace>/source_map.json exist → update
3. Otherwise → create
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DETECT = SCRIPT_DIR / "detect_existing.py"
SCAN = SCRIPT_DIR / "scan_workspace.py"
BUILD = SCRIPT_DIR / "build_source_map.py"


def run(cmd, **kw):
    """Run a subprocess and return CompletedProcess. Raise on non-zero."""
    return subprocess.run(cmd, check=True, **kw)


def main():
    p = argparse.ArgumentParser(description="Detect → scan → build source map (one-shot)")
    p.add_argument("workspace_root", help="Root directory to index")
    p.add_argument("--output-dir", default="x_temp", help="Where to write outputs (default: x_temp)")
    p.add_argument("--force-mode", choices=["create", "update"], help="Override auto-detection")
    p.add_argument("--exclude", default="", help="Comma-separated additional names to exclude")
    p.add_argument("--keep-prev-inventory", action="store_true",
                   help="In update mode, keep the previous inventory.json for diff display")
    args = p.parse_args()

    workspace = os.path.abspath(args.workspace_root)
    if not os.path.isdir(workspace):
        print(f"Workspace not found: {workspace}", file=sys.stderr)
        sys.exit(2)

    output_dir = os.path.join(workspace, args.output_dir)
    os.makedirs(output_dir, exist_ok=True)
    md_out = os.path.join(output_dir, "SOURCE_MAP.md")
    json_out = os.path.join(output_dir, "source_map.json")
    curated_out = os.path.join(output_dir, "curated_summaries.json")
    inventory_out = os.path.join(output_dir, "file_inventory.jsonl")
    prev_inventory = os.path.join(output_dir, "file_inventory.prev.jsonl")

    # 1) Detect (exit 0 = found, exit 1 = not found — both are normal)
    result = subprocess.run(
        [sys.executable, str(DETECT), workspace],
        capture_output=True, text=True,
    )
    if result.returncode not in (0, 1):
        print(f"detect_existing.py failed (rc={result.returncode}): {result.stderr}", file=sys.stderr)
        sys.exit(2)
    detect = json.loads(result.stdout)
    mode = args.force_mode or detect["mode"]
    print(f"[regenerate] mode = {mode} (detected: {detect['mode']})", file=sys.stderr)

    # 2) In update mode, save previous inventory (for diff)
    if mode == "update" and os.path.exists(json_out) and args.keep_prev_inventory:
        try:
            old_inv = json.loads(Path(json_out).read_text(encoding="utf-8"))
            if "files" in old_inv:
                Path(prev_inventory).write_text(
                    json.dumps({"files": old_inv["files"], "totals": old_inv.get("totals", {})}, ensure_ascii=False, indent=2),
                    encoding="utf-8"
                )
        except Exception:
            pass

    # 3) Scan
    scan_cmd = [
        sys.executable, str(SCAN), workspace,
        "--output", inventory_out,
    ]
    if args.exclude:
        scan_cmd += ["--exclude", args.exclude]
    run(scan_cmd, capture_output=True)

    # 4) Build
    build_cmd = [
        sys.executable, str(BUILD),
        "--inventory", inventory_out,
        "--md-out", md_out,
        "--json-out", json_out,
        "--curated-out", curated_out,
        "--mode", mode,
    ]
    if mode == "update" and os.path.exists(prev_inventory):
        build_cmd += ["--prev-inventory", prev_inventory]
    if mode == "update" and os.path.exists(curated_out):
        build_cmd += ["--existing-curated", curated_out]
    run(build_cmd)

    print(f"\n[regenerate] DONE. Mode: {mode}", file=sys.stderr)
    print(f"  Markdown : {md_out}", file=sys.stderr)
    print(f"  JSON     : {json_out}", file=sys.stderr)
    print(f"  Curated  : {curated_out}", file=sys.stderr)
    sys.exit(0)


if __name__ == "__main__":
    main()
