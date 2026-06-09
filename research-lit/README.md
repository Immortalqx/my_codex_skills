# research-lit

English | [中文](./README.zh-CN.md)

`research-lit` is a standalone Codex skill for searching, comparing, and synthesizing research papers across local PDFs, public web search, and structured arXiv metadata.

Use `$research-lit` when you want Codex to find related work, summarize a paper landscape, or understand what existing papers say about a topic:

```text
Use $research-lit to find recent papers about diffusion policies for robot manipulation and summarize the main method families.
```

For a narrower source selection:

```text
Use $research-lit to survey test-time scaling for VLM agents, sources: local, web, arxiv download: true.
```

## Workflow

1. Codex parses the topic, source selection, local paper-library path, and optional arXiv download settings.
2. Codex scans local `papers/` and `literature/` folders, or a user-provided paper library.
3. Codex uses public web search for recent and official paper pages.
4. Codex uses the bundled arXiv helper script for structured metadata and optional PDF download.
5. Codex de-duplicates papers by arXiv ID, URL, or normalized title.
6. Codex analyzes each relevant paper by problem, method, results, relevance, and source, then synthesizes the landscape.

## Outputs

- Literature tables with citation metadata, method summaries, key results, relevance, and source.
- A short narrative summary of the field landscape.
- Optional downloaded arXiv PDFs under `papers/`, `literature/`, or the user-specified directory.

## Helper Scripts

- [research-lit/scripts/arxiv_fetch.py](./research-lit/scripts/arxiv_fetch.py): bundled arXiv Atom API search and PDF download helper.

## Installable Directory

The installable Codex skill is:

```text
research-lit/research-lit/
```

Do not install the outer `research-lit/` folder. It contains repository README files only.

## Contents

- `research-lit/SKILL.md`: literature review workflow.
- `research-lit/scripts/`: deterministic helper scripts bundled with the skill.
- `research-lit/agents/openai.yaml`: UI metadata for Codex skill lists.
