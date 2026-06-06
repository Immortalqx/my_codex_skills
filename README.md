# my_codex_skills

English | [中文](./README.zh-CN.md)

This repository collects my personal Codex skills for reusable research workflows.

Each top-level skill folder keeps its own README files and contains an installable skill directory with `SKILL.md`.

Two of the skills in this repository are specifically tuned for **MiniMax M3 used inside Codex Desktop App**:

- `minimax-task-preflight`: clarify a raw user request and rewrite it into a clearer prompt without pre-planning execution
- `minimax-thorough-execution`: execute the user's prompt strictly, with explicit anti-shortcut, source-map, and completion-audit rules

## Skills

| Skill | Summary | Typical Use | Installable Directory |
| --- | --- | --- | --- |
| [`drawio-diagram`](./drawio-diagram/) | Draw.io research-figure workflow that builds an editable draw.io draft, reuses source paper/poster assets when available, exports PNG/SVG/PDF, and runs visual QA on the exported PNG until the QA checklist passes. | Paper figures, posters, slide visuals, and concept diagrams that need an editable draw.io artifact the user can keep refining directly in draw.io. | [`drawio-diagram/drawio-diagram`](./drawio-diagram/drawio-diagram/) |
| [`minimax-task-preflight`](./minimax-task-preflight/) | Prompt-clarification preflight tuned for MiniMax M3 in Codex Desktop App. It reads a raw request, asks only the necessary follow-up questions, and rewrites the request into a clearer prompt without drifting into planning or deliverable design. | Before running MiniMax M3 on ambiguous or underspecified tasks where prompt clarity matters more than early planning. | [`minimax-task-preflight/minimax-task-preflight`](./minimax-task-preflight/minimax-task-preflight/) |
| [`minimax-thorough-execution`](./minimax-thorough-execution/) | Strict-execution protocol tuned for MiniMax M3 in Codex Desktop App. It forbids prompt rewriting during execution, prevents token-saving scope shrinkage, requires real visual inspection for screenshot/page tasks, requires source links for search-backed claims, maintains source maps, and appends a short completion audit. | When the main risks are prompt rewriting, laziness, skipped appendix/supplement, shallow search, image avoidance, or missing source grounding. | [`minimax-thorough-execution/minimax-thorough-execution`](./minimax-thorough-execution/minimax-thorough-execution/) |
| [`mock-review`](./mock-review/) | Mock peer-review workflow for manuscript authors. It researches venue or journal requirements, inspects manuscript PDFs, studies related literature and experimental baselines, and writes a simulated review for rebuttal preparation and paper improvement. | Pre-submission risk check, rebuttal preparation, reviewer-style critique before revising a manuscript. | [`mock-review/mock-review`](./mock-review/mock-review/) |
| [`research-survey-loop`](./research-survey-loop/) | Long-running literature survey workflow. It creates or resumes survey tasks, maintains stable task documents, searches prioritized sources, migrates local PDFs, reads papers in chunks, and incrementally writes a Chinese survey. | Sustained literature surveys for robotics, embodied AI, computer vision, world models, navigation, manipulation, 3D perception, and adjacent topics. | [`research-survey-loop/research-survey-loop`](./research-survey-loop/research-survey-loop/) |

## Install

Copy the installable skill directory into your Codex skills directory.

```powershell
# Install drawio-diagram
Copy-Item -Recurse -Force .\drawio-diagram\drawio-diagram "$env:USERPROFILE\.codex\skills\drawio-diagram"

# Install minimax-task-preflight
Copy-Item -Recurse -Force .\minimax-task-preflight\minimax-task-preflight "$env:USERPROFILE\.codex\skills\minimax-task-preflight"

# Install minimax-thorough-execution
Copy-Item -Recurse -Force .\minimax-thorough-execution\minimax-thorough-execution "$env:USERPROFILE\.codex\skills\minimax-thorough-execution"

# Install mock-review
Copy-Item -Recurse -Force .\mock-review\mock-review "$env:USERPROFILE\.codex\skills\mock-review"

# Install research-survey-loop
Copy-Item -Recurse -Force .\research-survey-loop\research-survey-loop "$env:USERPROFILE\.codex\skills\research-survey-loop"
```

If `CODEX_HOME` is configured, copy the folders into `$env:CODEX_HOME\skills\` instead.

## Notes

- These skills encode personal research workflows and do not represent official processes of any venue, journal, or institution.
- `minimax-task-preflight` and `minimax-thorough-execution` are tuned for **MiniMax M3 in Codex Desktop App**. They are intended to improve prompt clarity and execution thoroughness for that setup rather than serve as general-purpose skills for every model.
- `drawio-diagram` is intended for editable figure workflows; it produces a `.drawio` plus PNG/SVG/PDF exports and only declares the figure ready after the visual QA loop passes.
- Outputs from `mock-review` should be clearly labeled as simulated/mock reviews. They must not replace real peer review or impersonate official reviewer reports.
- Literature retrieval should prioritize legally accessible sources such as official open-access pages, arXiv, OpenReview, and author pages.
- For details about a specific skill, read the README files inside that skill folder.