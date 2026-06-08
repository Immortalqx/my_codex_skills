# minimax_thorough_execution

Chinese version: [README.zh-CN.md](./README.zh-CN.md)

`minimax_thorough_execution` is a Codex skill repository tuned for **MiniMax M3 inside Codex Desktop App**.

It is a strict execution layer for **following the user's prompt as written**. The skill is designed to counter MiniMax-style failure modes such as rewriting the task, silently shrinking scope to save tokens, reading only the abstract and introduction, skipping appendix or supplementary material, avoiding real visual inspection, performing shallow search, and omitting source links.

The installable skill is in [minimax-thorough-execution/](./minimax-thorough-execution/).

## Important Boundary

This skill does not clarify, judge, optimize, or rewrite the prompt.

It is meant to enforce execution discipline and strong instruction following. If you want a separate clarification pass, use [`minimax-task-preflight`](../minimax-task-preflight/) first, but this skill itself must still execute the prompt literally rather than rewriting it.

## What It Enforces

- strict obedience to the user's prompt
- no prompt rewriting, prompt optimization, or silent reinterpretation during execution
- no silent scope reduction to save tokens
- completeness by default unless the user explicitly asks for a cheaper or shorter pass
- prefer local persisted task artifacts over fragile long-conversation memory
- temp artifacts must stay organized under typed task subfolders instead of piling up in the task root
- the model should search the current environment for relevant installed skills and call zero, one, or multiple suitable skills when useful
- maintain source maps and evidence maps rather than leaving only scattered cache files
- paper reading must include the body, not just abstract/introduction
- appendix and supplementary material must be checked when present and relevant
- screenshot and page-level tasks must use rendered visual inspection rather than caption guessing or OCR-only shortcuts
- search-backed answers must return original links
- searched claims must be tied to sources
- the final answer must include a short `Completion audit`

## Local Temp Cache

This skill now assumes that reliable multi-turn work should be grounded in local task artifacts, not only in chat history.

Before substantial execution, it should:

1. look for an existing temp-like working root in the workspace, such as `x_temp_codex`, `x_temp`, `temp_codex`, `temp`, `tmp`, `codex_temp`, or `.temp`
2. if none exists, create a new temp root that matches local naming style; prefer `x_temp_codex/` when the workspace already uses `x_*` utility folders, otherwise use `temp_codex/`
3. create or reuse a task-specific subfolder under that temp root
4. read any existing workspace-level or task-level source maps that matter
5. save the exact user prompt and reusable intermediate artifacts there

Typical artifacts include:

- `prompt.txt`
- `task_summary.md`
- `local_source_map.md` / `local_source_map.json`
- `evidence_map.md`
- downloaded papers and source files
- extracted text or scan outputs
- rendered PDF or slide images
- screenshots
- search notes and source links
- intermediate JSON or Markdown notes
- audit records

Required shape:

```text
<temp-root>/<task-subdir>/
  prompt.txt
  prompt_history.md
  task_summary.md
  manifest.json
  local_source_map.md
  local_source_map.json
  evidence_map.md
  completion_audit.md
  sources/
    user_files/
    fetched/
  extracted_text/
    page_text/
    ocr/
  renders/
    pages/
    verification/
  screenshots/
    selected/
  search/
    queries/
    results/
  notes/
  scripts/
  logs/
  audit/
```

Only prompt, summary, manifest, source-map, evidence-map, and audit files should live directly under the task subfolder. PDFs, webpages, images, extracted text, helper scripts, logs, and intermediate notes should go into typed subfolders or the closest existing local equivalent.

If an existing task folder is already messy, the skill should stop adding loose files to the root. New artifacts should go into typed subfolders and the existing loose files should be recorded in the source map or manifest. Existing files should not be moved unless the user asks.

If the workspace already has a stronger local convention, the skill should reuse it. In your own workspaces this often means reading an existing workspace-level map such as `x_codex/source_map.json` first, then maintaining a task-local `local_source_map` or `evidence_map` inside the current `x_temp_codex/`, `x_temp/`, or similar temp task folder.

For follow-up turns, MiniMax M3 should look for the existing task subfolder first, read the saved prompt history, task summary, manifest, source maps, evidence maps, rendered pages, downloaded files, extracted text, screenshots, notes, and audit artifacts, then continue from those local artifacts instead of relying only on compressed conversation context.

When the answer depends on visual content, MiniMax M3 should re-open the relevant rendered pages or images before making new claims or choosing screenshots.

## Skill Search And Delegation

Before generic shell commands, direct downloads, ad-hoc scripts, or manual search, MiniMax M3 should search the current environment for relevant installed skills, plugins, or specialized workflows.

Rules:

- use direct fallback only when no relevant skill exists
- call one relevant skill when one clearly matches
- call multiple relevant skills when the task benefits from combining them
- do not assume only one skill may apply
- do not commit to a generic workflow before checking the local skill environment
- do not skip skill discovery merely because `wget`, `curl`, or manual search seems shorter

This is execution routing only. It does not authorize prompt rewriting or task reinterpretation.

## Source Maps

This skill now treats `source map` maintenance as part of the execution contract.

That means MiniMax M3 should:

- look for existing workspace-level source-tracking files such as `x_codex/source_map.json`, `manifest.json`, or `file_inventory.jsonl`
- look for task-level maps such as `local_source_map*.md`, `source_map*.json`, or `evidence_map*.md`
- update those maps when new PDFs, webpages, screenshots, extracted texts, or derived notes are introduced

A source map should capture at least:

- local path
- original URL or origin
- source type
- task role, such as primary evidence, supplementary evidence, candidate source, or cache only
- read status
- whether the file is original evidence or only a derived artifact

The source map is an organizational and continuation artifact. It is not final evidence by itself.

## Quick Start

Copy the installable skill into `$CODEX_HOME/skills/`:

```bash
cp -R minimax-thorough-execution "$CODEX_HOME/skills/"
```

Then ask Codex to use `$minimax-thorough-execution` on the user's prompt:

```text
Use $minimax-thorough-execution to execute my prompt exactly as written, without rewriting it, silently shrinking scope, skipping appendix or supplement, guessing from text instead of inspecting images, or omitting source links.
```

## Typical Use

Example:

```text
Use $minimax-thorough-execution on this prompt:
"Read paper.pdf carefully, including any appendix or supplementary PDF in the workspace. Explain the method and experiments in Chinese, and if you cite any current external facts, search for them and return the original links."
```

## Completion Audit

This skill requires a short audit block in the final answer:

```text
Completion audit:
- Prompt obedience: checked | blocked
- Scope: checked | narrowed | blocked
- Skill search and delegation: checked | not applicable | blocked
- Temp artifact layout: checked | blocked
- Source map: checked | not applicable | blocked
- Local artifact re-read: checked | not applicable | blocked
- Body/appendix/supplement: checked | not applicable | blocked
- Visual verification: checked | not applicable | blocked
- Search and links: checked | not applicable | blocked
```

The audit is intentionally short. Its purpose is to make MiniMax M3 expose whether it actually completed the critical checks instead of silently assuming them.

When useful, the final answer can also mention the local artifact location briefly so the next turn can continue from it.

## Recommended Pairing

Typical sequence:

1. run a prompt-clarification skill first (if installed)
2. answer the follow-up questions if needed
3. run `$minimax-thorough-execution` on the resulting prompt without changing it again

## Repository Layout

- `README.md` and `README.zh-CN.md`: repository docs
- `minimax-thorough-execution/`: installable Codex skill
- `minimax-thorough-execution/SKILL.md`: skill definition
- `minimax-thorough-execution/agents/`: agent config used by the skill
