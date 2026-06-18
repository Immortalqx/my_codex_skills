---
name: paper-reading
description: >-
  Deep, critical paper-reading workflow that produces a structured reading
  note. Use when the user wants to read, understand, summarize, break down,
  or take notes on a single research paper. English triggers: "read this
  paper", "read the paper", "paper reading", "paper notes", "deeply read",
  "critically read", "summarize this paper", "break down the paper",
  "explain this paper", "walk me through this paper", "help me understand
  this paper". Chinese triggers: "读论文", "精读论文", "理解论文", "拆解
  论文", "整理论文笔记", "帮我看这篇论文", "分析这篇论文". Also triggers
  when the user hands over a .pdf, an arXiv URL or ID, or a paper title and
  asks for deep understanding. NOT for quick one-paragraph overviews (use
  alphaxiv), broad literature surveys (use research-lit), or simulated
  peer review (use mock-review).
---

# Paper Reading

Paper request: `$ARGUMENTS`

This skill produces a deep, critical, structured reading note for a single research paper. The note follows a fixed 9-section template, embeds cropped figures from the paper, cites every claim with a numbered reference, and links only to external sources. The final note is written in the same language the user used to invoke the skill unless the user explicitly asks for another language.

## Core Boundary

This skill is a personal reading note tool, not a peer review, not a survey, not a quick lookup.

Rules:

- Read the **whole paper**, including appendices. A skim of abstract plus experiments is not a reading.
- Be **objective and critical**. Quote the paper, do not advertise it. Words like "groundbreaking", "novel", "amazing", "revolutionary" require verifiable evidence and are usually wrong.
- **Every claim must be traceable**: cite the section, figure, or table. Every cited paper must have been re-fetched and read in original, not relied on from a secondary summary.
- **Crop figures, do not paste whole pages**. A figure that occupies half a page and is mostly whitespace or another figure is not informative. Crop further to the region that carries the argument.
- **Numbered citations** `[1]`, `[2]`, etc. The reference list at the end of the note contains only external links (arXiv, DOI, publisher page). No local file paths in the reference list.
- **All downloaded papers live in the project that triggered the skill**, never inside this skill's folder. The skill folder is meant to be reusable across projects.
- **The final note is in the user's language**. Chinese question -> Chinese note. English question -> English note. Explicit specification -> that specification.

## Required Resources

Read these bundled files in this order, before drafting the final note:

- `references/note-template.md` - 9-section reading note structure
- `references/benchmark-guard.md` - how to verify that each benchmark actually tests what the paper claims
- `references/related-work-schema.md` - columns to use in `related_work_matrix.md`
- `references/critical-reading-checklist.md` - objective and critical reading rules
- `references/output-contract.md` - non-negotiable output rules: citation style, figure policy, anti-patterns, self-check

Use scripts when available. Each script is self-contained and prints usage on `--help`:

- `scripts/extract_text.py` - extract structured text from the PDF, with `=== PAGE N ===` markers
- `scripts/split_sections.py` - heuristic section splitter, writes `sections.json`
- `scripts/render_pages.py` - render each PDF page to a PNG, writes `pages.json` sidecar with the actual page-number width
- `scripts/locate_figures.py` - find figure captions and crop the figure body from the rendered page

For page rendering, `render_pages.py` can also delegate to the `pdf` skill's converter script if that skill is installed alongside this one. In the standard skills-root layout, the delegate path is `../pdf/scripts/convert_pdf_to_images.py` relative to this skill directory. If the installation layout differs, resolve the installed `pdf` skill directory first and pass its `scripts/convert_pdf_to_images.py` path to `--delegate`.

## Working Directory Contract

All output lives **in the project that triggered the skill**, not in the skill folder. Output is split into two locations: **human deliverable** (the final reading note) and **agent scratch** (intermediate artifacts). Humans look at the first, the agent owns the second.

### Project paper directory (REQUIRED)

Before downloading any PDF, resolve the project paper directory in this order:

1. If the user names a path (for example "save to `references/papers/`" or "save to my project's paper drive"), use that path verbatim.
2. Else, probe the current working directory for an existing paper directory in this order and use the first match:
   - `papers/`
   - `references/papers/`
   - `docs/papers/`
3. Else, create `<cwd>/papers/` and use it.

Record the resolved path in Phase 2 when filling `benchmark_audit.md` (each row has a `local_path` column). Never write PDFs into the skill folder.

### Working layout

