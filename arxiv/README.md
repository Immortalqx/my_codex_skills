# arxiv

Chinese version: [README.zh-CN.md](./README.zh-CN.md)

`arxiv` is a Codex skill for searching arXiv, fetching metadata for specific arXiv IDs, and downloading paper PDFs into a local paper library.

Use `$arxiv` when you want Codex to find preprints, get a PDF by arXiv ID, or save relevant arXiv papers under `papers/` or a custom directory:

```text
Use $arxiv to search for recent papers about test-time scaling and download the top relevant PDF into papers/.
```

For a known paper:

```text
Use $arxiv to fetch 2301.07041 and download the PDF into literature/.
```

## Workflow

1. Codex parses the query, arXiv ID, result limit, output directory, and download mode.
2. Codex runs the bundled helper at `arxiv/scripts/arxiv_fetch.py` inside the installable skill.
3. Search results are returned as structured metadata: arXiv ID, title, authors, abstract, dates, categories, PDF URL, and abstract URL.
4. When download is requested, PDFs are saved to `papers/` by default or to the requested directory.
5. Existing PDFs are skipped rather than overwritten, and tiny downloads are rejected as likely error pages.

## Outputs

- Search results printed in the conversation.
- Optional downloaded PDFs under `papers/` or the user-specified directory.

The skill does not persist search logs, debug JSON, or cache files as task results.

## Helper Script

- [arxiv/scripts/arxiv_fetch.py](./arxiv/scripts/arxiv_fetch.py): small CLI for arXiv Atom API search and PDF download.

Example direct usage from the installable skill directory:

```bash
python scripts/arxiv_fetch.py search "diffusion policy" --max 10
python scripts/arxiv_fetch.py search "id:2301.07041" --max 1
python scripts/arxiv_fetch.py download 2301.07041 --dir papers
```

## Repository Structure

- `README.md` and `README.zh-CN.md`: repository-facing documentation.
- `arxiv/`: installable Codex skill directory.
- `arxiv/SKILL.md`: skill definition.
- `arxiv/scripts/`: deterministic helper code.
- `arxiv/agents/`: skill UI metadata.
