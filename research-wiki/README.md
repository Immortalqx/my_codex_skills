# research-wiki

English | [中文](./README.zh-CN.md)

`research-wiki` is a standalone Codex skill for maintaining a persistent research knowledge base across papers, ideas, experiments, claims, and typed relationships. It is designed to keep research context reusable instead of rebuilding the same field map in every session.

Use `$research-wiki` when you want Codex to initialize, query, or update a project-level research wiki:

```text
Use $research-wiki to initialize a research wiki for this project and ingest the arXiv papers we have already discussed.
```

For querying:

```text
Use $research-wiki to summarize the top gaps and failed ideas in the current research-wiki/ directory.
```

## Workflow

1. Codex initializes or reuses a `research-wiki/` directory in the current project.
2. Codex stores papers, ideas, experiments, and claims as separate Markdown pages.
3. Codex stores relationships in `graph/edges.jsonl` and rebuilds compact views from that graph.
4. Codex uses `scripts/research_wiki.py` as the canonical helper for initialization, paper ingest, edge updates, index rebuilds, query-pack generation, and sync.
5. Codex may run `scripts/verify_wiki_coverage.sh` as a non-blocking local diagnostic.

## Outputs

- A persistent `research-wiki/` project directory.
- Paper, idea, experiment, and claim pages.
- `index.md`, `log.md`, `gap_map.md`, `query_pack.md`, and `graph/edges.jsonl`.
- Optional diagnostic output for missing paper ingests.

## Helper Scripts

- [research-wiki/scripts/research_wiki.py](./research-wiki/scripts/research_wiki.py): canonical helper for wiki mutation and rebuild operations.
- [research-wiki/scripts/verify_wiki_coverage.sh](./research-wiki/scripts/verify_wiki_coverage.sh): non-blocking coverage diagnostic.

## Installable Directory

The installable Codex skill is:

```text
research-wiki/research-wiki/
```

Do not install the outer `research-wiki/` folder. It contains repository README files only.

## Contents

- `research-wiki/SKILL.md`: persistent research wiki workflow.
- `research-wiki/scripts/`: deterministic wiki helper scripts.
- `research-wiki/agents/openai.yaml`: UI metadata for Codex skill lists.
