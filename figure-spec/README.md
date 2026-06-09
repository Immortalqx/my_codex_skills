# figure-spec

Chinese version: [README.zh-CN.md](./README.zh-CN.md)

`figure-spec` generates deterministic, editable SVG diagrams from structured FigureSpec JSON. It is intended for publication-quality architecture, workflow, pipeline, audit cascade, and topology figures.

Use `$figure-spec` when you need a precise vector diagram whose layout should be reproducible:

```text
Use $figure-spec to create an editable SVG workflow diagram for this method.
```

## Dependency Note

No API key is required. The renderer runs locally from the bundled Python script.

## Workflow

1. Convert the diagram goal into structured FigureSpec JSON.
2. Validate the spec with `scripts/figure_renderer.py`.
3. Render SVG from the spec.
4. Inspect the SVG/PDF and revise the JSON, not the generated SVG.

## Helper Scripts

- `figure-spec/scripts/figure_renderer.py`: validates and renders FigureSpec JSON.

## Contents

- `figure-spec/SKILL.md`: Codex skill definition.
- `figure-spec/scripts/`: deterministic renderer.
- `figure-spec/agents/openai.yaml`: UI metadata.
