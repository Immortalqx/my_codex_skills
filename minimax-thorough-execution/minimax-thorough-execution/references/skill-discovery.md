# Skill Discovery

Use this reference when deciding whether to stay with direct commands or delegate part of the task to installed skills or plugins.

## When To Search For Skills

Search the current environment for relevant installed skills, plugins, or specialized workflows when the task involves:

- retrieval or downloading
- reading or research
- parsing or transformation
- browser work
- document handling
- spreadsheets
- presentations
- diagrams
- images
- other specialized workflows with existing local support

## Delegation Rules

- if no relevant skill exists, continue with the best direct fallback
- if one relevant skill exists and covers the needed operation, use it
- if multiple relevant skills exist, use one or more of them when they materially improve execution fidelity or coverage
- do not assume only one skill may apply to the task
- do not commit to a generic workflow before checking whether better local skills already exist
- do not replace a relevant installed skill with `wget`, `curl`, one-off scripts, or shallow manual search merely because those are faster or shorter
- if a relevant skill is unavailable, insufficient, or fails, note that briefly in task notes or the completion audit and then use a direct fallback

## Logging The Decision

When relevant:

- note which installed skills were considered
- note which skill or skills were actually used
- if no skill was used, note why

Valid short reasons include:

- `not applicable`
- `no relevant skill found`
- `relevant skill unavailable`
- `relevant skill insufficient`
- `fallback used after skill failure`
