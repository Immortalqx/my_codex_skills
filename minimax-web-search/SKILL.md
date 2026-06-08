---
name: minimax-web-search
description: Web search via the upstream minimax-coding-plan-mcp tool, using the user's MiniMax token-plan API key. Use when the user wants to search the web from inside Codex and Codex's built-in MCP integration is broken (openai/codex#23186). Triggers on phrases like "搜", "查", "找", "search", "find", "look up", "google", "latest news on", "what's the latest". Returns up to 15 organic results (titles, links, snippets) plus related-search suggestions.
---

# MiniMax Web Search

This skill lets Codex do web search through the user's MiniMax token-plan
key, bypassing Codex 0.137.0's broken MCP integration
([openai/codex#23186](https://github.com/openai/codex/issues/23186)).

## When to use

The user asks for a web search and is running inside Codex. Triggers:

- English: "search", "find", "look up", "google", "latest news on", "what's the latest", "any updates on", "current status of"
- Chinese: "搜", "查", "找", "最新", "动态", "进展", "新闻", "百度", "谷歌", "知乎"
- Mixed: "帮我查 2026 年 AI 模型最新进展"

Do **not** use this skill for image understanding (use
`$minimax-image-understand` instead) or for fetching a specific URL.

## How to invoke

Run the bundled script via `exec_command`:

```bash
python3 <skill-dir>/scripts/search.py "<query>" [--max N] [--timeout S] [--print]
```

Where `<skill-dir>` is this skill's install location. The default `--max`
is 15; the user can override.

### Examples

```bash
# Default: top 15 results
python3 scripts/search.py "MiniMax-M3 release notes"

# Top 5 only
python3 scripts/search.py "2026 AI 模型最新进展" --max 5

# Raw JSON-RPC response (for programmatic parsing)
python3 scripts/search.py "test" --print

# Slow query? Extend the timeout
python3 scripts/search.py "obscure topic" --timeout 180
```

## What the output looks like

```text
[minimax-skill] connected to Minimax v1.27.2
[minimax-web-search] 9 results for: 'MiniMax-M3 release date 2026'
  1. <title>
     <link>
     <snippet (truncated to 140 chars)>
  2. ...
  ...

  related: <related query 1>, <related query 2>, ...
  status: code=0 msg=success

full JSON: /tmp/minimax-mcp/result-YYYYMMDD-HHMMSS-NN.json
```

The last line points to a JSON file containing the full request and
response (for debugging). The script always writes this file, even when
the summary is empty.

## How to present results to the user

1. Show the numbered list (titles + links). If the user wants the snippets
   included, re-show the wrapper output as-is.
2. If the user wants more than the default 15, re-run with `--max N` (cap
   at 30 — the upstream `web_search` tool itself returns at most ~10-20
   organic per query).
3. If the user wants raw data (e.g. all related_searches, base_resp), use
   the `full JSON:` path printed at the end. Don't re-parse stdout.

## Configuration

The script auto-discovers the API key from:

1. `$MINIMAX_API_KEY` env var
2. `[model_providers.minimax].experimental_bearer_token` in
   `~/.codex/config.toml`
3. `[model_providers.minimax].experimental_bearer_token` in
   `~/.codex/switch_model/minimax/config.toml`

The third location is where Codex persists the token-plan key when
`switch_model` is configured — it's the most reliable because Codex
sometimes strips `[mcp_servers.*]` blocks.

**You (Codex) do not need to do anything to configure this.** If the user
has a valid MiniMax token-plan key in any of those locations, the skill
just works.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `MINIMAX_API_KEY not found` | None of the 3 sources have a key | User needs to set up a key in one of the locations above |
| `MCP server closed stdout` | `uvx` cache issue or network problem | Try `uvx --from minimax-coding-plan-mcp minimax-coding-plan-mcp --help` to verify uvx works |
| `(no organic results)` | Query too niche or has no recent coverage | Rephrase with different keywords, add a year/date, or split into multiple queries |
| `MCP error -32603: Internal error` | Upstream MiniMax server hiccup | Retry once; if persistent, file upstream bug at [MiniMax-Coding-Plan-MCP](https://github.com/MiniMax-AI/MiniMax-Coding-Plan-MCP) |

## When NOT to use this skill

- The user wants to understand an image → use `$minimax-image-understand`
- The user wants to fetch and read a specific URL → use `curl` / `wget`
- The user is in Claude Desktop, Cursor, or any non-Codex client → those
  have working MCP integration; suggest the upstream MCP server instead
- The user is debugging Codex's MCP integration → that's a different topic

## Reference

- Bundled scripts: `scripts/search.py`, `scripts/lib_key.py`, `scripts/mcp_client.py`
- Upstream MCP server: [MiniMax-AI/MiniMax-Coding-Plan-MCP](https://github.com/MiniMax-AI/MiniMax-Coding-Plan-MCP)
- Root cause for needing this skill: [openai/codex#23186](https://github.com/openai/codex/issues/23186)
- Fix proposal: [openai/codex#26234](https://github.com/openai/codex/issues/26234)
