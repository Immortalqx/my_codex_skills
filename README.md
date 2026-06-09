# my_codex_skills

English | [中文](./README.zh-CN.md)

This repository collects my personal Codex skills for reusable research workflows.

Each top-level skill folder keeps its own README files and contains an installable skill directory with `SKILL.md`.

The `mmx-cli` skill is kept as an exact upstream MiniMax CLI skill copy, with repository README files wrapped around it for this collection.

## Skills

| Skill | Summary | Typical Use | Installable Directory |
| --- | --- | --- | --- |
| [`arxiv`](./arxiv/) | Search arXiv, fetch metadata for specific arXiv IDs, and download paper PDFs into local paper libraries using the bundled arXiv Atom API helper. | Finding preprints, downloading arXiv PDFs by query or ID, and building local `papers/` or `literature/` collections. | [`arxiv/arxiv`](./arxiv/arxiv/) |
| [`drawio-diagram`](./drawio-diagram/) | Draw.io research-figure workflow that builds an editable draw.io draft, reuses source paper/poster assets when available, exports PNG/SVG/PDF, and runs visual QA on the exported PNG until the QA checklist passes. | Paper figures, posters, slide visuals, and concept diagrams that need an editable draw.io artifact the user can keep refining directly in draw.io. | [`drawio-diagram/drawio-diagram`](./drawio-diagram/drawio-diagram/) |
| [`help-me-read`](./help-me-read/) | Deep-read a user-provided PDF and produce a story-driven close-read note with page screenshots, figure explanations, background context, and a versioned output file. | When the user wants detailed study notes, a tutor-style breakdown, or a close read of a lecture deck or academic paper. | [`help-me-read/help-me-read`](./help-me-read/help-me-read/) |
| [`mmx-cli`](./mmx-cli/) | Official MiniMax CLI skill for using the local `mmx` command to generate text, images, video, speech, and music, perform web search and vision understanding, query quotas, manage files, and export command schemas. The inner `SKILL.md` is kept as an exact upstream copy. | When Codex should operate through a configured local MiniMax CLI, especially with `--dry-run`, `--quiet`, `--output json`, and `--non-interactive` for token-conscious checks. | [`mmx-cli/mmx-cli`](./mmx-cli/mmx-cli/) |
| [`mock-review`](./mock-review/) | Mock peer-review workflow for manuscript authors. It researches venue or journal requirements, inspects manuscript PDFs, studies related literature and experimental baselines, and writes a simulated review for rebuttal preparation and paper improvement. | Pre-submission risk check, rebuttal preparation, reviewer-style critique before revising a manuscript. | [`mock-review/mock-review`](./mock-review/mock-review/) |
| [`research-survey-loop`](./research-survey-loop/) | Long-running literature survey workflow. It creates or resumes survey tasks, maintains stable task documents, searches prioritized sources, migrates local PDFs, reads papers in chunks, and incrementally writes a Chinese survey. | Sustained literature surveys for robotics, embodied AI, computer vision, world models, navigation, manipulation, 3D perception, and adjacent topics. | [`research-survey-loop/research-survey-loop`](./research-survey-loop/research-survey-loop/) |
| [`update-source-map`](./update-source-map/) | Create or update an agent-readable source map (Markdown + JSON) for any project directory. It auto-detects whether to build a new map or refresh an existing one, and preserves hand-curated per-file summaries across regenerations. | When starting work in a new / unfamiliar workspace, refreshing a stale index after files change, or handing a project over to another agent. | [`update-source-map/update-source-map`](./update-source-map/update-source-map/) |

## Install

The installable unit of each skill is the nested `<skill>/<skill>/` directory inside this repo. The outer `<skill>/README.md` and `<skill>/README.zh-CN.md` are repository docs only and must not be installed into the Codex skills directory.

Ask Codex to install the skills. The only rule this repo needs to specify is the source/target layout; Codex can choose the platform-specific install operation itself.

```text
Use $skill-installer to install the following skills from this repo into the local Codex skills directory.

For each <skill> below:
  - source: <this-repo>/<skill>/<skill>/
  - target:$CODEX_HOME/skills/<skill>/
  - copy the contents flat (not the outer folder)
  - skip any __pycache__ directory

Skills to install: arxiv, drawio-diagram, help-me-read, mmx-cli, mock-review, research-survey-loop, update-source-map.
```

If you install only one skill, keep the same folder rule and shorten the skill list. Do not install the outer `<skill>/` folder, because that would copy the bilingual README files into the installed skill.

## Notes

- These skills encode personal research workflows and do not represent official processes of any venue, journal, or institution.
- `mmx-cli` requires a configured local `mmx` command; use `--dry-run`, `--quiet`, `--output json`, and `--non-interactive` for token-conscious agent checks.
- `drawio-diagram` is intended for editable figure workflows; it produces a `.drawio` plus PNG/SVG/PDF exports and only declares the figure ready after the visual QA loop passes.
- Outputs from `mock-review` should be clearly labeled as simulated/mock reviews. They must not replace real peer review or impersonate official reviewer reports.
- Literature retrieval should prioritize legally accessible sources such as official open-access pages, arXiv, OpenReview, and author pages.
- For details about a specific skill, read the README files inside that skill folder.
