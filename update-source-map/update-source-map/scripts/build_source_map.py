#!/usr/bin/env python3
"""
Build the agent-readable source map from a scan inventory.

Outputs:
  - <md_path>:    SOURCE_MAP.md (human + agent readable, primary deliverable)
  - <json_path>:  source_map.json (structured data, programmatic queries)
  - <curated>:    curated_summaries.json (hand-curated 1-line file summaries,
                  preserved across regenerations)

Curated summaries are KEY for quality: the auto-generated H2 skeleton is a
start, but the per-file one-line summaries tell an agent what each file
actually covers. In create mode the curated file is empty; the agent (or
user) is expected to add entries over time. In update mode, existing
entries are preserved and entries for deleted files are dropped.

Usage:
    python3 build_source_map.py \\
        --inventory inventory.json \\
        --md-out x_temp/SOURCE_MAP.md \\
        --json-out x_temp/source_map.json \\
        --curated-out x_temp/curated_summaries.json \\
        --existing-curated x_temp/curated_summaries.json  # optional, for update mode
"""
import argparse
import datetime
import json
import os
import sys
from pathlib import Path


# --- Section: size formatting ---
def sz(b):
    if b < 1024:
        return f"{b}B"
    if b < 1024 * 1024:
        return f"{b/1024:.1f}KB"
    return f"{b/1024/1024:.2f}MB"


# --- Section: tree rendering ---
def build_tree(inventory):
    """Build nested tree from flat rel_path list."""
    tree = {"_files": []}
    for r in inventory:
        parts = r["rel_path"].split(os.sep)
        cur = tree
        for p in parts[:-1]:
            cur = cur.setdefault(p, {"_files": []})
        cur["_files"].append(r)
    return tree


def render_tree_lines(node, prefix="", is_last=True, name=""):
    """Render a tree node as a list of ASCII lines."""
    out = []
    if name:
        connector = "└── " if is_last else "├── "
        file_count = len(node["_files"])
        sub_count = sum(1 for k, v in node.items() if k != "_files" and isinstance(v, dict))
        label = f"{name}/"
        if file_count and sub_count:
            label += f"  ({file_count} files, {sub_count} subdirs)"
        elif sub_count:
            label += f"  ({sub_count} subdirs)"
        elif file_count:
            label += f"  ({file_count} files)"
        out.append(f"{prefix}{connector}{label}")
        new_prefix = prefix + ("    " if is_last else "│   ")
    else:
        new_prefix = prefix

    subdirs = [(k, v) for k, v in node.items() if k != "_files" and isinstance(v, dict)]
    subdirs.sort(key=lambda x: x[0])
    for i, (k, v) in enumerate(subdirs):
        is_last_sub = (i == len(subdirs) - 1) and len(node["_files"]) == 0
        out.extend(render_tree_lines(v, new_prefix, is_last_sub, k))

    for f in sorted(node["_files"], key=lambda x: x["rel_path"]):
        is_last_file = (f is node["_files"][-1]) and len(subdirs) == 0
        connector = "└── " if is_last_file else "├── "
        marker = "📄" if f["type"] == "PDF" else "📝"
        size_str = sz(f["size_bytes"])
        if f["type"] == "MD":
            tail = f"({f.get('words', 0):,}w, {f.get('h2_count', 0)} H2)"
        else:
            tail = ""
        out.append(f"{new_prefix}{connector}{marker} {f['filename']}  {size_str}  {tail}")
    return out


# --- Section: top-level rollup (root files EXCLUDED — they're not folders) ---
def compute_top_rollups(inventory):
    """Return dict {folder_name: {md, pdf, size}} — only real folders, not root files."""
    rollups = {}
    for r in inventory:
        if r["rel_path"].startswith("x_temp"):
            continue
        parts = r["rel_path"].split(os.sep)
        if len(parts) == 1:
            # Root-level file — not a folder, skip
            continue
        top = parts[0]
        rollups.setdefault(top, {"md": 0, "pdf": 0, "size": 0})
        rollups[top][r["type"].lower()] += 1
        rollups[top]["size"] += r["size_bytes"]
    return rollups


