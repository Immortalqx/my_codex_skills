---
name: update-source-map
description: Create or update an agent-readable source map (Markdown + JSON) for any project directory. Use when Codex needs to (1) index an unfamiliar workspace before doing work in it, (2) refresh a stale source map after files are added, removed, or renamed, (3) prepare quick navigation context for a multi-turn task that touches many files, or (4) hand a downstream agent a structured inventory of the project. Auto-detects whether to create a new map or update an existing one based on the presence of `x_temp/SOURCE_MAP.md` or `SOURCE_MAP.md` at the workspace root. Outputs are human-readable Markdown for navigation and structured JSON for programmatic queries. Curated file summaries in a separate JSON file persist across regenerations.
---

# Update Source Map

## Overview

Build (or refresh) a structured, agent-readable index of a project directory. The skill always produces a **Markdown** `SOURCE_MAP.md` (primary, human + agent) and a **JSON** `source_map.json` (programmatic). A hand-curated `curated_summaries.json` is preserved across regenerations so the agent's per-file knowledge compounds over time.

## When this skill runs

Trigger on requests like:
- "build a source map for this project"
- "update the source map"
- "create a project index"
- any task where Codex is about to do work in a workspace it doesn't already know well

Do **not** trigger for: code refactoring, single-file edits, paper reading, or tasks unrelated to project navigation.

## Workflow

### Step 1 — Decide mode (auto-detect)

Run `scripts/detect_existing.py <workspace_root>` to decide between **create** and **update** mode. Detection priority:

1. `<workspace>/x_temp/SOURCE_MAP.md` + `x_temp/source_map.json` → update
2. `<workspace>/SOURCE_MAP.md` + `source_map.json` → update
3. `<workspace>/.codex/source_map.json` → update
4. Otherwise → create

The detection JSON has fields: `mode`, `md_path`, `json_path`, `found_at`. Pass `--force-mode create|update` to override.

If detection returns `partial: true` (only one of the two files exists), warn the user before proceeding.

### Step 2 — Plan with user (always)

Before any execution, report the plan:

- Which mode (create / update) and why
- Which workspace to scan
- Where the outputs will go (default: `<workspace>/x_temp/`)
- Any custom exclusions or extensions
- Estimated file count from a quick `find` (to set expectations)

Get explicit approval before running scripts. Do not silently start.

### Step 3 — Setup

Create the output directory if it doesn't exist:
```bash
mkdir -p <workspace>/x_temp
```

For update mode with diff support, also keep the previous inventory:
```bash
mv <workspace>/x_temp/file_inventory.jsonl <workspace>/x_temp/file_inventory.prev.jsonl
```
(only if regeneration would otherwise lose it)

### Step 4 — Run the pipeline

Two equivalent options:

**Option A — one-shot CLI** (recommended for simple cases):
```bash
python3 scripts/regenerate.py <workspace_root> \
    [--output-dir x_temp] \
    [--force-mode create|update] \
    [--exclude "extra_dir1,extra_dir2"] \
    [--keep-prev-inventory]
```

**Option B — modular** (use when the agent needs to inspect intermediate results):
```bash
# 1. Scan
python3 scripts/scan_workspace.py <workspace_root> \
    --output <workspace>/x_temp/file_inventory.jsonl \
    [--exclude "..."]

# 2. Build
python3 scripts/build_source_map.py \
    --inventory <workspace>/x_temp/file_inventory.jsonl \
    --md-out <workspace>/x_temp/SOURCE_MAP.md \
    --json-out <workspace>/x_temp/source_map.json \
    --curated-out <workspace>/x_temp/curated_summaries.json \
    --mode create|update \
    [--existing-curated <workspace>/x_temp/curated_summaries.json] \
    [--prev-inventory <workspace>/x_temp/file_inventory.prev.jsonl]
```

### Step 5 — Verify (do not skip)

After building, **always** check the following. Each check has a known failure mode from real past runs:

