# grant-proposal

Chinese version: [README.zh-CN.md](./README.zh-CN.md)

`grant-proposal` turns research ideas and literature into structured grant applications. It supports KAKENHI, NSF, NSFC, ERC, DFG, SNSF, ARC, NWO, and generic proposal formats.

Use `$grant-proposal` when you want Codex to draft a funding proposal from a research direction:

```text
Use $grant-proposal to draft an NSFC Youth proposal from this research idea.
```

## Dependency Note

No local API key is required. The skill works from the user's request, local project files, and public literature or funder pages when network access is available.

## Workflow

1. Detect grant agency, subtype, language, and output format.
2. Gather project idea, PI background, literature, and related funded projects.
3. Structure aims, milestones, feasibility, risks, outputs, and budget rationale.
4. Draft the proposal in agency-specific style.
5. Self-check against agency criteria and revise obvious weaknesses.
6. Write proposal outputs, notes, and simple recovery state.

## Contents

- `grant-proposal/SKILL.md`: Codex skill definition.
- `grant-proposal/agents/openai.yaml`: UI metadata.
