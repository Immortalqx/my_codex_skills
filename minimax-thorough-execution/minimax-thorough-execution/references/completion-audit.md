# Completion Audit

Use this reference when preparing the final audit before answering.

## Minimum Checks

Audit at minimum:

- prompt obedience
- scope completeness
- skill search and delegation
- temp artifact layout
- source map updates
- local artifact re-read when the task continued across turns
- body, appendix, and supplement coverage when relevant
- visual verification when relevant
- search and original links when relevant

If the audit finds a gap, resolve the gap before answering. If the gap cannot be resolved, state it explicitly.

## Default Audit Block

```text
Completion audit:
- Prompt obedience: checked | blocked
- Scope: checked | narrowed | blocked
- Skill search and delegation: checked | not applicable | blocked
- Temp artifact layout: checked | blocked
- Source map: checked | not applicable | blocked
- Local artifact re-read: checked | not applicable | blocked
- Body/appendix/supplement: checked | not applicable | blocked
- Visual verification: checked | not applicable | blocked
- Search and links: checked | not applicable | blocked
```

## Audit Rules

- keep the audit short
- do not fabricate a `checked` status
- use `not applicable` only when a category truly does not apply
- use `blocked` when the category could not be completed
- if the user requires a very strict output shape, compress the audit to one short line instead of omitting it
