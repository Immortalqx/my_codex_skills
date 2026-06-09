---
name: arxiv
description: Search, download, and summarize academic papers from arXiv. Use when user says "search arxiv", "download paper", "fetch arxiv", "arxiv search", "get paper pdf", or wants to find and save papers from arXiv to the local paper library.
---

# arXiv Paper Search & Download

Search topic or arXiv paper ID: $ARGUMENTS

## Constants

- **PAPER_DIR** - Local directory to save downloaded PDFs. Default: `papers/` in the current project directory.
- **MAX_RESULTS = 10** - Default number of search results.
- **FETCH_SCRIPT** - `scripts/arxiv_fetch.py` inside this skill directory. When running from this repository instead of an installed skill, use `arxiv/arxiv/scripts/arxiv_fetch.py`.

Overrides can be appended to arguments:

- `/arxiv "attention mechanism" - max: 20` - return up to 20 results.
- `/arxiv "2301.07041" - download` - download a specific paper by ID.
- `/arxiv "query" - dir: literature/` - save PDFs to a custom directory.
- `/arxiv "query" - download: all` - download PDFs for all listed results.

## Workflow

### Step 1: Parse Arguments

Parse `$ARGUMENTS` for directives:

- **Query or ID**: main search term or a bare arXiv ID such as `2301.07041` or `cs/0601001`.
- **`- max: N`**: override `MAX_RESULTS`.
- **`- dir: PATH`**: override `PAPER_DIR`.
- **`- download`**: download the first result's PDF after listing.
- **`- download: all`**: download PDFs for all results.

If the argument matches an arXiv ID pattern (`YYMM.NNNNN` or `category/NNNNNNN`), skip broad search and fetch that paper directly.

### Step 2: Locate the Helper Script

Prefer the helper bundled with this skill. Resolve it relative to the skill directory, not the user's current project:

```bash
python scripts/arxiv_fetch.py --help
```

When the skill is being inspected or tested from this repository before installation, run:

```bash
python arxiv/arxiv/scripts/arxiv_fetch.py --help
```

If the helper script is unavailable in an unusual install, fall back to the inline arXiv Atom API snippets below.

### Step 3: Search arXiv

With the helper script:

```bash
python scripts/arxiv_fetch.py search "QUERY" --max MAX_RESULTS
```

Fallback inline Python:

```bash
python - <<'PYEOF'
import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

NS = "http://www.w3.org/2005/Atom"
query = urllib.parse.quote("QUERY")
url = (f"http://export.arxiv.org/api/query"
       f"?search_query={query}&start=0&max_results=MAX_RESULTS"
       f"&sortBy=relevance&sortOrder=descending")
with urllib.request.urlopen(url, timeout=30) as r:
    root = ET.fromstring(r.read())
papers = []
for entry in root.findall(f"{{{NS}}}entry"):
    aid = entry.findtext(f"{{{NS}}}id", "").split("/abs/")[-1].split("v")[0]
    title = (entry.findtext(f"{{{NS}}}title", "") or "").strip().replace("\n", " ")
    abstract = (entry.findtext(f"{{{NS}}}summary", "") or "").strip().replace("\n", " ")
    authors = [a.findtext(f"{{{NS}}}name", "") for a in entry.findall(f"{{{NS}}}author")]
    published = entry.findtext(f"{{{NS}}}published", "")[:10]
    cats = [c.get("term", "") for c in entry.findall(f"{{{NS}}}category")]
    papers.append({
        "id": aid,
        "title": title,
        "authors": authors,
        "abstract": abstract,
        "published": published,
        "categories": cats,
        "pdf_url": f"https://arxiv.org/pdf/{aid}.pdf",
        "abs_url": f"https://arxiv.org/abs/{aid}",
    })
print(json.dumps(papers, ensure_ascii=False, indent=2))
PYEOF
```

Present results as a compact table:

```text
| # | arXiv ID   | Title               | Authors        | Date       | Category |
|---|------------|---------------------|----------------|------------|----------|
| 1 | 2301.07041 | Attention Is All... | Vaswani et al. | 2017-06-12 | cs.LG    |
```

### Step 4: Fetch Details for a Specific ID

When a single paper ID is requested:

```bash
python scripts/arxiv_fetch.py search "id:ARXIV_ID" --max 1
```

Display title, all authors, categories, full abstract, published date, PDF URL, and abstract URL.

### Step 5: Download PDFs

When download is requested, for each paper ID:

```bash
python scripts/arxiv_fetch.py download ARXIV_ID --dir PAPER_DIR
```

The helper script:

- Creates `PAPER_DIR` automatically.
- Saves old-style IDs such as `cs/0601001` as `cs_0601001.pdf`.
- Skips existing PDFs instead of overwriting them.
- Rejects files smaller than 10 KB because they are likely error pages.
- Sleeps for 1 second after downloads and retries once after 5 seconds on HTTP 429.

Fallback inline Python:

```bash
mkdir -p PAPER_DIR && python -c "
import pathlib
import sys
import urllib.request

out = pathlib.Path('PAPER_DIR/ARXIV_ID.pdf')
if out.exists():
    print(f'Already exists: {out}')
    sys.exit(0)
req = urllib.request.Request(
    'https://arxiv.org/pdf/ARXIV_ID.pdf',
    headers={'User-Agent': 'arxiv-skill/1.0'},
)
with urllib.request.urlopen(req, timeout=60) as r:
    data = r.read()
if len(data) < 10240:
    raise SystemExit(f'File too small: {len(data)} bytes')
out.write_bytes(data)
print(f'Downloaded: {out} ({out.stat().st_size // 1024} KB)')
"
```

### Step 6: Summarize

For each paper:

```markdown
## [Title]

- **arXiv**: [ID] - [abs_url]
- **Authors**: [full author list]
- **Date**: [published]
- **Categories**: [cs.LG, cs.AI, ...]
- **Abstract**: [full abstract]
- **Key contributions**:
  - [contribution 1]
  - [contribution 2]
  - [contribution 3]
- **Local PDF**: papers/[ID].pdf (if downloaded)
```

### Step 7: Final Output

Summarize what was done:

- `Found N papers for "query"`.
- `Downloaded: papers/2301.07041.pdf (842 KB)` for each download.
- Any warnings, including rate limits, API errors, tiny files, or already-existing PDFs.

Suggest follow-up skills only when relevant:

```text
/research-lit "topic"     - multi-source review: Zotero + Obsidian + local PDFs + web
/novelty-check "idea"     - verify an idea against these papers
```

## Key Rules

- Always show the arXiv ID prominently for citations and reproducibility.
- Verify downloaded PDFs are larger than 10 KB.
- Never overwrite an existing PDF at the same path.
- Handle both new (`2301.07041`) and old (`cs/0601001`) arXiv ID formats.
- Create `PAPER_DIR` automatically when downloading.
- Keep all task output in stdout and user-requested PDF files only. Do not create logs, caches, or debug JSON as skill results.
- If the arXiv API is unreachable, report the error clearly and suggest `/research-lit "topic" - sources: web` as a fallback.