```
<project_root>/
├── papers/                              <- resolved project paper directory
│   └── <author>__<year>__<slug>.pdf
├── readings/<paper-slug>/               <- HUMAN DELIVERABLE (visible to user)
│   ├── paper_note.md
│   └── figures/
│       └── figure_N.png
└── x_temp/paper-reading/<paper-slug>/   <- AGENT SCRATCH (intermediate only)
    ├── pages/                           <- page_NN.png from render_pages.py
    │   └── pages.json                   <- width sidecar (consumed by locate_figures.py)
    ├── figures/                         <- scratch cropped figure_N.png + figure_N.meta.json
    ├── text/
    │   ├── full.txt                     <- extract_text.py output
    │   └── sections.json                <- split_sections.py output
    ├── benchmark_audit.md               <- Phase 2 output
    └── related_work_matrix.md           <- Phase 3 output
```

The `paper-slug` is a filesystem-safe identifier derived from the paper title. Lowercase, alphanumerics and hyphens only.

### Where the final note lives

The final `paper_note.md` lives in `<project_root>/readings/<slug>/`, **not** in `x_temp/`. `x_temp/` is agent scratch space; humans do not look there. After Phase 5 synthesis, the agent must write `paper_note.md` to `readings/<slug>/`. Any cropped figures referenced by the final note must be copied into `readings/<slug>/figures/` so the note stays self-contained. The audit (`benchmark_audit.md`) and matrix (`related_work_matrix.md`) stay in `x_temp/paper-reading/<slug>/` because they are intermediate artifacts. Create the `readings/<slug>/` and `readings/<slug>/figures/` directories if they do not exist.

If `<project_root>/readings/` already exists with prior notes, append to it. If the user names a different "human deliverable" path, use that path verbatim and skip the `readings/` default.

## Workflow

The workflow is five sequential phases. Do not skip phases. Do not run phases in parallel: each later phase depends on output from the earlier ones.

### Phase 1: Skim and frame the problem

Goal: in plain words, what problem is this paper solving, and what is the problem class it belongs to?

1. Run `extract_text.py <paper.pdf> --output <working>/text/` to produce `text/full.txt` and `text/pages.json`.
2. Run `split_sections.py <working>/text/` to produce `text/sections.json`.
3. Read in this order: abstract, introduction, related work, experiments.
4. Write a 1-paragraph "what is this paper about" and a 3-5 bullet list of the paper's claimed contributions. These are intermediate notes; they feed into Phase 5.
5. **Do not yet download benchmark or prior-art papers. Do not yet crop figures.** This sub-step is for framing only.
6. **Read 2 foundational works to understand the problem class.** Pick from the target paper's related work: one paper that defines the problem class the target paper belongs to (for example, for a VLA paper, RT-2 or OpenVLA), and one that introduces a key dataset or benchmark the target paper uses. Read abstract and introduction only — not the full paper. These two reads are what make §3 of the final note informative; without them, the agent can only paraphrase the target paper's introduction and the note's "what is this problem" section becomes empty.

### Phase 2: Benchmark audit

Goal: verify that every benchmark the paper uses actually tests what the paper claims it tests. This guards against the common failure mode where a benchmark designed for task A is borrowed by a paper on task B without explanation.

For each benchmark named in the experiments section:

1. Find or download the benchmark's original paper into the resolved project paper directory.
2. Read the original paper's abstract, introduction, and task definition section. Skim the rest.
3. Fill one row in `benchmark_audit.md` using the schema in `references/benchmark-guard.md`.
4. If a benchmark's original purpose and the way the paper uses it are mismatched, mark the row with `mismatch: yes` and note the original task vs the paper's task in the cell.
5. Do not silently accept the paper's framing. If the paper says "we use X for Y" but X was designed for Z, the note must say so.

A benchmark-mismatch warning must appear in `paper_note.md` section 7 if any row is flagged. See `references/benchmark-guard.md` for the full audit schema and worked examples.

### Phase 3: Prior art and classic works

Goal: understand the lineage of ideas and identify the most classic prior work in the subfield.

1. From the introduction's related work and the experiments' comparison tables, extract the set of papers the target paper directly compares against. **Cap at 15 papers** total for this phase. If the paper cites more, pick the 15 that are most central to the paper's claim. (A minimum of 5 keeps the matrix representative; fewer than 5 means the target paper has almost no direct baselines and the matrix will be thin.)
2. Identify the 1-3 "most classic" works in this subfield (often older, highly-cited, foundational). These may or may not be in the comparison set; include them anyway.
3. Download each into the project paper directory. Prefer, in order: arXiv, publisher OA, OpenReview, author website, project page. Do not bypass paywalls.
4. For each, read abstract, introduction, and experiments. Do not read the full paper. The goal is to understand: what problem, what method, what result, why it matters in the lineage.
5. Save one row per paper to `related_work_matrix.md` using the columns defined in `references/related-work-schema.md`.