# --- Section: Markdown assembly ---
def build_markdown(workspace_root, inventory, totals, curated, mode, prev_inventory=None):
    """Assemble the full SOURCE_MAP.md content as a list of lines."""
    md = []
    files_by_folder = {}
    for r in inventory:
        if r["rel_path"].startswith("x_temp"):
            continue
        folder = r["folder"] if r["folder"] != "." else "_root_"
        files_by_folder.setdefault(folder, []).append(r)
    for f in files_by_folder.values():
        f.sort(key=lambda x: x["rel_path"])

    # Diff summary (only in update mode)
    diff_block = ""
    if mode == "update" and prev_inventory:
        prev_paths = {r["rel_path"] for r in prev_inventory}
        cur_paths = {r["rel_path"] for r in inventory}
        added = sorted(cur_paths - prev_paths)
        removed = sorted(prev_paths - cur_paths)
        if added or removed:
            diff_block = "\n## 0. 增量变化（仅 update 模式）\n\n"
            if added:
                diff_block += f"**新增 {len(added)} 个文件**：\n\n"
                for p in added[:20]:
                    diff_block += f"- `{p}`\n"
                if len(added) > 20:
                    diff_block += f"- ... 还有 {len(added) - 20} 个\n"
                diff_block += "\n"
            if removed:
                diff_block += f"**删除 {len(removed)} 个文件**：\n\n"
                for p in removed[:20]:
                    diff_block += f"- `{p}`\n"
                if len(removed) > 20:
                    diff_block += f"- ... 还有 {len(removed) - 20} 个\n"
                diff_block += "\n"

    # Header
    md.append(f"# Source Map — `{os.path.basename(workspace_root.rstrip('/')) or 'workspace'}`")
    md.append("")
    md.append(f"> Generated: `{datetime.datetime.now().isoformat(timespec='seconds')}`  ")
    md.append(f"> Workspace: `{workspace_root}`  ")
    md.append(f"> Mode: **{mode.upper()}**  ")
    md.append(f"> Scope: **{totals['md_files']} .md** + **{totals['pdf_files']} .pdf** = **{totals['files_total']} files**  ")
    md.append(">")
    md.append("> Agent-readable project index. Not a substitute for the original files — use it to find what you need, then read the actual file.")
    md.append("")
    md.append(diff_block)

    # TL;DR
    md.append("---")
    md.append("")
    md.append("## TL;DR — 5 行读懂这个 workspace")
    md.append("")
    if mode == "create":
        md.append("- 这是**新建**的 source map（之前不存在）")
    else:
        md.append("- 这是**更新后**的 source map（之前已存在）")
    md.append(f"- 共 **{totals['files_total']} 个文件**（{totals['md_files']} .md + {totals['pdf_files']} .pdf）")
    md.append("- 下面的章节逐文件夹展开 + 全文件清单 + 交叉引用")
    md.append("- Agent 找内容：先看 TL;DR → 看文件夹章节 → 跳到对应 .md / .pdf")
    md.append("- 维护：编辑 `curated_summaries.json` 可手写每个文件的 1 行说明（跨更新保留）")
    md.append("")

    # Top-level rollup table
    md.append("---")
    md.append("")
    md.append("## 1. 顶层目录速览")
    md.append("")
    md.append("| 文件夹 | 大小 | MD 数 | PDF 数 |")
    md.append("|---|---|---|---|")
    rollups = compute_top_rollups(inventory)
    for fldr in sorted(rollups.keys()):
        info = rollups[fldr]
        md.append(f"| `{fldr}/` | {sz(info['size'])} | {info['md']} | {info['pdf']} |")
    md.append("")

    # Visual tree
    md.append("### 视觉化目录树（带大小）")
    md.append("")
    md.append("```text")
    tree = build_tree(inventory)
    tree_root = os.path.basename(workspace_root.rstrip("/")) or "workspace"
    md.extend(render_tree_lines(tree, "", True, tree_root + "/"))
    md.append("```")
    md.append("")

    # Per-folder detail
    md.append("---")
    md.append("")
    md.append("## 2. 逐文件夹深读")
    md.append("")
    for folder in sorted(files_by_folder.keys()):
        if folder == "_root_":
            md.append("### 2.X 项目根")
            md.append("")
            for r in files_by_folder[folder]:
                summary = curated.get(r["rel_path"], "")
                if summary:
                    md.append(f"- `{r['filename']}` — {summary}")
                else:
                    md.append(f"- `{r['filename']}`")
            md.append("")
        else:
            md.append(f"### 2.X `{folder}/`")
            md.append("")
            for r in files_by_folder[folder]:
                summary = curated.get(r["rel_path"], "(no curated summary)")
                if r["type"] == "MD":
                    md.append(f"- `{r['filename']}` — {r.get('words', 0):,} 词, {r.get('h2_count', 0)} H2 — {summary}")
                else:
                    md.append(f"- `{r['filename']}` ({sz(r['size_bytes'])}) — {summary}")
            md.append("")

    # Full file inventory
    md.append("---")
    md.append("")
    md.append("## 3. 完整文件清单")
    md.append("")
    md.append("### 3.1 所有 Markdown 笔记")
    md.append("")
    md.append("| 路径 | 词数 | H2 | H3 | 字数 | 修改时间 |")
    md.append("|---|---|---|---|---|---|")
    for r in sorted([f for f in inventory if f["type"] == "MD" and not f["rel_path"].startswith("x_temp")], key=lambda x: x["rel_path"]):
        md.append(f"| `{r['rel_path']}` | {r.get('words', 0):,} | {r.get('h2_count', 0)} | {r.get('h3_count', 0)} | {r.get('chars', 0):,} | {r['mtime']} |")
    md.append("")
    md.append("### 3.2 所有 PDF 文件")
    md.append("")
    md.append("| 路径 | 大小 | 修改时间 |")
    md.append("|---|---|---|")
    for r in sorted([f for f in inventory if f["type"] == "PDF"], key=lambda x: x["rel_path"]):
        md.append(f"| `{r['rel_path']}` | {sz(r['size_bytes'])} | {r['mtime']} |")
    md.append("")

    # Conventions
    md.append("---")
    md.append("")
    md.append("## 4. 约定")
    md.append("")
    md.append("- **本文件是只读快照**——agent 不修改它")
    md.append("- **手写维护**：`curated_summaries.json` 跟 source_map.json 同目录")
    md.append("- **不读 PDF 内容**：PDF 只用 metadata（大小/时间），用途从邻近 README 推断")
    md.append("- **不索引嵌入图**（`*.assets/`、`*.images/`）")
    md.append("- **不修改受保护文件**（文件名含 'no modify' / 'no-edit' / 'readonly' 的文件 agent 必须跳过）")
    md.append("")

    # Meta
    md.append("---")
    md.append("")
    md.append("## 5. 元信息")
    md.append("")
    md.append(f"- 生成时间：{datetime.datetime.now().isoformat(timespec='seconds')}")
    md.append(f"- 模式：{mode}")
    md.append(f"- 总文件：{totals['files_total']} (MD: {totals['md_files']}, PDF: {totals['pdf_files']})")
    md.append(f"- 总字数（.md）：{sum(r.get('words', 0) for r in inventory if r['type']=='MD'):,}")
    md.append(f"- 总 H2：{sum(r.get('h2_count', 0) for r in inventory if r['type']=='MD')}")
    md.append("")
    md.append("**End of source map.**")
    md.append("")

    return md


