---
name: alphaxiv
description: Quick single-paper lookup via AlphaXiv LLM-optimized summaries with tiered source fallback. Use when user says "explain this paper", "summarize paper", pastes an arXiv/AlphaXiv URL, or provides a bare arXiv ID for quick understanding - not for broad literature search.
---

# AlphaXiv Paper Lookup

Lookup paper: $ARGUMENTS

> Quick single-paper reader with tiered source fallback (overview → full markdown → LaTeX source). Powered by [AlphaXiv](https://alphaxiv.org).

## Role & Positioning

This skill is a **quick single-paper reader** for one known arXiv paper. It is
best when the user provides a bare arXiv ID, an arXiv URL, a PDF URL, or an
AlphaXiv URL and wants a concise explanation without running a broad literature
survey.

## Constants

- **OVERVIEW_URL** = `https://alphaxiv.org/overview/{PAPER_ID}.md`
- **ABS_URL** = `https://alphaxiv.org/abs/{PAPER_ID}.md`
- **ARXIV_SRC_URL** = `https://arxiv.org/src/{PAPER_ID}`

> Overrides (append to arguments):
> - `/alphaxiv 2401.12345` — quick overview
> - `/alphaxiv "https://arxiv.org/abs/2401.12345"` — auto-extract ID
> - `/alphaxiv 2401.12345 - depth: src` — force LaTeX source inspection
> - `/alphaxiv 2401.12345 - depth: abs` — force full markdown

## Workflow

### Step 1: Parse Arguments & Extract Paper ID

Parse `$ARGUMENTS` to extract a bare arXiv paper ID. Accept these input formats:

- `https://arxiv.org/abs/2401.12345` or `https://arxiv.org/abs/2401.12345v2`
- `https://arxiv.org/pdf/2401.12345`
- `https://alphaxiv.org/overview/2401.12345`
- `https://alphaxiv.org/abs/2401.12345`
- `2401.12345` or `2401.12345v2`

Strip version suffixes (`v1`, `v2`, ...) for API calls. Store as `PAPER_ID`.

Parse optional directives:
- **`- depth: overview|abs|src`**: force a specific tier instead of cascading

### Step 2: Fetch AlphaXiv Overview (Tier 1 — Fastest)

Fetch the structured overview from `https://alphaxiv.org/overview/{PAPER_ID}.md`.

This returns a **structured, LLM-optimized report** designed for machine consumption. Use this as the default and preferred source.

If the overview answers the user's question, **stop here**. Do not fetch deeper tiers unnecessarily.

If the request fails (HTTP 404 — paper not yet processed) or the content is insufficient, proceed to Step 3.

### Step 3: Fetch Full AlphaXiv Markdown (Tier 2 — More Detail)

Fetch the full paper markdown from `https://alphaxiv.org/abs/{PAPER_ID}.md`.

This provides the full paper body as markdown. Use when the user needs:
- Specific methodology details
- Detailed experimental results
- Particular sections not covered in the overview

If this still does not answer the question, proceed to Step 4.

### Step 4: Fetch arXiv LaTeX Source (Tier 3 — Deepest)

When the overview and full markdown are both insufficient (e.g., the user asks about equations, proofs, appendix details, or implementation specifics), download the paper's LaTeX source from `https://arxiv.org/src/{PAPER_ID}`.

The source is a `.tar.gz` archive. Download it to a temporary directory, extract it, and list the `.tex` files inside.

Then inspect **only** the files needed to answer the question. Prioritize:

1. Top-level `*.tex` files (usually the main document)
2. Files referenced by `\input{}` or `\include{}`
3. Appendices, tables, or sections directly related to the user's question

**Do NOT read the entire source tree by default.** Read selectively.

Temporary source artifacts live under `/tmp`. Do not rely on persistence.

### Step 5: Present Results

#### Default Answer Shape

```markdown
## [Paper Title]

- **arXiv**: [PAPER_ID] — https://arxiv.org/abs/[PAPER_ID]
- **Source depth**: overview | abs | src

### Summary
[2-3 sentence summary]

### Key Points
- [point 1]
- [point 2]
- [point 3]

### Answer to Your Question
[Direct answer if the user asked a specific question]
```

If the user only asks for one specific detail, answer it directly — skip the full template.

## Key Rules

- **Overview first**: `overview` is the fastest path and must always be tried before deeper tiers. Only escalate when needed.
- **Minimal reads**: At `src` tier, read only the files that answer the question. Full-tree reads waste tokens.
- **Cross-platform**: When downloading and extracting the source archive, prefer cross-platform approaches (e.g., Python stdlib) over platform-specific commands to ensure Windows/WSL compatibility.
- **No PDF parsing**: This skill reads structured markdown and LaTeX source, not raw PDFs. If the user needs PDF-specific content, report that this standalone skill does not parse PDFs.
- **Rate limiting**: arXiv source download may rate-limit. If HTTP 429 occurs, wait 5 seconds and retry once. If still blocked, report the error clearly.

## Standalone Scope

The only external dependency is public network access to AlphaXiv and arXiv.
