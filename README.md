# my_codex_skills

English | [Chinese](./README.zh-CN.md)

Personal Codex skills for reusable research and writing workflows.

Each skill is a top-level directory. A valid skill directory contains `SKILL.md`
at its root and may also include `agents/`, `scripts/`, `references/`, or
`assets/`. There is no nested installable directory and no per-skill README in
this repository.

Unless a skill explicitly says otherwise, these skills are designed for
standalone, single-agent use: bundled local scripts, local files, and public web
access are normal; notification hooks, reviewer-agent chains, and hidden
cross-skill hooks are not part of the default path.

## Skills

| Skill | Summary | Typical use |
| --- | --- | --- |
| [`alphaxiv`](./alphaxiv/) | Quick single-paper lookup using public AlphaXiv Markdown first, with AlphaXiv Markdown and arXiv LaTeX source fallback when needed. | Explaining one arXiv paper from an ID or URL without running a broad literature survey. |
| [`arxiv`](./arxiv/) | Search arXiv, fetch metadata for specific arXiv IDs, and download PDFs into local paper libraries using the bundled arXiv Atom API helper. | Finding preprints, downloading arXiv PDFs by query or ID, and building local `papers/` or `literature/` collections. |
| [`drawio-diagram`](./drawio-diagram/) | Draw.io research-figure workflow that builds an editable `.drawio` draft, exports PNG/SVG/PDF, and runs visual QA on the exported PNG. | Paper figures, posters, slide visuals, and concept diagrams that need an editable draw.io artifact. |
| [`figure-description`](./figure-description/) | Patent figure workflow that identifies components, assigns reference numerals, and generates formal drawing descriptions. | Preparing CN/US/EP patent drawing descriptions and reference numeral indexes from local technical figures. |
| [`formula-derivation`](./formula-derivation/) | Research-formula derivation workflow that clarifies assumptions and separates identities, propositions, approximations, and interpretations. | Turning messy theory notes into an internal derivation note, paper-style theory draft, or blocker report. |
| [`grant-proposal`](./grant-proposal/) | Structured grant-proposal drafting from research ideas and literature, with agency-specific and generic formats. | Turning a research direction into a funding application with aims, milestones, feasibility, and outputs. |
| [`help-me-read`](./help-me-read/) | Deep-read a user-provided PDF and produce a story-driven close-read note with page screenshots, figure explanations, and background context. | Detailed study notes, tutor-style breakdowns, or close reads of lecture decks and academic papers. |
| [`mmx-cli`](./mmx-cli/) | MiniMax CLI skill for operating the local `mmx` command for text, search, vision, quota, file, and media tasks. | When Codex should use an installed local MiniMax CLI directly, especially for bilingual multi-query search and non-interactive JSON workflows. |
| [`mock-review`](./mock-review/) | Mock peer-review workflow for manuscript authors that studies venue requirements, inspects PDFs, researches related work, and writes simulated reviews. | Pre-submission risk checks, rebuttal preparation, and reviewer-style critique before revising a manuscript. |
| [`novelty-check`](./novelty-check/) | Research-idea novelty checker that extracts core claims, searches literature, compares closest prior work, and reports novelty risk. | Checking whether a method appears to have already been done before investing implementation time. |
| [`proof-writer`](./proof-writer/) | Rigorous proof-writing workflow for theorem, lemma, proposition, and corollary statements. | Turning a rough mathematical claim or proof sketch into a defensible proof package. |
| [`research-lit`](./research-lit/) | Standalone literature-review workflow across local PDFs, public web search, and structured arXiv metadata. | Finding related work, mapping a paper landscape, and comparing paper clusters around a research topic. |
| [`research-survey-loop`](./research-survey-loop/) | Long-running literature survey workflow that maintains stable task documents, searches prioritized sources, reads papers in chunks, and incrementally writes a Chinese survey. | Sustained literature surveys for robotics, embodied AI, computer vision, world models, navigation, manipulation, 3D perception, and adjacent topics. |
| [`research-wiki`](./research-wiki/) | Persistent project-level research knowledge base for papers, ideas, experiments, claims, and typed relationships. | Building reusable project memory instead of rediscovering the same field map in every session. |
| [`update-source-map`](./update-source-map/) | Create or update an agent-readable source map for any project directory while preserving hand-curated per-file summaries across regenerations. | Starting work in an unfamiliar workspace, refreshing a stale index, or handing a project to another agent. |

## Install

The installable unit is each top-level skill directory itself:

```text
source: <this-repo>/<skill>/
target: $CODEX_HOME/skills/<skill>/
copy the directory contents as-is
skip any __pycache__ directory
```

To install every skill from this repository, copy these directories into the
local Codex skills directory:

```text
alphaxiv, arxiv, drawio-diagram, figure-description, formula-derivation,
grant-proposal, help-me-read, mmx-cli, mock-review, novelty-check,
proof-writer, research-lit, research-survey-loop, research-wiki,
update-source-map
```

Do not install repository utility folders such as `scripts/`.

After installing or updating local skills, restart Codex so the new skill
metadata is picked up.

## Notes

- These skills encode personal research workflows and do not represent official
  processes of any venue, journal, or institution.
- `mmx-cli` requires a configured local `mmx` command.
- `drawio-diagram` is intended for editable figure workflows and declares a
  figure ready only after the visual QA loop passes.
- Outputs from `mock-review` should be clearly labeled as simulated/mock reviews
  and must not impersonate official reviewer reports.
- Literature retrieval should prioritize legally accessible sources such as
  official open-access pages, arXiv, OpenReview, and author pages.
