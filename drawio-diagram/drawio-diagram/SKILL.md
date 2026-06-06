---
name: drawio-diagram
description: Use when creating research figures, paper posters, academic presentation visuals, or conceptual diagrams as an editable draw.io/diagrams.net draft plus PNG/SVG/PDF exports that pass strict visual QA. Especially for paper figures/posters where Codex must read source materials, reuse extracted paper images or plots when useful, and produce editable draw.io/SVG/PDF assets that the user can keep editing directly in draw.io.
---

# Draw.io Research Figure Pipeline

## Purpose

This skill produces research visuals as a single deliverable:

1. An editable, readable `.drawio` draft plus SVG/PDF/PNG exports that pass strict visual QA.

The draw.io draft is not disposable. It must be good enough for the user to keep editing directly in draw.io and to use as a paper or poster figure on its own.

## Non-Negotiable Gates

Do not declare a figure ready until all gates pass:

1. **Asset gate:** If the task is based on a paper, poster, PDF, slides, Markdown notes, or experiment folder, inspect available figures/images/tables first and reuse useful visual assets instead of redrawing everything from scratch. This is mandatory, not optional.
2. **Editable draft gate:** Produce a `.drawio` that is meaningful and editable by itself. The user must be able to continue editing it in draw.io.
3. **Export gate:** Export PNG/SVG/PDF from the `.drawio`.
4. **Visual QA gate:** Open the exported PNG and inspect it visually. If text is clipped, occluded, distorted, overlapped, unreadable, misaligned, too small, or blocked by icons/shapes, fix the `.drawio`, re-export, and inspect again.
5. **No-blind-export gate:** Never say the PNG is ready just because files exist. The visual preview must be checked.

If any gate fails, repair the draw.io draft first. Do not declare the figure ready.

For research posters and paper figures, the asset gate must produce an `asset_manifest.md` before drawing begins. If relevant visual assets exist but are not used, `qa_notes.md` must explain why each was rejected.

## Privacy Rule

Never store API keys, tokens, auth JSON contents, private URLs, or user secrets inside the skill or generated figure files. Scripts may read credentials at runtime from environment variables or existing local Codex auth files, but must not print them.

## Default Output Folder

Use `image_draft/` by default. Never choose a generic test folder unless the user explicitly names it.

Recommended structure:

```text
image_draft/
  assets/                  # extracted paper images, plots, screenshots
  asset_manifest.md        # inventory of usable source visuals
  sketch.drawio            # editable semantic draft
  sketch.png               # visual QA preview
  sketch.svg               # editable/vector export
  sketch.pdf               # paper/poster export
  qa_notes.md              # visual QA checklist and fixes
```

If `image_draft/` already exists, create a versioned subfolder such as `image_draft/run_002/` unless the user asks to overwrite.

## Source Material Workflow

For research tasks, first build content from source materials:

- Read the paper/PDF/slides/notes enough to identify the actual method, problem setting, main claim, experimental evidence, and available figures.
- Treat user-provided screenshots/images in the conversation as source assets too: inspect them and reuse them when they contain useful paper figures, layouts, plots, or visual examples.
- Search local folders for `.pdf`, `.pptx`, `.md`, `.png`, `.jpg`, `.jpeg`, `.svg`, `.webp`, and figure asset folders.
- Run or manually create an asset inventory before sketching. Use `scripts/inventory_assets.py` when possible.
- Extract or reuse relevant visual material:
  - method diagrams
  - robot/camera setup images
  - pipeline screenshots
  - result plots/tables
  - qualitative examples
  - ablation charts
- Put reused assets under `image_draft/assets/`.
- Insert useful assets into draw.io when they improve fidelity. Do not replace real paper figures with weak hand-drawn substitutes.
- For a paper poster, at least one relevant method/result/setup/qualitative asset should be inserted when such assets exist. If none are inserted, justify this explicitly in `qa_notes.md`.
- If the source paper includes figures that communicate the method, robot/camera setup, dataset, results, ablations, or qualitative examples, those figures have priority over newly invented icons or generic boxes.
- Keep figure assets as movable draw.io image objects where possible. If programmatic insertion is unreliable, use the `auto_drawio` browser editor or draw.io desktop to insert the images, then re-export and inspect.
- Use `scripts/render_pdf_pages.py` when possible.

## Draw.io Draft Requirements

The draft must be clean:

- Fixed canvas size appropriate to the task, usually 16:9 for posters or `1536x1024`-like landscape.
- Stable grid: columns, rows, and section titles must align.
- No text under shapes, arrows, image crops, icons, badges, or panel borders.
- No text clipping or overflow.
- No ambiguous arrows.
- No title/body/media collisions.
- All panels must have enough internal padding.
- All labels must be concise and editable.
- Use real extracted paper figures/images where useful; embed or reference them in draw.io so the user can move/replace them.
- Do not create a generic diagram if the paper already provides relevant visual evidence. Use the paper's method figure, setup figure, result chart, or qualitative examples as visual anchors.
- Keep the draft independent: no "according to the paper", "from PDF", or "adapted from notes" in the visible figure.

For academic posters, prefer:

- A strong title band.
- 3-4 main sections.
- Method/architecture in the center.
- Real result numbers/plots on the right or bottom.
- Key takeaways in a dedicated strip.
- Paper images/robot setup/qualitative examples as visual anchors when available.

## Mandatory Visual QA Loop

After every draw.io export:

1. Open `sketch.png` with an image viewer or `view_image`.
2. Check at full-image scale and zoomed into dense regions.
3. Record pass/fail in `qa_notes.md`.
4. If fail, fix the `.drawio`, re-export, and inspect again.

QA checklist:

```text
- [ ] Title is readable and not clipped.
- [ ] Every panel title has a fixed area and does not overlap body text.
- [ ] Body text fits inside its box with padding.
- [ ] No image, icon, arrow, badge, or crop covers text.
- [ ] No text extends outside panel boundaries.
- [ ] All arrows point in the intended direction.
- [ ] Extracted figures/images are visible and not distorted.
- [ ] Relevant source assets were inserted, or each unused relevant asset is justified in `qa_notes.md`.
- [ ] Result numbers/axis labels are readable when included.
- [ ] The draft is useful as a standalone editable draw.io artifact, with all labels and structure understandable without external context.
```

Only after every item passes may the figure be declared ready.

## auto_drawio Bridge

If `auto_presentation/auto_drawio` is available, connect the draft so the user can watch and edit live. See `references/auto_drawio.md`.

Use the bridge for interactive review whenever possible. If no bridge is available, still create the `.drawio` and inspect exported PNG as part of the visual QA loop.

## Export

Use `scripts/export_drawio.ps1` when possible:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/export_drawio.ps1 `
  -DrawioPath "<image_draft>/sketch.drawio" `
  -OutDir "<image_draft>"
```

The exported PNG is the visual QA preview. Embedded draw.io metadata can create very large PNG text chunks, so the provided export script leaves PNG diagram embedding off by default. Keep the editable `.drawio` as the source of truth. Use `-EmbedPngDiagram` only when a self-contained editable PNG is explicitly needed.

## Final Response

Report:

- Bridge URL if running.
- `.drawio`, `.svg`, `.pdf`, `.png`, and `qa_notes.md` paths.
- Whether source figures/images were reused.
- Whether visual QA passed.

If visual QA did not pass, stop and report that the figure is not ready and describe what was fixed in the latest iteration.