1. **JSON validity**: `python3 -c "import json; json.load(open('<json_path>'))"` — must succeed
2. **File count consistency**: MD + PDF count in `source_map.json["totals"]` must equal `len(files)` — catches partial writes
3. **No type-mismatch in tables**: spot-check 1 row of the Markdown — `r["type"]` should appear in the type column (known bug: hardcoded "PDF" leaked into MD rows in earlier versions)
4. **No root-file-as-folder bug**: top-level rollup table should only contain real folders, not files at workspace root
5. **Curated summaries not lost**: if update mode, `curated_summaries.json` count should be ≥ previous count minus deleted files
6. **No `notes.assets/` leakage**: `find <workspace>/x_temp -name "*.png" -o -name "*.jpg"` should return nothing
7. **Original files untouched**: `find <workspace> -newer <workspace>/x_temp/SOURCE_MAP.md -type f` should not return anything (or only items inside `x_temp/`)

If any check fails, fix the source (`build_source_map.py`) and re-run. Do not patch the output Markdown by hand.

### Step 6 — Hand off

Tell the user:
- Mode used (create / update)
- Number of files indexed
- Where the artifacts live
- Any diff highlights (in update mode)
- Whether the curated_summaries.json was preserved / extended

Append the standard completion audit block (see "Completion audit" below).

## Quick reference — script purposes

| Script | Purpose | Standalone? |
|---|---|---|
| `detect_existing.py` | Decide create vs update by looking for existing artifacts | Yes (CLI) |
| `scan_workspace.py` | Walk the workspace, emit per-file metadata + H2/H3 for .md | Yes (CLI) |
| `extract_headings.py` | Extract H2/H3 from a single .md file (quick one-off) | Yes (CLI) |
| `build_source_map.py` | Take inventory, build Markdown + JSON + curated | Yes (CLI) |
| `regenerate.py` | One-shot orchestrator: detect → scan → build | Yes (CLI) |

## Reference docs (load on demand)

- `references/format-spec.md` — exact schema of `SOURCE_MAP.md`, `source_map.json`, `curated_summaries.json`. Read when you need to know the output structure precisely.
- `references/create-vs-update.md` — the auto-detection rules, when to force-mode, and how curated summaries survive updates. Read when mode decision is unclear.
- `references/exclusions-default.md` — what's filtered out by default, how to add custom exclusions, and the "no modify" file boundary. Read before scanning an unfamiliar project.

## Boundaries (non-negotiable)

- ❌ Never modify files outside the output directory (default: `<workspace>/x_temp/`)
- ❌ Never read PDF contents — metadata only
- ❌ Never index image assets (`*.assets/`, `*.images/`, etc.)
- ❌ Never touch files with names containing `no modify`, `no-edit`, `readonly`, `do not touch`
- ❌ Never overwrite `curated_summaries.json` entries that the user / agent curated by hand
- ❌ Never reformat a regeneration silently — if file count changes, surface the diff to the user

## Completion audit

At the end of every run, append:

```text
Completion audit:
- Mode: create | update
- Files indexed: <N> (MD: <M>, PDF: <P>)
- Outputs: <md_path>, <json_path>, <curated_path>
- Curated summaries preserved: yes (N entries) | no (create mode)
- Diff: <N> added, <M> removed (update mode only)
- Original files touched: no
- All 7 verify checks passed: yes | <failed checks>
```

## Lessons embedded in this skill

The skill encodes mistakes from a prior real-world run on a 43-file / 66MB personal knowledge base:

1. **Type-mismatch bug**: hardcoding "PDF" in a loop over a folder that contains a README.md — fixed by using `r["type"]` everywhere
2. **Root-file-as-folder bug**: top-level rollup loop treated root-level files as if they were subdirectories — fixed by skipping `len(parts) == 1` in `compute_top_rollups`
3. **Double-slash in tree root**: render_tree passed both name and a trailing slash — fixed by single source of truth in `tree_root`
4. **Lost curated knowledge**: if curated summaries were stored in the build script, they were lost on every regeneration — fixed by extracting to `curated_summaries.json`
5. **PDF binary read attempts**: the agent sometimes tries to `read_text()` on PDFs — fixed by never opening PDFs for content, only metadata

When you add new scripts, check the verify checklist in Step 5 for additional bugs to add.
