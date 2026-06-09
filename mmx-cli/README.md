# mmx-cli

English | [中文](./README.zh-CN.md)

`mmx-cli` is the official MiniMax CLI skill from [MiniMax-AI/cli](https://github.com/MiniMax-AI/cli/tree/main/skill). The installable skill body is kept as an exact copy of the upstream `SKILL.md` so Codex can use `mmx` for text, image, video, speech, music, web search, vision, quota, file, and schema-export workflows.

Use this skill when you want Codex to operate through the local `mmx` command-line interface:

```text
Use $mmx-cli to run a MiniMax CLI dry run for an image generation request and show me the request JSON.
```

For token-sensitive checks, ask Codex to use `--dry-run`, `--quiet`, `--output json`, and `--non-interactive`.

## Installable Directory

The installable Codex skill is:

```text
mmx-cli/mmx-cli/
```

Do not install the outer `mmx-cli/` folder. It contains repository README files only.

## Contents

- `mmx-cli/SKILL.md`: exact upstream MiniMax CLI skill document.

## Prerequisite

Install and configure the MiniMax CLI before using the skill:

```bash
npm install -g mmx-cli
mmx auth status
```
