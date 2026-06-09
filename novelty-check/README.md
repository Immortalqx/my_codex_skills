# novelty-check

Chinese version: [README.zh-CN.md](./README.zh-CN.md)

`novelty-check` verifies whether a research idea or method has already been done in recent literature. It extracts core technical claims, searches for overlapping work, and produces a brutally honest novelty assessment.

Use `$novelty-check` before spending implementation time on a new idea:

```text
Use $novelty-check to check whether this method idea has already been done.
```

## Dependency Note

No local API key is required. The skill uses public search results and publicly accessible paper pages when network access is available.

## Workflow

1. Extract 3-5 core technical claims from the proposed idea.
2. Search arXiv, Google Scholar, Semantic Scholar, and recent top venues.
3. Read abstracts and related-work sections for potentially overlapping papers.
4. Compare the proposed idea against the closest prior work from the collected evidence.
5. Produce a novelty score, closest prior work table, recommendation, and positioning advice.

## Contents

- `novelty-check/SKILL.md`: Codex skill definition.
- `novelty-check/agents/openai.yaml`: UI metadata.
