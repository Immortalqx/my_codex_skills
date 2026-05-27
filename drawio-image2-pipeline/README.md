# drawio_image2_pipeline

Chinese version: [README.zh-CN.md](./README.zh-CN.md)

`drawio_image2_pipeline` is a Codex skill repository for research-figure workflows built around an editable `draw.io` / `diagrams.net` draft plus a polished GPT-Image-2 reference image.

The installable skill is in [drawio-image2-pipeline/](./drawio-image2-pipeline/).

## Quick Start

Copy the skill into `$CODEX_HOME/skills/`:

```bash
cp -R drawio-image2-pipeline "$CODEX_HOME/skills/"
```

Then ask Codex to use `$drawio-image2-pipeline` on a paper, poster, or concept-diagram task:

```text
Use $drawio-image2-pipeline to create a research figure from the current workspace.
Read the available paper assets first, reuse useful figures or plots, create an editable draw.io draft under image_draft/,
export PNG/SVG/PDF, run visual QA on the PNG, and only then produce a polished GPT-Image-2 reference image.
Style target: clean technical poster figure.
```

If you already have a `.drawio` file and want Codex to continue from it:

```text
Use $drawio-image2-pipeline on this existing .drawio file.
Keep the structure editable, connect an auto_drawio bridge if available, tighten the layout, re-export, run QA, and then generate the Image2 reference.
```

## How It Works

1. Codex reads the local paper, poster, slides, notes, or experiment materials and checks for reusable visual assets.
2. Codex creates or refines an editable `sketch.drawio` draft.
3. Codex exports PNG/SVG/PDF versions for review.
4. Codex prepares a GPT-Image-2 prompt and generates a polished reference image that follows the approved structure.

## Output

By default, the skill writes to `image_draft/` and typically produces:

- `assets/`
- `asset_manifest.md`
- `sketch.drawio`
- `sketch.png`
- `sketch.svg`
- `sketch.pdf`
- `qa_notes.md`
- `image2_prompt.txt`
- `image2_result.png`
- `image2_response.json`

## Bridge Compatibility

This skill can attach to an existing `auto_drawio` bridge workflow when one is available in the workspace.

The bridge reference is documented in [drawio-image2-pipeline/references/auto_drawio.md](./drawio-image2-pipeline/references/auto_drawio.md). This is useful when the workspace already contains an `auto_presentation/auto_drawio` setup and the user wants live editing plus automatic refresh while Codex refines the diagram.

The bridge itself is not bundled here. This repository only keeps the skill definition and the helper scripts that work with that style of workflow.

## Helper Scripts

- [drawio-image2-pipeline/scripts/inventory_assets.py](./drawio-image2-pipeline/scripts/inventory_assets.py): inventory reusable local assets
- [drawio-image2-pipeline/scripts/render_pdf_pages.py](./drawio-image2-pipeline/scripts/render_pdf_pages.py): render PDF pages into reusable image assets
- [drawio-image2-pipeline/scripts/export_drawio.ps1](./drawio-image2-pipeline/scripts/export_drawio.ps1): export PNG/SVG/PDF from a `.drawio` file
- [drawio-image2-pipeline/scripts/rightcode_image2.py](./drawio-image2-pipeline/scripts/rightcode_image2.py): submit the approved PNG draft to GPT-Image-2 and save the response artifacts

## Reference

This workflow is compatible with the `auto_drawio` bridge style used in:

- [ziyuhuang123/auto_presentation](https://github.com/ziyuhuang123/auto_presentation)

That repository is a useful reference for the surrounding draw.io bridge workflow. This skill focuses that pattern on research figures, posters, and presentation visuals.

## Repository Layout

- `README.md` and `README.zh-CN.md`: repository docs
- `drawio-image2-pipeline/`: installable Codex skill
- `drawio-image2-pipeline/SKILL.md`: installable Codex skill definition
- `drawio-image2-pipeline/scripts/`: deterministic helper scripts
- `drawio-image2-pipeline/references/`: bridge and workflow references
- `drawio-image2-pipeline/agents/`: agent config used by the skill
