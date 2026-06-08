# minimax-web-search

English | [中文](./README.zh-CN.md)

Web search via the upstream `minimax-coding-plan-mcp` `web_search` tool, using the user's MiniMax token-plan key. Bypasses Codex 0.137.0's broken MCP integration ([openai/codex#23186](https://github.com/openai/codex/issues/23186)).

Returns up to 15 organic results (titles, links, snippets) plus related-search suggestions. Prints results to stdout only - does not write local result, cache, or debug files.

## When to use

Use this skill when Codex's built-in MCP integration is broken and the user wants to search the web (news, latest updates, fact lookup, etc.). Triggers: "search", "find", "look up", "google", "latest news on", "what's the latest", "any updates on", "current status of".

Do **not** use this skill for:

- Image understanding - use an image-understanding skill instead
- Fetching / reading a specific URL - use `curl` / `wget`

## Bilingual search (recommended for broad coverage)

For broad, fast-moving, or authoritative-coverage queries, the skill recommends running the script **twice** with the same intent in two languages and merging the results:

1. **English keywords** - the query translated to English
2. **Chinese keywords** - the same intent translated to Chinese

Then dedupe by URL, prefer the higher-ranked hit when the same URL appears in both, and present the combined set to the user. For narrow technical lookups (a specific API, a specific error message, a single library), a single language is usually enough - the skill says so explicitly. See `SKILL.md` -> "Bilingual search" for the full recommendation and a worked example.

## Configuration

The bundled script auto-discovers the MiniMax API key from three locations (checked in this order):

1. `$MINIMAX_API_KEY` environment variable
2. `[model_providers.minimax].experimental_bearer_token` in `~/.codex/config.toml`
3. `[model_providers.minimax].experimental_bearer_token` in `~/.codex/switch_model/minimax/config.toml`

The third location is where Codex persists the token-plan key when `switch_model` is configured - it is the most reliable because Codex sometimes strips `[mcp_servers.*]` blocks.

You do not need to configure anything manually - if the key is present in any of those locations, the skill just works.

## Reference

- Full skill instructions: [`minimax-web-search/SKILL.md`](./minimax-web-search/SKILL.md)
- Upstream MCP server: [MiniMax-AI/MiniMax-Coding-Plan-MCP](https://github.com/MiniMax-AI/MiniMax-Coding-Plan-MCP)
- Codex MCP issue: [openai/codex#23186](https://github.com/openai/codex/issues/23186)
- See also: image-understanding skill (if installed)

