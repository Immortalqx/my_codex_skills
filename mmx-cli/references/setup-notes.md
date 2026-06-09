# MiniMax CLI Setup Notes

Read this file only when the user explicitly asks about setup, installation,
auth, config, or schema export. It is not part of the default task flow for the
`mmx-cli` skill.

## Install

```bash
npm install -g mmx-cli
```

## Auth

Check current auth state:

```bash
mmx auth status --output json --quiet --non-interactive
```

Login with an API key when needed:

```bash
mmx auth login --api-key sk-xxxxx
```

Per-call auth override:

```bash
mmx text chat --api-key sk-xxxxx --message "Hello"
```

Region can be left to auto-detect or overridden with `--region global` or
`--region cn`.

## Config

Config precedence:

1. CLI flags
2. Environment variables
3. `~/.mmx/config.json`
4. CLI defaults

Useful commands:

```bash
mmx config show
mmx config set --key region --value cn
mmx config set --key default-text-model --value MiniMax-M2.7-highspeed
```

Useful environment variables:

```bash
MINIMAX_API_KEY=sk-xxxxx
MINIMAX_REGION=cn
```

## Schema Export

Export JSON tool schemas when integrating `mmx` commands into another agent
framework:

```bash
mmx config export-schema
mmx config export-schema --command "video generate"
```

## Notes

- Use `--non-interactive` in agent or CI contexts.
- Use `--output json` when the caller needs structured output.
- Use `--dry-run` to inspect a request before an expensive generation command.
