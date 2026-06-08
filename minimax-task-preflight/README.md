# minimax_task_preflight

Chinese version: [README.zh-CN.md](./README.zh-CN.md)

`minimax_task_preflight` is a Codex skill repository tuned for **MiniMax M3 inside Codex Desktop App**.

It is a narrow preflight layer used before execution. The skill reads a raw user request, identifies only the ambiguities that matter, asks concise follow-up questions when needed, and rewrites the request into a clearer prompt.

The installable skill is in [minimax-task-preflight/](./minimax-task-preflight/).

## Important Boundary

This skill is for **prompt clarification only**.

It must not:

- start solving the task
- design the deliverable
- create an execution plan
- decide task scope on its own
- optimize for token savings

The goal is to help MiniMax M3 understand the request better before execution, not to let it pre-plan the later work.

## Quick Start

Copy the installable skill into `$CODEX_HOME/skills/`:

```bash
cp -R minimax-task-preflight "$CODEX_HOME/skills/"
```

Then ask Codex to use `$minimax-task-preflight` on a raw request:

```text
Use $minimax-task-preflight to read my raw request, ask only the necessary clarification questions, and rewrite it into a clearer prompt without planning how to execute it.
```

Example:

```text
Use $minimax-task-preflight for this request:
"Read this paper carefully and explain it to me."
```

## How It Works

1. Codex reads the request literally.
2. Codex identifies only the ambiguities that materially affect the later prompt.
3. Codex asks concise follow-up questions when needed.
4. Codex returns either:
   - a short clarification block, or
   - a rewritten prompt

## Typical Output

When clarification is needed:

```text
Need clarification:
1. Which paper should I read?
2. Do you want a broad explanation, a section-by-section explanation, or a deep technical breakdown?
3. Should I include appendix and supplementary material if they exist?
```

When the request is already clear enough:

```text
Rewritten prompt:
Read the paper in paper.pdf and explain the method section in Chinese. If the appendix contains training details, evaluation settings, implementation details, or other information needed to understand the method, include those appendix details in the explanation.
```

## Recommended Pairing

This skill is intended to be used before a strict-execution skill (whichever is installed).

Typical sequence:

1. run `$minimax-task-preflight`
2. answer its follow-up questions if needed
3. pass the clarified prompt into the strict-execution skill

## Repository Layout

- `README.md` and `README.zh-CN.md`: repository docs
- `minimax-task-preflight/`: installable Codex skill
- `minimax-task-preflight/SKILL.md`: skill definition
- `minimax-task-preflight/agents/`: agent config used by the skill
