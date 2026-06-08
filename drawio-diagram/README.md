# drawio_diagram

Chinese version: [README.zh-CN.md](./README.zh-CN.md)

`drawio_diagram` is a Codex skill repository for research-figure workflows. The deliverable is an editable `draw.io` / `diagrams.net` draft plus its PNG/SVG/PDF exports that have passed strict visual QA. The draw.io draft is meant to be reused and edited by the user directly, not discarded as an intermediate artifact.

## How It Works

1. Codex reads the local paper, poster, slides, notes, or experiment materials and checks for reusable visual assets.
2. Codex creates or refines an editable `sketch.drawio` draft.
3. Codex exports PNG/SVG/PDF versions for review.
4. Codex runs the visual QA loop on the PNG, fixes the `.drawio`, and re-exports until the QA checklist passes.

## Output

By default, the skill writes to `image_draft/` and typically produces:

- `assets/`
- `asset_manifest.md`
- `sketch.drawio`
- `sketch.png`
- `sketch.svg`
- `sketch.pdf`
- `qa_notes.md`

## Bridge Compatibility

This skill can attach to an existing `auto_drawio` bridge workflow when one is available in the workspace.

The bridge reference is documented in [drawio-diagram/references/auto_drawio.md](./drawio-diagram/references/auto_drawio.md). This is useful when the workspace already contains an `auto_presentation/auto_drawio` setup and the user wants live editing plus automatic refresh while Codex refines the diagram.

The bridge itself is not bundled here. This repository only keeps the skill definition and the helper scripts that work with that style of workflow.

## Helper Scripts

- [drawio-diagram/scripts/inventory_assets.py](./drawio-diagram/scripts/inventory_assets.py): inventory reusable local assets
- [drawio-diagram/scripts/render_pdf_pages.py](./drawio-diagram/scripts/render_pdf_pages.py): render PDF pages into reusable image assets
- [drawio-diagram/scripts/export_drawio.ps1](./drawio-diagram/scripts/export_drawio.ps1): export PNG/SVG/PDF from a `.drawio` file

## Reference

This workflow is compatible with the `auto_drawio` bridge style used in:

- [ziyuhuang123/auto_presentation](https://github.com/ziyuhuang123/auto_presentation)

That repository is a useful reference for the surrounding draw.io bridge workflow. This skill focuses that pattern on research figures, posters, and presentation visuals.

## Repository Layout

- `README.md` and `README.zh-CN.md`: repository docs
- `drawio-diagram/`: Codex skill files
- `drawio-diagram/SKILL.md`: Codex skill definition
- `drawio-diagram/scripts/`: deterministic helper scripts
- `drawio-diagram/references/`: bridge and workflow references
- `drawio-diagram/agents/`: agent config used by the skill
