# my_codex_skills

English | [中文](./README.zh-CN.md)

This repository collects my personal Codex skills for reusable research workflows.

Each top-level skill folder keeps its own README files and contains an installable skill directory with `SKILL.md`.

Several skills in this repository are specifically tuned for **MiniMax M3 used inside Codex Desktop App**:

- `minimax-task-preflight`: clarify a raw user request and rewrite it into a clearer prompt without pre-planning execution
- `minimax-thorough-execution`: execute the user's prompt strictly, with explicit anti-shortcut, source-map, and completion-audit rules
- `minimax-web-search`: web search via the upstream `minimax-coding-plan-mcp` `web_search` tool, using the user's MiniMax token-plan key — bypasses Codex 0.137.0's broken MCP integration (openai/codex#23186)
- `minimax-image-understand`: image understanding (describe / analyze / OCR) via the upstream `minimax-coding-plan-mcp` `understand_image` tool, using the user's MiniMax token-plan key — same MCP workaround

The two `minimax-web-search` / `minimax-image-understand` skills are siblings:
they are **fully independent** (each ships its own `lib_key.py` + `mcp_client.py`),
so you can install one without the other. They both call the official upstream
MCP server via JSON-RPC, so the results match what the upstream tool produces
exactly — no API translation layer in between.

Both MiniMax MCP wrapper scripts are **stdout-only** for task results. They do
not write search results, image-understanding results, logs, debug JSON, or
business cache files to disk. If `--print` is used, the full JSON-RPC response
is printed to stdout for Codex to read, not saved locally. Normal runtime caches
from the Python interpreter (`__pycache__`) or from `uvx` / `uv` dependency
management may still exist; those are toolchain side effects, not skill result
artifacts.

## Skills

| Skill | Summary | Typical Use | Installable Directory |
| --- | --- | --- | --- |
| [`drawio-diagram`](./drawio-diagram/) | Draw.io research-figure workflow that builds an editable draw.io draft, reuses source paper/poster assets when available, exports PNG/SVG/PDF, and runs visual QA on the exported PNG until the QA checklist passes. | Paper figures, posters, slide visuals, and concept diagrams that need an editable draw.io artifact the user can keep refining directly in draw.io. | [`drawio-diagram/drawio-diagram`](./drawio-diagram/drawio-diagram/) |
| [`minimax-image-understand`](./minimax-image-understand/) | Image understanding (describe / analyze / OCR) via the upstream `minimax-coding-plan-mcp` `understand_image` tool. Reads the MiniMax token-plan key from `~/.codex/switch_model/minimax/config.toml` (or `[model_providers.minimax].experimental_bearer_token` in `~/.codex/config.toml`). Supports local JPEG/PNG/WebP paths and HTTP(S) URLs. Prints results to stdout only; it does not write local result/debug files. | When Codex's built-in MCP integration is broken (#23186) and the user wants to understand an image (describe, analyze, OCR). | [`minimax-image-understand/`](./minimax-image-understand/) |
| [`minimax-task-preflight`](./minimax-task-preflight/) | Prompt-clarification preflight tuned for MiniMax M3 in Codex Desktop App. It reads a raw request, asks only the necessary follow-up questions, and rewrites the request into a clearer prompt without drifting into planning or deliverable design. | Before running MiniMax M3 on ambiguous or underspecified tasks where prompt clarity matters more than early planning. | [`minimax-task-preflight/minimax-task-preflight`](./minimax-task-preflight/minimax-task-preflight/) |
| [`minimax-thorough-execution`](./minimax-thorough-execution/) | Strict-execution protocol tuned for MiniMax M3 in Codex Desktop App. It forbids prompt rewriting during execution, prevents token-saving scope shrinkage, requires real visual inspection for screenshot/page tasks, requires source links for search-backed claims, maintains source maps, and appends a short completion audit. | When the main risks are prompt rewriting, laziness, skipped appendix/supplement, shallow search, image avoidance, or missing source grounding. | [`minimax-thorough-execution/minimax-thorough-execution`](./minimax-thorough-execution/minimax-thorough-execution/) |
| [`minimax-web-search`](./minimax-web-search/) | Web search via the upstream `minimax-coding-plan-mcp` `web_search` tool. Same key resolution as `minimax-image-understand`. Returns up to 15 organic results (titles, links, snippets) plus related-search suggestions. Prints results to stdout only; it does not write local result/debug files. | When Codex's built-in MCP integration is broken (#23186) and the user wants to search the web (news, latest updates, fact lookup, etc.). | [`minimax-web-search/`](./minimax-web-search/) |
| [`mock-review`](./mock-review/) | Mock peer-review workflow for manuscript authors. It researches venue or journal requirements, inspects manuscript PDFs, studies related literature and experimental baselines, and writes a simulated review for rebuttal preparation and paper improvement. | Pre-submission risk check, rebuttal preparation, reviewer-style critique before revising a manuscript. | [`mock-review/mock-review`](./mock-review/mock-review/) |
| [`research-survey-loop`](./research-survey-loop/) | Long-running literature survey workflow. It creates or resumes survey tasks, maintains stable task documents, searches prioritized sources, migrates local PDFs, reads papers in chunks, and incrementally writes a Chinese survey. | Sustained literature surveys for robotics, embodied AI, computer vision, world models, navigation, manipulation, 3D perception, and adjacent topics. | [`research-survey-loop/research-survey-loop`](./research-survey-loop/research-survey-loop/) |
| [`update-source-map`](./update-source-map/) | Create or update an agent-readable source map (Markdown + JSON) for any project directory. It auto-detects whether to build a new map or refresh an existing one, and preserves hand-curated per-file summaries across regenerations. | When starting work in a new / unfamiliar workspace, refreshing a stale index after files change, or handing a project over to another agent. | [`update-source-map/update-source-map`](./update-source-map/update-source-map/) |

## Install

Copy the installable skill directory into your Codex skills directory.

```powershell
# Install drawio-diagram
Copy-Item -Recurse -Force .\drawio-diagram\drawio-diagram "$env:USERPROFILE\.codex\skills\drawio-diagram"

# Install minimax-image-understand
Copy-Item -Recurse -Force .\minimax-image-understand "$env:USERPROFILE\.codex\skills\minimax-image-understand"

# Install minimax-task-preflight
Copy-Item -Recurse -Force .\minimax-task-preflight\minimax-task-preflight "$env:USERPROFILE\.codex\skills\minimax-task-preflight"

# Install minimax-thorough-execution
Copy-Item -Recurse -Force .\minimax-thorough-execution\minimax-thorough-execution "$env:USERPROFILE\.codex\skills\minimax-thorough-execution"

# Install minimax-web-search
Copy-Item -Recurse -Force .\minimax-web-search "$env:USERPROFILE\.codex\skills\minimax-web-search"

# Install mock-review
Copy-Item -Recurse -Force .\mock-review\mock-review "$env:USERPROFILE\.codex\skills\mock-review"

# Install research-survey-loop
Copy-Item -Recurse -Force .\research-survey-loop\research-survey-loop "$env:USERPROFILE\.codex\skills\research-survey-loop"

# Install update-source-map
Copy-Item -Recurse -Force .\update-source-map\update-source-map "$env:USERPROFILE\.codex\skills\update-source-map"
```

macOS / Linux equivalent:

```bash
# Install minimax-image-understand
cp -R ./minimax-image-understand "$HOME/.codex/skills/"

# Install minimax-web-search
cp -R ./minimax-web-search "$HOME/.codex/skills/"
```

If `CODEX_HOME` is configured, copy the folders into `$CODEX_HOME/skills/` instead.

### Prerequisite for the two MiniMax MCP skills

`minimax-web-search` and `minimax-image-understand` both spawn
`uvx minimax-coding-plan-mcp` to talk to the upstream server. You need
`uvx` on your `PATH`:

```bash
# macOS
brew install uv

# Linux (Debian/Ubuntu)
# see https://docs.astral.sh/uv/

# Windows (PowerShell)
iwr -useb https://astral.sh/uv/install.ps1 | iex
```

The two skills auto-discover your MiniMax token-plan key from any of:
- `$MINIMAX_API_KEY` env var
- `[model_providers.minimax].experimental_bearer_token` in `~/.codex/config.toml`
- `[model_providers.minimax].experimental_bearer_token` in `~/.codex/switch_model/minimax/config.toml`

No additional configuration is needed if any of those already hold your key.

Runtime note: the MiniMax wrapper scripts themselves do not persist search or
image-understanding outputs. They only print to stdout. CPython may still create
`__pycache__` bytecode files when scripts run, and `uvx` / `uv` may use its own
dependency cache (for example under the user's uv cache directory). Those caches
are normal interpreter/package-manager behavior and are not generated result
files from these skills.

## Notes

- These skills encode personal research workflows and do not represent official processes of any venue, journal, or institution.
- `minimax-task-preflight`, `minimax-thorough-execution`, `minimax-web-search`, and `minimax-image-understand` are tuned for **MiniMax M3 in Codex Desktop App**. The first two improve prompt clarity and execution thoroughness; the latter two provide web search and image understanding capabilities that Codex 0.137.0 cannot deliver through its own MCP integration due to the namespace-tools bug (openai/codex#23186).
- `minimax-web-search` and `minimax-image-understand` call the **upstream** `minimax-coding-plan-mcp` server via JSON-RPC. Results match the official tool's output exactly — no translation layer in between.
- `drawio-diagram` is intended for editable figure workflows; it produces a `.drawio` plus PNG/SVG/PDF exports and only declares the figure ready after the visual QA loop passes.
- Outputs from `mock-review` should be clearly labeled as simulated/mock reviews. They must not replace real peer review or impersonate official reviewer reports.
- Literature retrieval should prioritize legally accessible sources such as official open-access pages, arXiv, OpenReview, and author pages.
- For details about a specific skill, read the README files inside that skill folder.
