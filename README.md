# my_codex_skills

English | [Chinese](./README.zh-CN.md)

Personal Codex skills for reusable research, writing, document-production, and project-navigation workflows.

Each skill in this repository is a top-level directory. A valid skill directory contains `SKILL.md` at its root and may also include `agents/`, `scripts/`, `references/`, or `assets/`.

Unless a skill explicitly says otherwise, these skills are designed for standalone Codex use: bundled local scripts, local files, and normal public web access are part of the expected path; hidden reviewer chains, notification hooks, and implicit cross-skill orchestration are not.

## Skills

| Skill | Summary | Typical use |
| --- | --- | --- |
| [`alphaxiv`](./alphaxiv/) | Quick single-paper lookup using AlphaXiv first, with fallback to source material when needed. | Explaining one arXiv paper from an ID or URL without running a broad literature survey. |
| [`arxiv`](./arxiv/) | Search arXiv, fetch metadata, and download paper PDFs into a local library. | Finding preprints, downloading PDFs by query or arXiv ID, and building local paper collections. |
| [`doc-coauthoring`](./doc-coauthoring/) | Structured co-authoring workflow for specs, proposals, PRDs, RFCs, and decision documents. | Planning, drafting, and iterating on long-form collaborative documents. |
| [`docx`](./docx/) | Create, inspect, and edit Word documents, including tracked changes and comments. | Word editing, redlining, commenting, and OOXML-aware document workflows. |
| [`drawio-diagram`](./drawio-diagram/) | Build editable draw.io research figures and export PNG, SVG, and PDF with visual QA. | Paper figures, posters, and concept diagrams that must remain editable in draw.io. |
| [`figure-description`](./figure-description/) | Generate patent-style figure descriptions and reference-numeral mappings from local figures. | Preparing CN/US/EP patent drawing descriptions from technical figures. |
| [`formula-derivation`](./formula-derivation/) | Structure and derive research formulas from assumptions and problem statements. | Turning theory notes into a paper-ready derivation skeleton or blocker report. |
| [`grant-proposal`](./grant-proposal/) | Draft structured grant proposals from research ideas and literature context. | Turning a research direction into a funding application with agency-specific structure. |
| [`mmx-cli`](./mmx-cli/) | Operate the local MiniMax CLI for text, search, vision, quota, and media tasks. | Running MiniMax-specific workflows through a configured local `mmx` command. |
| [`mock-review`](./mock-review/) | Run a simulated reviewer-style critique of a manuscript before submission. | Pre-submission risk review, rebuttal preparation, and reviewer-style paper critique. |
| [`novelty-check`](./novelty-check/) | Check whether a research idea appears novel against nearby prior work. | Screening an idea for prior-art overlap before investing implementation time. |
| [`pdf`](./pdf/) | Read, extract, fill, edit, and generate PDFs, including form workflows. | PDF extraction, form handling, annotation, and validation-heavy PDF tasks. |
| [`phd-benchmark-paper-template`](./phd-benchmark-paper-template/) | Structure benchmark and evaluation papers around the five-pillar framework. | Planning benchmark or evaluation papers, their Introduction logic, pipeline, and experiments. |
| [`phd-figure-designer`](./phd-figure-designer/) | Design and audit the core figures in a technical paper. | Deciding paradigms, layouts, labels, and QA rules for paper figures. |
| [`phd-idea-evaluator`](./phd-idea-evaluator/) | Evaluate research ideas for strength, feasibility, and lifecycle fit. | Stress-testing a paper idea before implementation or writing begins. |
| [`phd-intro-drafter`](./phd-intro-drafter/) | Build a six-paragraph Introduction outline for a technical paper. | Structuring the paper story before writing Introduction prose. |
| [`phd-pre-submission-reviewer`](./phd-pre-submission-reviewer/) | Run a pre-submission audit across logic, writing, grammar, LaTeX, and figures. | Final manuscript audit before submission. |
| [`phd-tech-paper-template`](./phd-tech-paper-template/) | Build the logic skeleton and consistency checks for a technical paper. | Planning technical papers before drafting, especially advisor-student brainstorming. |
| [`phd-vibe-research-workflow`](./phd-vibe-research-workflow/) | Plan AI-assisted research sessions while keeping academic judgment with the user. | Organizing coding, figure, and writing sessions under explicit research-integrity rules. |
| [`pptx`](./pptx/) | Create, inspect, and edit PowerPoint decks with a required QA loop. | Slide creation and repair workflows that need artifact validation. |
| [`proof-writer`](./proof-writer/) | Turn theorem and lemma sketches into rigorous proof drafts. | Converting rough proof ideas into a defensible proof package. |
| [`research-lit`](./research-lit/) | Run a standalone literature review across local PDFs, the public web, and arXiv metadata. | Finding related work, mapping a field, and comparing nearby paper clusters. |
| [`research-survey-loop`](./research-survey-loop/) | Maintain a long-running survey task with stable task files and iterative Chinese writing. | Sustained literature surveys that evolve across multiple rounds. |
| [`research-wiki`](./research-wiki/) | Build a persistent project research wiki for papers, ideas, experiments, and claims. | Maintaining reusable project memory across sessions. |
| [`theme-factory`](./theme-factory/) | Apply bundled visual themes or derive new ones for slides, docs, and lightweight artifacts. | Reusing or deriving consistent visual themes for presentation-style outputs. |
| [`update-source-map`](./update-source-map/) | Build or refresh a structured source map for an unfamiliar workspace. | Creating or updating an agent-readable project index before deeper work. |
| [`xlsx`](./xlsx/) | Create, repair, analyze, and extend spreadsheet files while preserving formulas and structure. | Spreadsheet editing, recalculation, and workbook-preserving automation. |

## Install

Each top-level skill directory can be installed directly into `$CODEX_HOME/skills`.

```text
source: <this-repo>/<skill>/
target: $CODEX_HOME/skills/<skill>/
copy the directory as-is
```

If you want the full collection, repeat the same copy rule for every top-level skill directory listed above.

After installing or updating skills, restart Codex so the refreshed metadata is loaded.

## Notes

- These skills encode personal research workflows and do not represent official processes of any venue, journal, or institution.
- The `phd-` prefix is used to namespace a set of paper-writing and research-planning skills in this repository.
- Unless a specific skill says otherwise, these skills assume standalone Codex use with local scripts, local files, and normal web access.
- Some skills depend on local tools such as LibreOffice, Poppler, `pandoc`, `markitdown`, `mmx`, or language runtimes described inside the skill folder.
- Outputs from review-style skills such as `mock-review` are simulated feedback, not official reviewer reports.
- For details about a specific skill, read that skill's `SKILL.md` and bundled references.
