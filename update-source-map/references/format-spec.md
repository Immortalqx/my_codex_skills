# Output Format Spec

The skill produces three artifacts, all in the same output directory (default: `<workspace>/x_temp/`):

## 1. `SOURCE_MAP.md` — Primary Deliverable (Markdown)

A human + agent readable index. Sections in fixed order:

1. **Header** — name, generated timestamp, workspace, mode, scope counts
2. **Diff block** (update mode only) — list of added/removed files since last scan
3. **TL;DR** — 5-line executive summary
4. **Top-level rollup** — table of top-level folders with size + MD/PDF counts
5. **Visual tree** — ASCII tree with sizes (excludes root-level files that aren't folders)
6. **Per-folder deep-dive** — for each folder, list files with curated 1-line summaries
7. **Full file inventory** — separate tables for .md and .pdf
8. **Conventions** — fixed rules the agent must obey
9. **Meta** — generation timestamp, totals

Format conventions:
- All file paths wrapped in backticks: `` `path/to/file.md` ``
- Sizes in human format: `B`, `KB`, `MB`
- Word counts comma-separated: `1,234`
- Date format: `YYYY-MM-DD`
- All tables are GitHub-flavored Markdown
- UTF-8, no BOM

## 2. `source_map.json` — Structured Companion (JSON)

Top-level keys:

```json
{
  "metadata": {
    "workspace_root": "<abs path>",
    "generated_at": "<ISO 8601>",
    "mode": "create" | "update"
  },
  "totals": {
    "files_total": 43,
    "md_files": 32,
    "pdf_files": 11
  },
  "files": [
    {
      "rel_path": "README.md",
      "filename": "README.md",
      "type": "MD" | "PDF",
      "size_bytes": 7399,
      "mtime": "2026-06-04",
      "folder": ".",
      // .md only:
      "chars": 7399,
      "words": 727,
      "lines": 122,
      "h2_titles": ["Section 1: ...", "Section 2: ..."],
      "h3_titles": ["1.1 ...", "1.2 ..."],
      "h2_count": 5,
      "h3_count": 0
    }
  ],
  "curated_summaries": {
    "README.md": "Main project README — defines 5 core questions and 4-folder structure",
    "1_Classical Robotics/README.md": "..."
  }
}
```

## 3. `curated_summaries.json` — Hand-Curated Layer (JSON)

```json
{
  "README.md": "1-2 line summary of what this file covers",
  "path/to/file.md": "Another hand-written summary"
}
```

This is the only file the user/agent is expected to edit over time. The skill:
- Loads existing entries in update mode
- Preserves them across regenerations
- Drops entries for files that no longer exist
- New files start with no entry (the H2 skeleton in the markdown gives the auto-summary)

## What is NOT included

- PDF contents (binary, never read)
- Image assets in `*.assets/` or `*.images/` directories
- File contents from non-`.md` / non-`.pdf` extensions
- Embedded links / external references
- Git history
- Cross-file dependencies (a separate analysis pass)
