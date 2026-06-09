# Create vs Update — Decision Reference

## Auto-Detection (default)

The skill auto-detects mode by looking for existing artifacts in this priority order:

1. `<workspace>/x_temp/SOURCE_MAP.md` AND `<workspace>/x_temp/source_map.json` → **update**
2. `<workspace>/SOURCE_MAP.md` AND `<workspace>/source_map.json` → **update**
3. `<workspace>/.codex/SOURCE_MAP.md` AND `<workspace>/.codex/source_map.json` → **update**
4. Otherwise → **create**

If only one of `SOURCE_MAP.md` / `source_map.json` exists at a location, that location is treated as update (with a `partial: true` warning in the detection JSON).

## Create Mode

- Triggered when no source map exists at standard locations
- Behavior:
  - Full scan of workspace
  - Build new `SOURCE_MAP.md` + `source_map.json`
  - Initialize `curated_summaries.json` as empty `{}`
  - No diff section in output (nothing to diff against)
- Use case: First time indexing a project, or after deleting the old source map

## Update Mode

- Triggered when source map exists at standard locations
- Behavior:
  - Re-scan workspace
  - **Preserve** entries in `curated_summaries.json` (drop only entries for files that no longer exist)
  - Add **diff section** to the markdown listing added/removed files
  - Optionally keep `file_inventory.prev.jsonl` for deeper diff (via `--keep-prev-inventory`)
- Use case: After adding/removing/renaming files in the project

## Force Override

The CLI accepts `--force-mode create|update` to override auto-detection:

```bash
# Force re-create from scratch (will lose existing curated_summaries.json)
python3 regenerate.py <workspace> --force-mode create

# Force update even if no existing map found (no diff section)
python3 regenerate.py <workspace> --force-mode update
```

## Important: Curated Summaries Survive Updates

The hand-curated 1-line summaries in `curated_summaries.json` are the most valuable content of a source map. The skill guarantees they survive every update. To extend a map:

1. Open `curated_summaries.json`
2. Add an entry: `"path/to/new/file.md": "1-line description of what this file covers"`
3. Re-run the skill — the new entry appears in the next `SOURCE_MAP.md`
