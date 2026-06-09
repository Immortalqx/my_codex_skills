---
name: mmx-cli
description: Operate the local MiniMax CLI (`mmx`) from Codex. Use when Codex needs to run MiniMax-specific text chat, web search, vision, image generation, video generation, speech synthesis, music generation, quota inspection, or MiniMax file operations through the installed `mmx` command, especially when the user explicitly mentions MiniMax or `mmx`.
---

# MiniMax CLI

Target request: `$ARGUMENTS`

## Overview

Operate the already-installed local `mmx` command as the execution surface for
MiniMax tasks. Keep the main flow focused on doing the user`s task, not on
teaching the CLI.

Load `references/setup-notes.md` only when the user explicitly asks about
installation, authentication, configuration, or schema export.

## Execution Workflow

1. Determine the narrowest `mmx` command that fits the task:
   `text chat`, `search query`, `vision describe`, `image generate`,
   `video generate`, `speech synthesize`, `music generate`, `music cover`,
   `quota show`, or `file` operations.
2. Verify runtime readiness with `mmx --version` or
   `mmx auth status --output json --quiet --non-interactive`.
3. Run the command with agent-safe defaults first.
4. Save generated artifacts with explicit workspace-local output paths.
5. Verify the returned JSON, task IDs, URLs, or files before reporting success.

## Agent Defaults

Use these flags by default in agent mode:

- `--non-interactive`
- `--quiet`
- `--output json` when machine-readable output helps

Add these selectively:

- `--dry-run` before an expensive or ambiguous request
- `--async` for long-running video generation
- explicit output path flags such as `--out`, `--out-dir`, or `--download`
  for binary artifacts

## Search Policy

When using `mmx search query`, default to mixed Chinese + English and multiple
search passes. Do not answer from a single query unless the task is trivial.

For any non-trivial search:

1. Run at least one English technical query.
2. Run at least one Chinese query for the same concept.
3. Run at least one mixed-language query that combines Chinese topic words with
   canonical English names, abbreviations, model names, venue names, or product
   terms.
4. If the topic is recent, ambiguous, or sparse, add more passes with synonyms,
   recency words, or source-specific filters in the query string.
5. Compare results across the query set before answering.
6. Prefer citing URLs and titles from JSON output instead of paraphrasing from
   memory.

Read `references/search-playbook.md` when query design matters.

## Command Patterns

Prefer short, task-shaped commands:

```bash
mmx text chat --message "user:Explain this result" --output json --quiet --non-interactive
mmx search query --q "embodied navigation world model benchmark" --output json --quiet --non-interactive
mmx vision describe --image figure.png --prompt "Explain the key takeaway." --output json --quiet --non-interactive
mmx auth status --output json --quiet --non-interactive
```

Use explicit workspace-local output paths for generated artifacts:

```bash
mmx image generate --prompt "..." --out-dir .\\outputs --quiet --non-interactive
mmx speech synthesize --text "..." --out .\\outputs\\sample.mp3 --quiet --non-interactive
mmx video generate --prompt "..." --download .\\outputs\\clip.mp4 --quiet --non-interactive
```

Preview expensive or ambiguous generation first:

```bash
mmx image generate --prompt "..." --dry-run --output json --quiet --non-interactive
```

Track async video tasks through `video task get` and `video download` before
treating the job as complete.

## Failure Handling

- Report missing `mmx`, failed auth, or quota blockers directly.
- Broaden weak search runs with bilingual synonyms and additional passes.
- Prefer `--dry-run` or `--async` before committing to expensive generation.
- Perform the required follow-up step when a command returns only task IDs,
  file IDs, or URLs instead of a finished local artifact.

## References

Load these only when needed:

- `references/setup-notes.md` for installation, auth, config, and schema export
- `references/search-playbook.md` for concrete bilingual multi-search patterns
