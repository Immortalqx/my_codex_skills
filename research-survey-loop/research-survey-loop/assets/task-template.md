# Task Document: {{TOPIC}}

## Task Definition

- Topic: {{TOPIC}}
- Task slug: {{TOPIC_SLUG}}
- Created at: {{CREATED_AT}}
- Workspace root: {{WORKSPACE_ROOT}}
- Task directory: {{TASK_DIR}}

## Core Goals

- Produce a long-running, append-only Markdown survey at `./survey.md`
- Default research scope: embodied AI, computer vision, robotics, and adjacent topics
- Prefer formal published sources from the web first; supplement with arXiv and the local papers pool

## Fixed Constraints

- `task.md` stays stable by default; only modify it when the user explicitly changes the task itself
- `round_log.md` is append-only; do not rewrite history
- `current_task.md` is rewritten at the end of each round
- `survey.md` grows by category paragraphs only; do not produce per-paper cards
- All local citations must use relative paths
- Use web links for sources that cannot be downloaded
- Never read more than 10 PDF pages in a single pass

## Priority Sources

- Nature / Science and related journals
- CVPR / ICCV / ECCV / TPAMI / IJCV
- Science Robotics / IJRR / TRO / RA-L / RSS / ICRA / CoRL / IROS
- arXiv
- Local PDFs in workspace root `papers/` that are directly related to the task

## Inclusion Criteria

- Papers must be directly related to the topic, or provide clear value for category mapping, terminology unification, or method comparison
- Before writing into `survey.md`, clearly understand: research problem, core method, main contribution, key limitation
- Papers in local `papers/` absorbed by the task must be migrated to `./sources/papers/`

## Exclusions

- Papers clearly unrelated to the topic
- Content written as firm conclusions after only reading the title or partial abstract
- Continuing to cite root `papers/` as canonical paths in `survey.md`
- Mixing `industry_report/` into the academic main survey without explicit user request

## Output Requirements

- Main survey file: `./survey.md`
- Round log: `./round_log.md`
- Current task: `./current_task.md`
- Papers and supplementary material: `./sources/`

## Initial Classification Suggestions

- Start with coarse categories, then refine progressively
- Example categories: survey and field overview / world models / spatial memory / 3D scene representation / navigation / manipulation / benchmarks / evaluation

## Quality Standards

- Conclusions traceable to a local PDF or web link
- Consistent terminology across rounds
- Each round has a clear next-round entry point
- Classification structure becomes progressively clearer, not more scattered
