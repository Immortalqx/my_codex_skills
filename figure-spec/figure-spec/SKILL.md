---
name: figure-spec
description: "Generate deterministic publication-quality architecture, workflow, and pipeline diagrams from structured JSON (FigureSpec) into editable SVG. Use when user says \"架构图\", \"workflow 图\", \"pipeline 图\", \"确定性矢量图\", \"figure spec\", \"draw architecture\", or needs precise, editable, publication-ready vector diagrams. Preferred over AI illustration for formal architecture/workflow figures."
---

# FigureSpec: Deterministic JSON → SVG Figure Generation

Generate publication-quality **architecture diagrams**, **workflow pipelines**, **audit cascades**, and **system topology** figures as editable SVG vector graphics using a deterministic JSON → SVG renderer.

## When to Use This Skill

**Use `figure-spec`** for:
- System architecture diagrams (layered, hub-and-spoke, multi-plane)
- Workflow / pipeline figures
- Audit cascade / flow-control diagrams
- Any structured diagram where node positions, connections, and groupings are semantically important
- Figures that need to be edited/tweaked later (SVG is plain text)
- Figures where determinism matters (same spec → same SVG)

**Do NOT use for:**
- Data plots (bar/line/scatter)
- Natural/qualitative illustrations
- Quick state-machine / flowchart diagrams where simple Markdown syntax is enough

## Core Properties

- **Deterministic**: identical FigureSpec JSON always produces identical SVG output (for a fixed renderer version + fonts)
- **Editable**: SVG output is plain-text, can be post-edited by hand or programmatically
- **Validated**: renderer enforces schema, rejects malformed specs with clear error messages
- **Shape-aware**: edge clipping works correctly for rect/rounded/circle/ellipse/diamond
- **CJK support**: multi-line labels with proper Chinese character width estimation
- **No external API**: runs fully local, no network, no API keys

## Tool Location

`scripts/figure_renderer.py` inside this skill directory. Invoke via:

```bash
python scripts/figure_renderer.py render <spec.json> --output <out.svg>
python scripts/figure_renderer.py validate <spec.json>
python scripts/figure_renderer.py schema
```

## Workflow

### Step 1: Understand the Diagram Goal

From `$ARGUMENTS` (description or path to `PAPER_PLAN.md` / `NARRATIVE_REPORT.md`), identify:
- **Purpose**: architecture, workflow, pipeline, audit cascade, topology?
- **Main entities**: what are the boxes?
- **Relationships**: how do they connect? (uses, produces, calls, verifies, chains)
- **Grouping**: do entities cluster into named regions?
- **Hierarchy vs network**: stacked layers, left-to-right flow, or central hub?

### Step 2: Draft the FigureSpec JSON

Canvas sizing guide:
- Single-column figure: ~500×350 px
- Two-column (full-width): ~900×500 px
- Tall topology: ~700×700 px

Start from a template based on the diagram type:

**Architecture (stacked rows)**:
```json
{
  "canvas": {"width": 900, "height": 520},
  "nodes": [
    {"id": "layer1_label", "label": "Layer 1", "x": 450, "y": 60, ...},
    {"id": "node_a", "label": "A", "x": 180, "y": 120, ...},
    {"id": "node_b", "label": "B", "x": 350, "y": 120, ...}
  ],
  "edges": [...],
  "groups": [
    {"label": "Layer 1", "node_ids": ["node_a", "node_b"], "fill": "#F0F9FF", "stroke": "#BAE6FD"}
  ]
}
```

**Workflow (left-to-right chain)**:
```json
{
  "canvas": {"width": 900, "height": 300},
  "nodes": [
    {"id": "step1", "label": "Step 1", "x": 100, "y": 150, "shape": "rounded"},
    {"id": "step2", "label": "Step 2", "x": 280, "y": 150, "shape": "rounded"}
  ],
  "edges": [
    {"from": "step1", "to": "step2", "label": "produces"}
  ]
}
```

**Decision diamond**:
```json
{"id": "check", "label": "Passes?", "shape": "diamond", "x": 450, "y": 200}
```

### Step 3: Render and Validate

```bash
# Validate first
python scripts/figure_renderer.py validate /tmp/spec.json

# Render to SVG
python scripts/figure_renderer.py render /tmp/spec.json --output figures/fig_arch.svg

# Convert to PDF for LaTeX inclusion
rsvg-convert -f pdf figures/fig_arch.svg -o figures/fig_arch.pdf
```

If validation fails, inspect the error (missing field, duplicate ID, overlap warning, invalid hex color) and fix the JSON.

### Step 4: Visual Check

Open the SVG/PDF and check:
- **No overlaps**: nodes don't collide with each other or group boundaries
- **Readability**: font sizes are consistent, labels aren't clipped
- **Edge clarity**: arrows hit nodes at clean angles, labels near edges are legible
- **Group alignment**: background rectangles frame their members cleanly
- **Color distinction**: categories are visually distinct in both color and grayscale

If issues found, edit the JSON spec (never the generated SVG) and re-render.

## Schema Quick Reference

Run `python scripts/figure_renderer.py schema` for the authoritative schema.

### Nodes

| Field | Required | Default | Notes |
|-------|----------|---------|-------|
| `id` | ✓ | — | Unique |
| `label` | ✓ | — | `\n` for multi-line |
| `x`, `y` | ✓ | — | Center coordinates |
| `width`, `height` | | 120, 50 | |
| `shape` | | `rounded` | `rect` / `rounded` / `circle` / `ellipse` / `diamond` |
| `fill`, `stroke` | | auto from palette | `#RRGGBB` |
| `text_color` | | `#333333` | |
| `font_size` | | 14 | Override style default |

### Edges

| Field | Default | Notes |
|-------|---------|-------|
| `from`, `to` | required | Same = self-loop |
| `label` | — | Short edge label |
| `style` | `solid` | `solid` / `dashed` / `dotted` |
| `color` | `#555555` | |
| `curve` | `false` | Curved path |

### Groups

Rectangular background regions framing a set of nodes:
```json
{"label": "Layer Name", "node_ids": ["a", "b", "c"], "fill": "#EFF6FF", "stroke": "#BFDBFE"}
```

## Design Patterns

### Pattern 1: Layered Architecture
Stack rows of related nodes, each row is a group, add inter-layer arrows with semantic labels (`uses↓`, `produces↑`, `checks↓`).

### Pattern 2: Hub-and-Spoke
Central node (e.g., Executor), peripheral nodes (skills, tools), solid arrows for primary relations, dashed for feedback.

### Pattern 3: Pipeline with Feedback
Left-to-right main flow, feedback arrows curve below with `curve: true`.

### Pattern 4: Audit Cascade
Three-stage horizontal cascade with inputs feeding in from top, outputs exiting right, each stage in its own group.

## Anti-Patterns

- **Don't use groups as hierarchy**: groups frame peer nodes, not containment
- **Don't nest groups**: renderer draws them as background rectangles; nested groups look like Russian dolls
- **Don't cross-draw long diagonals**: if an arrow crosses 3+ rows, rethink the layout
- **Don't mix font sizes for same role**: keep one size per node category

## Output Contract

- SVG file in `figures/` (vector, editable, hand-tweakable)
- Source FigureSpec JSON saved in `figures/specs/` for reproducibility
- PDF version via `rsvg-convert` for LaTeX inclusion

## Standalone Scope

The workflow is local and deterministic: read the source material, inspect the
rendered SVG/PDF, revise the FigureSpec JSON, and re-render until the diagram is
clear and accurate.
