# update_source_map

Chinese version: [README.zh-CN.md](./README.zh-CN.md)

`update_source_map` is a Codex skill that creates or updates an **agent-readable source map** for any project directory.

The source map is a structured index of a project's files (`.md` notes + `.pdf` documents), with one-line summaries per file, file sizes, modification times, and a heading skeleton for every markdown file. It is designed so that an AI agent (or a human) can quickly answer "what's in this project, and where do I find X?" without reading every file.

The skill auto-detects whether a source map already exists in the workspace:
- **Create** mode: builds a new `SOURCE_MAP.md` + `source_map.json` from scratch
- **Update** mode: re-scans the workspace, preserves the hand-curated per-file summaries, and shows a diff of what changed since the last scan

## When to use

- When starting work in a new / unfamiliar workspace
- When files have been added / removed / renamed and the existing index is stale
- When preparing context for a multi-turn task that touches many files
- When handing a project over to another agent who needs navigation help

## What it produces

Three files in `<workspace>/x_temp/` (or your chosen output dir):

| File | Format | Purpose |
|---|---|---|
| `SOURCE_MAP.md` | Markdown | Primary deliverable — human + agent readable |
| `source_map.json` | JSON | Structured data — programmatic queries |
| `curated_summaries.json` | JSON | Hand-written per-file summaries (preserved across regenerations) |

## Important Boundary

This skill is for **navigation and inventory**, not for:
- Reading or summarizing file contents (use other skills for that)
- Refactoring or editing files
- Running experiments

The source map tells the agent what's in the project and where to look. It does not replace the actual files.

## Source

The skill encodes patterns learned from a real source map run on a 43-file / 66MB personal knowledge base. See the [SKILL.md](./update-source-map/SKILL.md) for the full workflow, the [references/](./update-source-map/references/) for the format spec and detection rules, and the [scripts/](./update-source-map/scripts/) for the executable code.
