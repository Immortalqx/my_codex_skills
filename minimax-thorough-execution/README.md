# minimax_thorough_execution

Chinese version: [README.zh-CN.md](./README.zh-CN.md)

`minimax_thorough_execution` is a Codex skill repository tuned for **MiniMax M3 inside Codex Desktop App**.

It is the execution layer used after the prompt is already clear. The skill is designed to counter MiniMax-style shortcut behavior such as token-saving scope shrinkage, reading only the abstract and introduction, skipping appendix or supplementary material, avoiding real visual inspection, performing shallow search, and omitting source links.

The installable skill is in [minimax-thorough-execution/](./minimax-thorough-execution/).

## Important Boundary

This skill assumes the prompt is already clear.

It is meant to enforce execution discipline, not to replace prompt clarification. In the normal workflow, use [`minimax-task-preflight`](../minimax-task-preflight/) first when the request is still ambiguous.

## What It Enforces

- no silent scope reduction to save tokens
- completeness by default unless the user explicitly asks for a cheaper or shorter pass
- paper reading must include the body, not just abstract/introduction
- appendix and supplementary material must be checked when present and relevant
- screenshot and page-level tasks must use rendered visual inspection rather than caption guessing or OCR-only shortcuts
- search-backed answers must return original links
- searched claims must be tied to sources
- the final answer must include a short `Completion audit`

## Quick Start

Copy the installable skill into `$CODEX_HOME/skills/`:

```bash
cp -R minimax-thorough-execution "$CODEX_HOME/skills/"
```

Then ask Codex to use `$minimax-thorough-execution` on an already-clear prompt:

```text
Use $minimax-thorough-execution to execute this already-clear prompt thoroughly, without silently shrinking scope, skipping appendix or supplement, guessing from text instead of inspecting images, or omitting source links.
```

## Typical Use

Example:

```text
Use $minimax-thorough-execution on this clarified prompt:
"Read paper.pdf carefully, including any appendix or supplementary PDF in the workspace. Explain the method and experiments in Chinese, and if you cite any current external facts, search for them and return the original links."
```

## Completion Audit

This skill requires a short audit block in the final answer:

```text
Completion audit:
- Scope: checked | narrowed | blocked
- Body/appendix/supplement: checked | not applicable | blocked
- Visual verification: checked | not applicable | blocked
- Search and links: checked | not applicable | blocked
```

The audit is intentionally short. Its purpose is to make MiniMax M3 expose whether it actually completed the critical checks instead of silently assuming them.

## Recommended Pairing

Typical sequence:

1. run [`$minimax-task-preflight`](../minimax-task-preflight/)
2. answer the follow-up questions if needed
3. run `$minimax-thorough-execution` on the clarified prompt

## Repository Layout

- `README.md` and `README.zh-CN.md`: repository docs
- `minimax-thorough-execution/`: installable Codex skill
- `minimax-thorough-execution/SKILL.md`: skill definition
- `minimax-thorough-execution/agents/`: agent config used by the skill
