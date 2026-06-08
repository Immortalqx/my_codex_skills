---
name: minimax-web-search
description: Web search via the upstream minimax-coding-plan-mcp tool, using the user's MiniMax token-plan API key. Use when the user wants to search the web from inside Codex and Codex's built-in MCP integration is broken (openai/codex#23186). Triggers on phrases like "search", "find", "look up", "google", "latest news on", "what's the latest". Returns up to 15 organic results (titles, links, snippets) plus related-search suggestions.
---

# MiniMax Web Search

This skill lets Codex do web search through the user's MiniMax
token-plan key, bypassing Codex 0.137.0's broken MCP integration
([openai/codex#23186](https://github.com/openai/codex/issues/23186)).

## When to use

Use this skill when Codex's built-in MCP integration is broken and the
user wants to search the web (news, latest updates, fact lookup, etc.).

Do **not** use this skill for image understanding (use
`$minimax-image-understand` instead) or for fetching a specific URL.

## How to invoke

Run the bundled script via `exec_command`:

```bash
python3 <skill-dir>/scripts/search.py "<query>" [--max N] [--timeout S] [--print]
```

Where `<skill-dir>` is this skill's install location. The default `--max`
is 15; the user can override. The script prints results to stdout for
Codex to read and does not write local result/cache/debug files.

### Bilingual search (recommended for broad coverage)

The upstream search tool returns the most useful results when the query
matches the language of the corpus. For broad, fast-moving, or
authoritative-coverage queries, run the script **twice** with the same
intent in two languages and merge the results:

1. **English keywords** - the query translated to English (or kept
   as-is if already English).
2. **Chinese keywords** - the same intent translated to Chinese (or
   kept as-is if already Chinese).

Then dedupe the two result lists by URL, prefer the higher-ranked hit
when the same URL appears in both, and present the combined set to the
user.

Worked example for the user query "what's the latest on AI agents in
2026":

```bash
# English pass
python3 scripts/search.py "AI agents latest 2026"

# Chinese pass - same intent, Chinese keywords (the script accepts
# non-ASCII input directly; no encoding flag is needed)
python3 scripts/search.py "AI 智能体 最新进展 2026"
```

When to apply:

- **Use bilingual** for broad news, latest trends, multi-source
  comparison, anything where the user wants comprehensive coverage, and
  any query whose target audience spans English and Chinese web
  sources.
- **One language is fine** for narrow lookups: a specific API name, a
  specific error message, a single library, a fixed URL or paper
  title. Doubling the call would just add noise here.

The translation between English and Chinese is a model-side step - the
script just forwards whatever query string it is given.

## What the output looks like

```text
[minimax-skill] connected to Minimax v1.27.2
[minimax-web-search] 9 results for: '<query>'
  1. <title>
     <link>
     <snippet (truncated to 140 chars)>
  2. ...
  ...

  related: <related query 1>, <related query 2>, ...
  status: code=0 msg=success
```

The output is stdout only, so Codex receives the search results directly
and no local result/cache/debug file is created.

## How to present results to the user

1. When you ran bilingual search, dedupe by URL first, then show the
   combined numbered list (titles + links). If the user wants the
   snippets included, re-show the wrapper output as-is.
2. If the user wants more than the default 15 per pass, re-run with
   `--max N` (cap at 30 - the upstream `web_search` tool itself
   returns at most ~10-20 organic per query).
3. If the user wants raw data (e.g. all related_searches, base_resp),
   re-run with `--print` to emit the full JSON-RPC response to stdout.

## Configuration

The script auto-discovers the API key from:

1. `$MINIMAX_API_KEY` env var
2. `[model_providers.minimax].experimental_bearer_token` in
   `~/.codex/config.toml`
3. `[model_providers.minimax].experimental_bearer_token` in
   `~/.codex/switch_model/minimax/config.toml`

The third location is where Codex persists the token-plan key when
`switch_model` is configured - it is the most reliable because Codex
sometimes strips `[mcp_servers.*]` blocks.

**You (Codex) do not need to do anything to configure this.** If the user
has a valid MiniMax token-plan key in any of those locations, the skill
just works.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `MINIMAX_API_KEY not found` | None of the 3 sources have a key | User needs to set up a key in one of the locations above |
| `MCP server closed stdout` | `uvx` cache issue or network problem | Try `uvx --from minimax-coding-plan-mcp minimax-coding-plan-mcp --help` to verify uvx works |
| `(no organic results)` | Query too niche or has no recent coverage | Rephrase with different keywords, add a year/date, or split into multiple queries. If only one language returned nothing, try the other language pass. |
| `MCP error -32603: Internal error` | Upstream MiniMax server hiccup | Retry once; if persistent, file upstream bug at [MiniMax-Coding-Plan-MCP](https://github.com/MiniMax-AI/MiniMax-Coding-Plan-MCP) |

## When NOT to use this skill

- The user wants to understand an image - use `$minimax-image-understand`
- The user wants to fetch and read a specific URL - use `curl` / `wget`
- The user is in Claude Desktop, Cursor, or any non-Codex client - those
  have working MCP integration; suggest the upstream MCP server instead
- The user is debugging Codex's MCP integration - that's a different topic

## Reference

- Bundled scripts: `scripts/search.py`, `scripts/lib_key.py`, `scripts/mcp_client.py`
- Upstream MCP server: [MiniMax-AI/MiniMax-Coding-Plan-MCP](https://github.com/MiniMax-AI/MiniMax-Coding-Plan-MCP)
- Root cause for needing this skill: [openai/codex#23186](https://github.com/openai/codex/issues/23186)
- Fix proposal: [openai/codex#26234](https://github.com/openai/codex/issues/26234)
