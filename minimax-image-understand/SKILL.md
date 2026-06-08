---
name: minimax-image-understand
description: Image understanding via the upstream minimax-coding-plan-mcp tool, using the user's MiniMax token-plan API key. Use when the user wants to describe, analyze, OCR, or extract information from a specific image and Codex's built-in MCP integration is broken (openai/codex#23186). Triggers on phrases like "理解这张图", "描述这张图", "describe this image", "what's in this image", "OCR this", "analyze this picture", "caption this". Supports JPEG, PNG, and WebP from local file paths or URLs.
---

# MiniMax Image Understanding

This skill lets Codex do image understanding through the user's MiniMax
token-plan key, bypassing Codex 0.137.0's broken MCP integration
([openai/codex#23186](https://github.com/openai/codex/issues/23186)).

## When to use

The user wants to analyze a specific image (not search the web for
images). Triggers:

- English: "describe this image", "what's in this image", "what's in this picture", "analyze this image", "OCR this", "read the text in this image", "caption this", "explain this image"
- Chinese: "理解这张图", "描述这张图", "看看这张图", "图里有什么", "识别图片", "OCR", "图里的文字是什么"
- Mixed: "describe what's in /Users/me/Desktop/photo.jpg"

A file path or URL must be present in the user's message, OR you must
know where the image is (e.g. user just shared it in the conversation
and Codex can find it on disk).

Do **not** use this skill for web search (use `$minimax-web-search`
instead) or for "find me images of X" (that's a search).

## How to invoke

Run the bundled script via `exec_command`:

```bash
python3 <skill-dir>/scripts/image.py "<prompt>" "<image-source>" [--timeout S] [--print]
```

Where `<image-source>` is either:

- An absolute local file path, e.g. `/Users/me/Desktop/photo.png`
- An HTTP(S) URL, e.g. `https://example.com/x.jpg`
- A relative path resolved against the current working directory

Supported formats: **JPEG, PNG, WebP** (not PDF/GIF/PSD/SVG).

### Examples

```bash
# Local file (absolute path)
python3 scripts/image.py "Describe this image" "/Users/me/Desktop/photo.jpg"

# Local file with Chinese prompt
python3 scripts/image.py "请详细描述这张图片" "/tmp/screenshot.png"

# URL
python3 scripts/image.py "What is shown here?" "https://example.com/x.jpg"

# OCR
python3 scripts/image.py "Read all visible text in this receipt" "/Users/me/receipt.jpg"

# Raw JSON-RPC response (for programmatic parsing)
python3 scripts/image.py "describe" "https://..." --print

# Slow network? Extend timeout
python3 scripts/image.py "..." "..." --timeout 180
```

## What the output looks like

```text
[minimax-skill] connected to Minimax v1.27.2
[minimax-image-understand] prompt='一句话描述'
  source: /Users/immortalqx/Projects/minimax/6.jpg
  result: 一架全副武装的军用直升机在夜色中开启探照灯，低空飞越灯火通明的港口工业区。

full JSON: /tmp/minimax-mcp/result-YYYYMMDD-HHMMSS-NN.json
```

The `result:` line is the model's text description (truncated to 1500
chars for display; full content in the JSON file). The script always
writes the JSON file, even when the result is empty.

## How to present results to the user

1. Paste the `result:` line(s) directly into your response. The model's
   output is already a clean, descriptive text — usually no need to
   paraphrase.
2. If the user asked a specific question (e.g. "is this a cat?"), the
   model answers it directly. Just relay the answer.
3. If the user wants a shorter summary, re-run with a directive prompt:
   ```bash
   python3 scripts/image.py "用一句话描述这张图" "<same path>"
   ```
4. If the user wants OCR and the result is mixed with prose, ask the
   model to "list only the visible text" via a re-run.

## Configuration

Auto-discovers the API key from the same 3 locations as
`$minimax-web-search`:

1. `$MINIMAX_API_KEY` env var
2. `[model_providers.minimax].experimental_bearer_token` in
   `~/.codex/config.toml`
3. `[model_providers.minimax].experimental_bearer_token` in
   `~/.codex/switch_model/minimax/config.toml`

You (Codex) don't need to configure anything. If the user has a valid
key in any of those locations, the skill just works.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `file not found: <path>` | Path typo or wrong cwd | Verify with `ls -la <path>`; use absolute path |
| `unsupported format '.pdf'` | Format not in {JPEG, PNG, WebP} | Convert: `sips -s format jpeg in.pdf --out out.jpg` (macOS) |
| `MCP server closed stdout` | `uvx` issue | Try `uvx --from minimax-coding-plan-mcp minimax-coding-plan-mcp --help` |
| `Failed to perform VLM analysis` (in stderr) | Bad URL/path or upstream model error | Verify path with `file <path>`, retry once, or file upstream bug |
| `MINIMAX_API_KEY not found` | None of the 3 sources have a key | User needs to set up a key |

## When NOT to use this skill

- The user wants to search the web → use `$minimax-web-search`
- The user wants to fetch an image to look at → use `curl` / `wget` and
  then `view_image` tool
- The user wants to edit/transform an image → use a different tool/skill
- The user is in Claude Desktop, Cursor, or any non-Codex client → use
  the upstream MCP server directly

## Reference

- Bundled scripts: `scripts/image.py`, `scripts/lib_key.py`, `scripts/mcp_client.py`
- Upstream MCP server: [MiniMax-AI/MiniMax-Coding-Plan-MCP](https://github.com/MiniMax-AI/MiniMax-Coding-Plan-MCP)
- Root cause for needing this skill: [openai/codex#23186](https://github.com/openai/codex/issues/23186)
- Fix proposal: [openai/codex#26234](https://github.com/openai/codex/issues/26234)