### Phase 4: Deep read and figure capture

Goal: now that benchmarks and prior art are understood, re-read the entire paper carefully and capture every key figure as a cropped image.

1. Run `render_pages.py <paper.pdf> --output <working>/pages/` to produce `pages/page_NN.png` and `pages/pages.json` (the sidecar that records the actual page-number width). Use `--dpi 150` as a sensible default; bump to 300 if figure text is too small.
2. Re-read the paper from start to finish: method, experiments, limitations, conclusion, **appendix**. Earlier reading of benchmarks and prior art makes this re-read substantively deeper than the first skim.
3. For each `Figure N`, `Table N`, or other visually informative element that the note will reference, run `locate_figures.py <paper.pdf> --text-dir <working>/text/ --pages-dir <working>/pages/ --output <working>/figures/ --figure N` to produce `figures/figure_N.png` plus `figures/figure_N.meta.json`.
4. **Visually QA every cropped figure immediately.** Open the PNG and confirm:
   - The crop contains the figure body, not just the caption or whitespace.
   - The crop is not clipped at top, bottom, or sides.
   - The figure is readable at note-zoom (text inside the figure is legible).
5. If a crop is bad, retry with `--bbox "x,y,w,h"` to specify the crop region manually in PNG pixels. Do not embed a broken figure into the note.

### Phase 5: Synthesize the final note

Goal: produce a single `paper_note.md` that any reader (including the user, six months from now) can use to recall the paper's contribution and the reading session's verdict.

1. Open `references/note-template.md` and follow the 9-section structure verbatim. Section order is fixed.
2. Use **numbered citations** `[1]`, `[2]`, ... everywhere a paper, book, or report is referenced. Put the reference list at the end of the note; the list contains only external URLs.
3. Copy every figure that the final note embeds from `<working>/figures/` into `<project_root>/readings/<slug>/figures/`, then **insert the copied cropped figures** in the section that references them, with `![Figure N: <caption summary>](figures/figure_N.png)`. Never link to a whole-page render. Never point the final note at `x_temp/`.
4. Apply the rules in `references/output-contract.md` strictly: numbered citations only, external links only in the reference list, no anachronistic critique, no "rather than" sentence pattern, no process narration in the final note.
5. Apply the rules in `references/critical-reading-checklist.md`: every claim cites a section, figure, or table; numbers carry units and sample sizes; overclaims are flagged in-line; unevaluated scenarios are noted.
6. **Write the final note in the user's language.** If the user asked in Chinese, write Chinese. If in English, write English. The template's section labels can be translated. If the user explicitly specifies a language, use that.
7. Before declaring done, run the self-check in `references/output-contract.md`. If any item fails, fix and re-run.

## Critical Reading Rules

Read `references/critical-reading-checklist.md` for the full set. The most important rule in one line:

**Authors claim X. Evidence is at section Y / figure Z. Evidence supports claim: yes / no / partial. State the verdict in the note.**

Never write a claim without a citation. Never write a number without units and sample size. Never write a critique from a later vocabulary that the early work could not have used. Flag every benchmark that the paper borrows from a mismatched original purpose.

## Failure Handling

- PDF text extraction fails -> fall back to OCR via `pdftoppm` + `tesseract` if available, otherwise ask the user for a text version.
- Benchmark original paper cannot be legally obtained -> record the URL and the source gap in `benchmark_audit.md`; do not silently treat absence as confirmation.
- arXiv download fails -> try the publisher's HTML page, OpenReview, or the author's homepage. If none works, record the failure and continue.
- Figure auto-crop is wrong after one attempt -> re-run `locate_figures.py` with `--bbox "x,y,w,h"` to specify the crop manually in PNG pixels. Do not embed a broken figure.
- A cited paper's external link is dead -> replace with the closest equivalent URL (publisher page, DOI resolver, arXiv abstract page) and note the change in the reference list.
- The user's request is ambiguous about which paper -> ask one concise question before downloading anything.
- The paper is in a language the user did not specify -> default to writing the note in that paper's language only if the user agrees.
