# minimax-image-understand

English | [中文](./README.zh-CN.md)

Image understanding (describe / analyze / OCR) via the upstream `minimax-coding-plan-mcp` `understand_image` tool, using the user's MiniMax token-plan key. Bypasses Codex 0.137.0's broken MCP integration ([openai/codex#23186](https://github.com/openai/codex/issues/23186)).

Supports local JPEG / PNG / WebP file paths and HTTP(S) URLs. Prints results to stdout only - does not write local result, cache, or debug files.

The `SKILL.md` and all bundled scripts use **English only** so that Codex never sees CJK mojibake when reading the skill.

## When to use

Use this skill when Codex's built-in MCP integration is broken and the user wants to understand a specific image (describe, analyze, OCR). Triggers (English only): "describe this image", "what's in this image", "OCR this", "read the text in this image", "analyze this picture", "caption this".

Do **not** use this skill for:

- Web search - use a web search skill instead
- Searching for images of X on the web - use a real web search
- Editing / transforming an image - use a different image tool

## Installable skill directory

The actual installable skill (with `SKILL.md`, `agents/`, `scripts/`) lives in:

```
minimax-image-understand/minimax-image-understand/
```

Point your Codex skill installer at that nested directory. The top-level `README.md` and `README.zh-CN.md` here are repo-level documentation only and are not part of the installable skill, so they will not be confused with `SKILL.md` by the installer.

## Configuration

The bundled script auto-discovers the MiniMax API key from three locations (checked in this order):

1. `$MINIMAX_API_KEY` environment variable
2. `[model_providers.minimax].experimental_bearer_token` in `~/.codex/config.toml`
3. `[model_providers.minimax].experimental_bearer_token` in `~/.codex/switch_model/minimax/config.toml`

You do not need to configure anything manually - if the key is present in any of those locations, the skill just works.

## Reference

- Full skill instructions: [`minimax-image-understand/SKILL.md`](./minimax-image-understand/SKILL.md)
- Upstream MCP server: [MiniMax-AI/MiniMax-Coding-Plan-MCP](https://github.com/MiniMax-AI/MiniMax-Coding-Plan-MCP)
- Codex MCP issue: [openai/codex#23186](https://github.com/openai/codex/issues/23186)
- See also: web search skill (if installed)
