# Temp Layout

Use this reference when creating a new task directory, extending an existing one, or cleaning up how new artifacts are written.

## Temp Root Selection

Common valid temp-like roots include:

- `x_temp_codex`
- `x_temp`
- `temp_codex`
- `temp`
- `tmp`
- `codex_temp`
- `.temp`

Nested roots such as `.../temp_codex/` inside an existing task area are also valid.

When multiple candidates exist, prefer in this order:

1. an existing temp root already used for similar tasks in the same workspace subtree
2. a root whose name strongly suggests Codex or agent temporary work, such as `x_temp_codex`, `temp_codex`, or `x_temp`
3. a generic temp root

Do not choose a leaf artifact folder such as these as the task root:

- `cache/`
- `renders/`
- `screenshots/`
- `notes/`
- `search/`
- `audit/`
- `pdf_pages_*`
- `thumbnails/`
- `x_temp_user_text/`

When both agent-oriented and user-oriented temp roots exist, prefer the agent-oriented root unless the user says otherwise.

If no suitable temp-like directory exists, create one in the workspace. Reuse the local naming style if it is obvious. Otherwise prefer `x_temp_codex/` when the workspace already uses `x_*` utility folders; if not, create `temp_codex/`.

## Task Subfolder Selection

Inside the temp root, create or reuse a task-specific subfolder.

Common naming patterns include:

- `<topic>`
- `<topic>_<YYYYMMDD>`
- `<date>_<task>`
- `<task>_v02`
- `<task>_<YYYYMMDD>_v03`

Choose an existing task subfolder when it clearly matches the current task by topic, paper set, output target, or recent related artifacts. If none exists, create one following the local naming style. If no local pattern is visible, default to `<task-slug>_<YYYYMMDD>` and add a version suffix when needed.

## Required Layout

```text
<temp-root>/<task-subdir>/
  prompt.txt
  prompt_history.md
  task_summary.md
  manifest.json
  local_source_map.md
  local_source_map.json
  evidence_map.md
  completion_audit.md
  sources/
    user_files/
    fetched/
  extracted_text/
    page_text/
    ocr/
  renders/
    pages/
    verification/
  screenshots/
    selected/
  search/
    queries/
    results/
  notes/
  scripts/
  logs/
  audit/
```

Only prompt, summary, manifest, source-map, evidence-map, and audit files should live directly under the task subfolder. PDFs, webpages, images, extracted text, helper scripts, logs, and intermediate notes should go into typed subfolders or the closest existing local equivalent.

## Reusable Local Equivalents

If the workspace already has a stronger local convention, reuse it instead of forcing the layout above. Common reusable patterns include:

- `sources/`, `external/`, or `downloads/` for fetched files
- `cache/`, `text_extracts/`, `pdf_text/`, or `selected_text/` for extracted text
- `pdf_pages_*`, `renders/`, `thumbnails/`, or `verify_thumbs/` for rendered images
- `notes/`, `web_notes/`, `research_log.md`, `round_log.md`, or `current_task.md` for continuation state
- `local_source_map*.md`, `source_map*.json`, `evidence_map*.md`, `manifest.json`, or `file_inventory.jsonl` for source-tracking artifacts

## Messy Existing Folders

If an existing task folder is already messy:

- stop adding loose files to the root
- put all new artifacts into typed subfolders
- record existing loose files in the manifest or source map
- do not move or rename existing files unless the user asks
