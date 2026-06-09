# alphaxiv

Chinese version: [README.zh-CN.md](./README.zh-CN.md)

`alphaxiv` is a quick single-paper lookup skill for arXiv papers. It uses public AlphaXiv Markdown pages first, then falls back to full AlphaXiv Markdown or arXiv LaTeX source when the question needs more detail.

Use `$alphaxiv` when you want Codex to quickly explain one paper from an arXiv ID or URL:

```text
Use $alphaxiv to explain https://arxiv.org/abs/2401.12345 and focus on the method.
```

## Dependency Note

No local API key is required. The skill depends on public access to:

- `https://alphaxiv.org/overview/<paper-id>.md`
- `https://alphaxiv.org/abs/<paper-id>.md`
- `https://arxiv.org/src/<paper-id>`

If AlphaXiv has not processed a paper, the skill falls back to deeper public sources.

## Workflow

1. Extract a clean arXiv paper ID from a bare ID, arXiv URL, PDF URL, or AlphaXiv URL.
2. Fetch the AlphaXiv overview first.
3. Escalate to full AlphaXiv Markdown only when the overview is insufficient.
4. Escalate to arXiv LaTeX source only for equations, proofs, appendix details, or implementation details.
5. Return a concise answer with the source depth used.

## Contents

- `alphaxiv/SKILL.md`: Codex skill definition.
- `alphaxiv/agents/openai.yaml`: UI metadata.
