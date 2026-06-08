---
name: minimax-image-understand
description: Image understanding via the upstream minimax-coding-plan-mcp tool, using the user's MiniMax token-plan API key. Use when the user wants to describe, analyze, OCR, or extract information from a specific image and Codex's built-in MCP integration is broken (openai/codex#23186). Triggers on phrases like "describe this image", "what's in this image", "OCR this", "analyze this picture", "caption this". Supports JPEG, PNG, and WebP from local file paths or URLs.
---

# MiniMax Image Understanding

This skill lets Codex do image understanding through the user's MiniMax token-plan key, bypassing Codex 0.137.0's broken MCP integration ([openai/codex#23186](https://github.com/openai/codex/issues/23186)).

## When to use

Use this skill when Codex's built-in MCP integration is broken and the user wants to understand a specific image (describe, analyze, OCR). The user message must contain a file path or URL, or the image must be discoverable on disk.

## How to invoke

Run the bundled script via `exec_command`:

```bash
python3 <skill-dir>/scripts/image.py "<prompt>" "<image-source>" [--timeout S] [--print]
```

Where `<image-source>` is either:

- An absolute local file path, e.g. `/Users/me/Desktop/photo.png`
- An HTTP(S) URL, e.g. `https://example.com/x.jpg`
- A relative path resolved against the current working directory

Supported formats: **JPEG, PNG, WebP** (not PDF/GIF/PSD/SVG). The script prints the image-understanding result to stdout for Codex to read and does not write local result/cache/debug files.

## What the output looks like

```text
[minimax-skill] connected to Minimax v1.27.2
[minimax-image-understand] prompt='<the prompt>'
  source: <path-or-url>
  result: <model description, truncated to 1500 chars>
```

The `result:` line is the model's text description. Output is stdout only, so Codex receives the answer directly and no local result/cache/ debug file is created.

## How to present results to the user

1. Paste the `result:` line(s) directly into your response. The model's
   output is already a clean, descriptive text - usually no need to paraphrase.
2. If the user asked a specific question (e.g. "is this a cat?"), the
   model answers it directly. Just relay the answer.
3. If the user wants a shorter summary, re-run with a directive prompt.
4. If the user wants OCR and the result is mixed with prose, ask the
   model to "list only the visible text" via a re-run.
5. If the user wants the raw MCP response, re-run with `--print` to emit
   the full JSON-RPC response to stdout.

## Configuration

Auto-discovers the API key from the 3 standard Codex locations:

1. `$MINIMAX_API_KEY` env var
2. `[model_providers.minimax].experimental_bearer_token` in
   `~/.codex/config.toml`
3. `[model_providers.minimax].experimental_bearer_token` in
   `~/.codex/switch_model/minimax/config.toml`

You (Codex) don't need to configure anything. If the user has a valid key in any of those locations, the skill just works.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `file not found: <path>` | Path typo or wrong cwd | Verify with `ls -la <path>`; use absolute path |
| `unsupported format '.pdf'` | Format not in {JPEG, PNG, WebP} | Convert: `sips -s format jpeg in.pdf --out out.jpg` (macOS) |
| `MCP server closed stdout` | `uvx` issue | Try `uvx --from minimax-coding-plan-mcp minimax-coding-plan-mcp --help` |
| `Failed to perform VLM analysis` (in stderr) | Bad URL/path or upstream model error | Verify path with `file <path>`, retry once, or file upstream bug |
| `MINIMAX_API_KEY not found` | None of the 3 sources have a key | User needs to set up a key |

## When NOT to use this skill

- The user wants to search the web - use a web search skill
- The user wants to fetch an image to look at - use `curl` / `wget` and
  then `view_image` tool
- The user wants to edit/transform an image - use a different tool/skill
- The user is in Claude Desktop, Cursor, or any non-Codex client - use
  the upstream MCP server directly

## Reference

- Bundled scripts: `scripts/image.py`, `scripts/lib_key.py`, `scripts/mcp_client.py`
- Upstream MCP server: [MiniMax-AI/MiniMax-Coding-Plan-MCP](https://github.com/MiniMax-AI/MiniMax-Coding-Plan-MCP)
- Root cause for needing this skill: [openai/codex#23186](https://github.com/openai/codex/issues/23186)
- Fix proposal: [openai/codex#26234](https://github.com/openai/codex/issues/26234)
