---
name: "research-lit"
description: "Search and analyze research papers, find related work, summarize key ideas. Use when user says \"find papers\", \"related work\", \"literature review\", \"what does this paper say\", or needs to understand academic papers."
---

# Research Literature Review

Research topic: `$ARGUMENTS`

## Purpose

Use this skill to build a grounded paper landscape from:

1. local PDFs already present in the workspace,
2. public web search and official paper pages,
3. structured arXiv metadata from the bundled helper script.

This skill is intentionally standalone. Its default path uses only local PDFs, public web search, and the bundled arXiv helper.

## Runtime Knobs

- **PAPER_LIBRARY** Search these locations in order:
  1. a path explicitly provided by the user, e.g. `paper library: ~/my_papers/`
  2. `papers/` in the current project
  3. `literature/` in the current project
- **MAX_LOCAL_PAPERS = 20** Maximum number of local PDFs to read at the title / abstract / intro level.
- **ARXIV_DOWNLOAD = false** When `true`, download the top relevant arXiv PDFs after ranking.
- **ARXIV_MAX_DOWNLOAD = 5** Maximum number of arXiv PDFs to download.

## Argument Directives

Parse `$ARGUMENTS` for optional directives:

- `paper library: <path>`
- `sources: local`
- `sources: web`
- `sources: local, web`
- `sources: all`
- `arxiv download: true`
- `max download: <N>`

If `sources:` is not specified, default to `all`.

Examples:

```text
/research-lit "diffusion models"
/research-lit "diffusion models" - sources: local
/research-lit "diffusion models" - sources: web
/research-lit "diffusion models" - sources: local, web
/research-lit "test-time scaling for VLM agents" - sources: all - arxiv download: true - max download: 8
```

## Source Table

| Priority | Source | ID | Detection | What it provides |
| --- | --- | --- | --- | --- |
| 1 | Local PDFs | `local` | `papers/**/*.pdf`, `literature/**/*.pdf`, or a user-provided library path | Existing papers the user already has |
| 2 | Web search | `web` | Current agent web tools or direct HTTP access | Official paper pages, OpenReview, author pages, Semantic Scholar pages, venue pages |
| 3 | Bundled arXiv helper | `arxiv` | `scripts/arxiv_fetch.py` inside this skill | Structured metadata and optional PDF download |

## Workflow

### Step 0: Scan Local Papers First

Before going outward, check whether the user already has relevant papers locally.

1. Locate the paper library.
2. Enumerate candidate PDFs under `papers/` / `literature/` or the user-provided path.
3. Filter by filename relevance first.
4. For promising PDFs, read the first 3 pages and extract:
   - title
   - authors
   - year
   - venue if visible
   - one-line core contribution
   - why it matters to the current topic
5. Build a "local papers already available" section.

If no relevant local papers are found, continue normally.

### Step 1: Search the Web

Search the public web for recent and canonical papers on the topic.

Preferred targets:

- official conference or journal pages
- OpenReview
- arXiv abstract pages
- author project pages
- Semantic Scholar result pages

Rules:

- Prefer the published venue page when both a venue version and an arXiv mirror exist.
- Use arXiv or author pages when they are the most accessible legal source.
- Focus on the last 2 years unless the topic clearly requires older foundational work.
- De-duplicate against the local-paper set.

### Step 2: Run the Bundled arXiv Helper

Always run the local helper for a structured arXiv pass:

```bash
python scripts/arxiv_fetch.py search "QUERY" --max 10
```

This returns richer structured data than a generic search snippet:

- title
- abstract
- author list
- categories
- published / updated dates
- abstract URL
- PDF URL

Merge the arXiv results with the web-search findings and de-duplicate.

Optional PDF download, only when `ARXIV_DOWNLOAD = true`:

```bash
python scripts/arxiv_fetch.py download ARXIV_ID --dir papers/
```

Download rules:

- only download the top `ARXIV_MAX_DOWNLOAD` items
- skip papers already present locally
- verify each PDF is larger than 10 KB

### Step 3: Analyze Each Relevant Paper

For each paper retained after de-duplication, extract:

- **Problem**: what gap does it address?
- **Method**: what is the core technical contribution?
- **Results**: what numbers or concrete claims matter?
- **Relevance**: how does it relate to the current task?
- **Source**: `local`, `web`, or `arxiv`

### Step 4: Synthesize the Landscape

- group papers by method family or research theme
- identify consensus, disagreement, and open gaps
- distinguish directly competing work from supporting context
- surface what is genuinely new versus what is already standard

### Step 5: Output

Present a structured table:

```text
| Paper | Venue | Method | Key Result | Relevance to Us | Source |
|-------|-------|--------|------------|-----------------|--------|
```

Then add a short narrative summary of the field:

- what the main clusters are
- what recent trends changed
- where the strongest baselines come from
- what the current blind spots appear to be

### Step 6: Save Artifacts When Requested

If the user wants files:

- save PDFs into `papers/`, `literature/`, or the specified library path
- save the literature note or comparison note in the workspace

## Key Rules

- Always include citation metadata: authors, year, venue or preprint status.
- Always separate peer-reviewed papers from preprints when it matters.
- Never fake certainty about novelty or claim strength.
- Never assume another installed skill is required for the default path.
- Use the bundled `scripts/arxiv_fetch.py` helper instead of external install paths.
- If one source is missing or weak, continue with the others instead of failing.