def main():
    p = argparse.ArgumentParser(description="Build source map artifacts from a scan inventory")
    p.add_argument("--inventory", required=True, help="Path to scan_workspace.py JSON output")
    p.add_argument("--md-out", required=True, help="Path to write SOURCE_MAP.md")
    p.add_argument("--json-out", required=True, help="Path to write source_map.json")
    p.add_argument("--curated-out", required=True, help="Path to write curated_summaries.json")
    p.add_argument("--existing-curated", help="Path to existing curated_summaries.json (for update mode)")
    p.add_argument("--mode", choices=["create", "update"], default="create")
    p.add_argument("--prev-inventory", help="Path to previous inventory.json (for diff in update mode)")
    args = p.parse_args()

    inv_data = json.loads(Path(args.inventory).read_text(encoding="utf-8"))
    inventory = inv_data["files"]
    totals = inv_data["totals"]
    workspace_root = inv_data["workspace_root"]

    # Load existing curated summaries (or start empty)
    curated = {}
    if args.existing_curated and os.path.exists(args.existing_curated):
        try:
            curated = json.loads(Path(args.existing_curated).read_text(encoding="utf-8"))
        except Exception:
            curated = {}

    # Drop entries for files that no longer exist
    cur_paths = {r["rel_path"] for r in inventory}
    curated = {p: s for p, s in curated.items() if p in cur_paths}

    # Load previous inventory for diff
    prev_inventory = None
    if args.prev_inventory and os.path.exists(args.prev_inventory):
        try:
            prev_inventory = json.loads(Path(args.prev_inventory).read_text(encoding="utf-8"))["files"]
        except Exception:
            prev_inventory = None

    # Build Markdown
    md_lines = build_markdown(workspace_root, inventory, totals, curated, args.mode, prev_inventory)
    md_content = "\n".join(md_lines)

    # Build JSON (curated summaries embedded, plus full inventory)
    src_map = {
        "metadata": {
            "workspace_root": workspace_root,
            "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
            "mode": args.mode,
        },
        "totals": totals,
        "files": inventory,
        "curated_summaries": curated,
    }

    # Write outputs
    Path(args.md_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.md_out).write_text(md_content, encoding="utf-8")

    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(json.dumps(src_map, ensure_ascii=False, indent=2), encoding="utf-8")

    Path(args.curated_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.curated_out).write_text(json.dumps(curated, ensure_ascii=False, indent=2), encoding="utf-8")

    # Update file size placeholder at end of markdown (final size)
    final_size = os.path.getsize(args.md_out)
    md_content = md_content.replace(
        "**End of source map.**",
        f"- 本文件大小：{sz(final_size)} ({final_size:,} bytes)\n\n**End of source map.**"
    )
    Path(args.md_out).write_text(md_content, encoding="utf-8")

    print(f"Wrote {args.md_out} ({sz(final_size)})", file=sys.stderr)
    print(f"Wrote {args.json_out} ({sz(os.path.getsize(args.json_out))})", file=sys.stderr)
    print(f"Wrote {args.curated_out} ({sz(os.path.getsize(args.curated_out))}, {len(curated)} entries)", file=sys.stderr)
    sys.exit(0)


if __name__ == "__main__":
    main()
