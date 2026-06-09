---
name: research-wiki
description: "Persistent research knowledge base that accumulates papers, ideas, experiments, claims, and their relationships across a project. Inspired by Karpathy's LLM Wiki pattern. Use when user says \"知识库\", \"research wiki\", \"add paper\", \"wiki query\", \"查知识库\", or wants to build/query a persistent field map."
---

# Research Wiki: Persistent Research Knowledge Base

Subcommand: **$ARGUMENTS**

## Overview

The research wiki is a persistent, per-project knowledge base that accumulates structured knowledge across papers, ideas, experiments, claims, and their relationships.

Unlike one-off literature notes that are forgotten after a session, the wiki compounds: every paper page, experiment page, failed idea, and explicit relationship becomes reusable context for later work.

Inspired by [Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f): compile knowledge once, keep it current, do not re-derive the same field map every time.

## Core Concepts

### Four Entity Types

| Entity | Directory | Node ID format | What it represents |
| --- | --- | --- | --- |
| **Paper** | `papers/` | `paper:<slug>` | A published or preprint research paper |
| **Idea** | `ideas/` | `idea:<id>` | A research idea, whether active, failed, or partial |
| **Experiment** | `experiments/` | `exp:<id>` | A concrete experiment run with evidence |
| **Claim** | `claims/` | `claim:<id>` | A testable scientific claim with evidence status |

### Typed Relationships (`graph/edges.jsonl`)

| Edge type | From -> To | Meaning |
| --- | --- | --- |
| `extends` | paper -> paper | Builds on prior work |
| `contradicts` | paper -> paper | Disagrees with results or claims |
| `addresses_gap` | paper\|idea -> gap | Targets a known field gap |
| `inspired_by` | idea -> paper | Idea came from this paper |
| `tested_by` | idea\|claim -> exp | Tested in this experiment |
| `supports` | exp -> claim\|idea | Experiment supports a claim or idea |
| `invalidates` | exp -> claim\|idea | Experiment disproves a claim or idea |
| `supersedes` | paper -> paper | Newer work replaces older work |

Edges live in `graph/edges.jsonl`. The `## Connections` section on each page is a human-readable projection of that graph and should not be hand-maintained as a second source of truth.

## Wiki Directory Structure

```text
research-wiki/
  index.md
  log.md
  gap_map.md
  query_pack.md
  papers/
    <slug>.md
  ideas/
    <idea_id>.md
  experiments/
    <exp_id>.md
  claims/
    <claim_id>.md
  graph/
    edges.jsonl
```

## Subcommands

### `/research-wiki init`

Initialize the wiki for the current project:

1. create the `research-wiki/` directory structure
2. create empty `index.md`, `log.md`, `gap_map.md`, `query_pack.md`
3. create empty `graph/edges.jsonl`
4. append an initialization entry to `log.md`

### `/research-wiki ingest "<paper title>" - arxiv: <id>`

Add a paper to the wiki with the bundled helper:

```bash
# arXiv-based ingest
python scripts/research_wiki.py ingest_paper research-wiki/ \
    --arxiv-id 2501.12345 --thesis "One-line claim from abstract."

# manual metadata ingest
python scripts/research_wiki.py ingest_paper research-wiki/ \
    --title "Attention Is All You Need" \
    --authors "Ashish Vaswani, Noam Shazeer" \
    --year 2017 --venue "NeurIPS"

# add an explicit relationship after ingest
python scripts/research_wiki.py add_edge research-wiki/ \
    --from "paper:vaswani2017_attention_all_you" \
    --to "paper:chen2025_factorized_gap" \
    --type "extends" --evidence "Section 3.2 adapts the encoder block."
```

The helper performs:

1. metadata fetch when `--arxiv-id` is provided
2. slug generation
3. de-duplication
4. page creation or update
5. `index.md` rebuild
6. `query_pack.md` rebuild
7. `log.md` append

### `/research-wiki sync - arxiv-ids <id1>,<id2>,...`

Batch backfill one or more arXiv IDs:

```bash
python scripts/research_wiki.py sync research-wiki/ \
    --arxiv-ids 2310.06770,1706.03762

python scripts/research_wiki.py sync research-wiki/ --from-file ids.txt
```

Use this when papers were discussed earlier but not yet ingested. `sync` does not depend on hidden hooks or session traces; it only ingests the IDs you explicitly provide.

### Paper Page Schema

The bundled helper emits this schema for paper pages:

```markdown
---
type: paper
node_id: paper:<slug>
title: "<full title>"
authors: ["First A. Author", "Second B. Author"]
year: 2025
venue: "arXiv"
external_ids:
  arxiv: "2501.12345"
  doi: null
  s2: null
tags: ["tag1", "tag2"]
added: 2026-04-07T10:12:00Z
---

# <full title>

## One-line thesis

## Problem / Gap

## Method

## Key Results

## Assumptions

## Limitations / Failure Modes

## Reusable Ingredients

## Open Questions

## Claims

## Connections

## Relevance to This Project
```

If the paper was ingested with `--arxiv-id` and the API returned an abstract, the helper appends `## Abstract (original)` at the end.

### `/research-wiki query "<topic>"`

Generate `query_pack.md`, a compressed context file for later ideation, planning, or quick re-entry into the project.

**Fixed budget (max 8000 chars / about 2000 tokens):**

| Section | Budget | Content |
| --- | --- | --- |
| Project direction | 300 chars | From `RESEARCH_BRIEF.md` if present |
| Top gaps | 1200 chars | From `gap_map.md` |
| Paper clusters | 1600 chars | Compact cluster summary |
| Failed ideas | 1400 chars | High-value anti-repetition memory |
| Top papers | 1800 chars | Most central / relevant paper pages |
| Active chains | 900 chars | Important relationship chains |
| Open unknowns | 500 chars | Unresolved questions |

Prune low-ranked paper detail first. Do not prune failed ideas first.

### `/research-wiki update <node_id> - <field>: <value>`

Update a specific entity and then rebuild the compact artifacts:

```text
/research-wiki update paper:chen2025 - relevance: core
/research-wiki update idea:001 - outcome: negative
/research-wiki update claim:C1 - status: invalidated
```

After every update, rebuild `query_pack.md` and append to `log.md`.

### `/research-wiki lint`

Health check the wiki:

1. orphan pages
2. stale claims
3. contradictory evidence
4. papers that probably need explicit links
5. dead ideas
6. sparse pages

Write the result to `LINT_REPORT.md`.

### `/research-wiki stats`

Produce a quick project overview:

```text
Research Wiki Stats
Papers: 28
Ideas: 7
Experiments: 12
Claims: 15
Edges: 64
```

## Operating Style

- Treat the wiki as a local source of truth for project memory.
- Keep entity pages readable by humans first, structured enough for scripted rebuilds second.
- Record failed ideas explicitly; they are valuable memory.
- Use canonical node IDs consistently.
- Append to `log.md` for every mutation.
- Keep `query_pack.md` deterministic and compact rather than open-ended.

## Optional Diagnostic

If you want a rough coverage check for arXiv IDs mentioned in local project artifacts, run:

```bash
bash scripts/verify_wiki_coverage.sh research-wiki/
```

This is diagnostic only. It should report gaps, not block the wiki.
