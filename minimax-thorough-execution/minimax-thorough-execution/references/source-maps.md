# Source Maps

Use this reference when creating or extending source-tracking artifacts.

## What To Look For

Common existing source-tracking artifacts include:

- `x_codex/source_map.json`
- `x_codex/manifest.json`
- `x_codex/file_inventory.jsonl`
- task-local `local_source_map*.md`
- task-local `source_map*.json`
- task-local `evidence_map*.md`

Prefer two levels when possible:

1. a workspace-level source map or manifest, if one already exists
2. a task-level source map for the current run or task subtree

If no workspace-level source map exists, do not invent a fake global registry unless the task genuinely needs one. The task-level map is enough.

## Task-Level Source Map Fields

Record these fields when applicable:

- local path
- original source URL or origin description
- source type, such as PDF, slide, screenshot, webpage, notes, extracted text, or derived artifact
- relation to the task, such as primary evidence, supplementary evidence, candidate source, cache only, or output support
- read status, such as queued, skimmed, deeply read, visually verified, or blocked
- whether the file is original evidence or a derived cache artifact
- brief notes about why it matters

## Evidence Map

The evidence map should track which claims or subtasks are supported by which sources.

## Important Boundary

- source maps are organizational tools and continuation aids
- source maps are not final evidence by themselves
- actual claims must still be grounded in original papers, original pages, original rendered images, or original web sources
