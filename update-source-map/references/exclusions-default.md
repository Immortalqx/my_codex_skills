# Default Exclusion Rules

The skill **skips** the following by default. Pass `--exclude "a,b,c"` to add more.

## Always-Excluded File Names

- `.DS_Store` (macOS metadata)
- Files in `__pycache__/`
- `*.pyc` (compiled Python — though `.py` itself is not scanned anyway)

## Always-Excluded Directory Names

- `node_modules` — Node.js dependencies
- `__pycache__` — Python bytecode
- `.git` — Git internals
- `.venv` / `venv` — Python virtual envs
- `dist` / `build` — build outputs
- `notes.assets` — note-editor-style embedded images
- `x_temp` — Codex-style temp/task workspace
- `x_temp_*` — any `x_temp_<date>` task subfolder

## Never-Read File Extensions

- `.pdf` — binary, never read; metadata-only
- All extensions except `.md` are skipped (this is by design — the source map is for human-readable content)

## Files with "Do Not Modify" Names

The skill must NEVER write to files whose name contains: - `no modify` - `no-edit` - `no_edit` - `readonly` - `do not touch`

These are typically protected master files (e.g. `README - No Modify.md`). The skill detects them in the file inventory and the agent must respect the boundary.

## User-Configurable

```bash
# Add custom directory names to exclude
python3 regenerate.py <workspace> --exclude "my_private,backup,old"

# Scan only markdown (skip PDFs)
python3 regenerate.py <workspace> --ext "md"

# Scan a different mix
python3 regenerate.py <workspace> --ext "md,pdf,tex"
```

## Image / Asset Directories

Embedded images in markdown notes are typically in folders named: - `*.assets/` - `*.images/` - `attachments/` - `media/`

These are excluded by default. If the project has an unusual convention (e.g. `figures/`), add it to `--exclude`.
