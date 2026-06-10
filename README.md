# my_codex_skills

English | [Chinese](./README.zh-CN.md)

Personal Codex skills for research, writing, document production, and project navigation workflows.

Each top-level directory in this repository is an installable skill. A valid skill directory contains `SKILL.md` at the root and may also include `agents/`, `scripts/`, `references/`, or `assets/`.

## Skill List

- [`alphaxiv`](./alphaxiv/) - Quick single-paper lookup using AlphaXiv first, with fallback to source material when needed.
- [`arxiv`](./arxiv/) - Search arXiv, fetch metadata, and download paper PDFs into a local library.
- [`doc-coauthoring`](./doc-coauthoring/) - Structured co-authoring workflow for specs, proposals, PRDs, RFCs, and decision docs.
- [`docx`](./docx/) - Create, inspect, and edit Word documents, including tracked changes and comments.
- [`drawio-diagram`](./drawio-diagram/) - Build editable draw.io research figures and export PNG, SVG, and PDF with visual QA.
- [`figure-description`](./figure-description/) - Generate patent-style figure descriptions and reference-numeral mappings from local figures.
- [`formula-derivation`](./formula-derivation/) - Structure and derive research formulas from assumptions and problem statements.
- [`grant-proposal`](./grant-proposal/) - Draft structured grant proposals from research ideas and literature context.
- [`help-me-read`](./help-me-read/) - Deep-read a user-provided PDF and produce a story-driven study note.
- [`mmx-cli`](./mmx-cli/) - Operate the local MiniMax CLI for text, search, vision, quota, and media tasks.
- [`mock-review`](./mock-review/) - Run a simulated reviewer-style critique of a manuscript before submission.
- [`novelty-check`](./novelty-check/) - Check whether a research idea appears novel against nearby prior work.
- [`pdf`](./pdf/) - Read, extract, fill, edit, and generate PDFs, including form workflows.
- [`phd-benchmark-paper-template`](./phd-benchmark-paper-template/) - Structure benchmark and evaluation papers around the five-pillar framework.
- [`phd-figure-designer`](./phd-figure-designer/) - Design and audit the core figures in a technical paper.
- [`phd-idea-evaluator`](./phd-idea-evaluator/) - Evaluate research ideas for strength, feasibility, and lifecycle fit.
- [`phd-intro-drafter`](./phd-intro-drafter/) - Build a six-paragraph Introduction outline for a technical paper.
- [`phd-pre-submission-reviewer`](./phd-pre-submission-reviewer/) - Run a pre-submission audit across logic, writing, grammar, LaTeX, and figures.
- [`phd-tech-paper-template`](./phd-tech-paper-template/) - Build the logic skeleton and consistency checks for a technical paper.
- [`phd-vibe-research-workflow`](./phd-vibe-research-workflow/) - Plan AI-assisted research sessions while keeping academic judgment with the user.
- [`pptx`](./pptx/) - Create, inspect, and edit PowerPoint decks with a required QA loop.
- [`proof-writer`](./proof-writer/) - Turn theorem and lemma sketches into rigorous proof drafts.
- [`research-lit`](./research-lit/) - Run a standalone literature review across local PDFs, the public web, and arXiv metadata.
- [`research-survey-loop`](./research-survey-loop/) - Maintain a long-running survey task with stable task files and iterative Chinese writing.
- [`research-wiki`](./research-wiki/) - Build a persistent project research wiki for papers, ideas, experiments, and claims.
- [`theme-factory`](./theme-factory/) - Apply bundled visual themes or derive new ones for slides, docs, and lightweight artifacts.
- [`update-source-map`](./update-source-map/) - Build or refresh a structured source map for an unfamiliar workspace.
- [`xlsx`](./xlsx/) - Create, repair, analyze, and extend spreadsheet files while preserving formulas and structure.

## Install

Copy each top-level skill directory directly into `$CODEX_HOME/skills`:

```text
source: <this-repo>/<skill>/
target: $CODEX_HOME/skills/<skill>/
copy the directory contents as-is
skip any __pycache__ directory
```

Do not install repository utility folders such as `temp/`.

After installing or updating skills, restart Codex so the refreshed metadata is loaded.

## Notes

- The `phd-` prefix is used to namespace imported paper-writing and research-planning skills.
- These skills are designed for standalone Codex use with local scripts, local files, and normal web access.
- Some skills depend on local tools such as LibreOffice, Poppler, `pandoc`, `markitdown`, `mmx`, or language runtimes already described inside each skill.
- Outputs from review-style skills such as `mock-review` remain simulated feedback, not official reviewer reports.
