---
name: grant-proposal
description: "Draft a structured grant proposal from research ideas and literature. Supports KAKENHI (Japan), NSF (US), NSFC (China, including 面上/青年/优青/杰青/海外优青/重点), ERC (EU), DFG (Germany), SNSF (Switzerland), ARC (Australia), NWO (Netherlands), and generic formats. Use when user says \"write grant\", \"grant proposal\", \"申請書\", \"write KAKENHI\", \"科研費\", \"基金申请\", \"写基金\", \"NSF proposal\", or wants to turn research ideas into a funding application."
---

# Grant Proposal

Draft a grant proposal based on: **$ARGUMENTS**

## Standalone Scope

This skill works from the user's request, local project files, and any publicly
accessible literature or funder pages that can be reached in the current
environment.

No local API key is required by this skill. If network access is unavailable,
continue from user-provided materials and clearly mark literature or funded-project
coverage gaps.

## Defaults

- **GRANT_TYPE = `KAKENHI`** unless the request names another agency.
- **GRANT_SUBTYPE = `auto`** from the request or the most common subtype.
- **OUTPUT_FORMAT = `markdown`** unless `latex` is requested.
- **OUTPUT_DIR = `grant-proposal/`** for generated files.
- **LANGUAGE = `auto`**:
  - KAKENHI -> Japanese
  - NSFC -> Chinese
  - NSF/ERC/DFG/SNSF/ARC/NWO -> English unless requested otherwise
  - GENERIC -> match the user's language
- **AUTO_PROCEED = false**. Stop at major planning checkpoints unless the user
  explicitly asks for a complete one-shot draft.

Supported grant types:

| Type | Common Sections | Notes |
|---|---|---|
| `KAKENHI` | 研究目的, 研究計画・方法, 準備状況, 人権の保護 if applicable | Formal Japanese academic style; emphasize academic significance, originality, feasibility, and societal value. |
| `NSF` | Project Summary, Project Description, References, Biosketch, Budget Justification, Data Management Plan | Explicit Intellectual Merit and Broader Impacts. |
| `NSFC` | 立项依据, 研究内容, 研究目标, 研究方案, 可行性分析, 创新点, 预期成果, 研究基础 | Formal Chinese; position against the international frontier and applicant foundation. |
| `ERC` | Extended Synopsis, Scientific Proposal Part B2 | High-risk/high-gain framing, work packages, deliverables, milestones. |
| `DFG` | State of the Art, Objectives, Work Programme, Bibliography, CV | English or German depending on request. |
| `SNSF` | Summary, Research Plan, Timetable, Budget | Scientific relevance, originality, feasibility, track record. |
| `ARC` | Project Description, Feasibility, Benefit, Budget | Research quality, feasibility, and benefit. |
| `NWO` | Summary, Proposed Research, Knowledge Utilisation | Scientific quality, innovation, knowledge utilisation. |
| `GENERIC` | User-provided or inferred sections | Ask for page limits and required sections if unknown. |

## Inputs to Gather

Read only what is useful for the requested proposal:

1. The research idea, draft, or direction from `$ARGUMENTS`.
2. Local files that look relevant, for example:
   - `IDEA_REPORT.md`, `FINAL_PROPOSAL.md`, `EXPERIMENT_PLAN.md`
   - `NARRATIVE_REPORT.md`, `STORY.md`, `literature.md`, `survey.md`
   - `publications.md`, `cv.md`, `bio.md`, `CV.pdf`
3. User-provided grant constraints:
   - agency, subtype, page limit, deadline, language, section template
   - PI stage, team, institution, budget range, project duration
4. Public sources if network access is available:
   - funder instructions and official criteria
   - recent papers and surveys in the area
   - funded-project databases for related awards

If critical PI-specific or budget information is missing, use explicit placeholders
such as `[TODO: add PI publications]` and `[AMOUNT]`. Never invent these details.

## Workflow

### Phase 1: Parse and Scope

Extract:

- grant agency and subtype
- output language and format
- project duration
- topic, method, application area, and expected contribution
- any hard requirements such as page limits or mandatory sections

If the request is too vague to draft responsibly, ask concise questions for the
missing grant type, project duration, PI background, or target language.

### Phase 2: Landscape and Gap

Build the proposal's positioning directly:

1. Summarize the research area in 5-8 bullets.
2. Identify the scientific or technical gap.
3. Search or inspect supplied literature for close work.
4. Search funded-project pages when relevant and available:
   - KAKENHI: KAKEN database
   - NSF: NSF Award Search
   - NSFC: public NSFC project information where accessible
   - other agencies: official award/project search or public web pages
5. Write a one-sentence gap statement:

```text
Despite progress in [X], [specific gap] remains unresolved because [reason].
This project addresses the gap by [approach], enabling [expected scientific or societal impact].
```

Checkpoint unless one-shot drafting was requested:

```markdown
## Positioning Checkpoint

- Grant type: [type/subtype]
- Proposed title: [working title]
- Gap statement: [gap]
- Closest related work/projects: [3-5 bullets]
- Proposed angle: [1-2 bullets]

Please confirm or adjust before I draft the proposal structure.
```

### Phase 3: Aims and Project Architecture

Design 2-4 aims. Each aim should be:

- independently valuable
- technically concrete
- feasible within the project duration
- linked to a deliverable
- paired with a risk and mitigation

Create an aims matrix:

```markdown
| Aim | Key Question | Approach | Evidence/Preparation | Risk | Mitigation | Deliverable |
|---|---|---|---|---|---|---|
| Aim 1 | ... | ... | ... | Low/Med/High | ... | ... |
```

Then create a timeline:

```markdown
| Period | Aim/Task | Milestone | Deliverable |
|---|---|---|---|
| Year 1 Q1-Q2 | ... | ... | ... |
```

Checkpoint unless one-shot drafting was requested:

```markdown
## Structure Checkpoint

- Aim 1: [title]
- Aim 2: [title]
- Aim 3: [title if any]
- Main risk: [risk]
- Timeline: [summary]

Proceed to full drafting, or revise the aims first?
```

### Phase 4: Draft the Proposal

Write complete prose in the agency-specific style. Do not leave outline-only
sections unless the user explicitly requested an outline.

Recommended drafting order:

1. Specific Aims / Research Objective
2. Background / Significance / State of the Art
3. Research Plan / Methods
4. Expected Outcomes and Deliverables
5. Timeline and Milestones
6. Risk Management and Alternative Plans
7. PI Qualification / Preparation Status
8. Budget Justification
9. Broader Impacts / Societal Significance / Knowledge Utilisation when required

For figures, create text placeholders unless the user asks you to generate them:

```markdown
[Figure 1: Overall project architecture showing Aim 1 -> Aim 2 -> Aim 3 and deliverables.]
[Figure 2: Timeline and milestones.]
```

If the user asks for figures, generate simple local SVG, Mermaid, draw.io, or
matplotlib figures directly in the project. Do not call another skill.

### Phase 5: Self-Check and Revise

Review the draft directly against the grant type's criteria:

- Does the opening state the gap early and clearly?
- Are aims concrete, feasible, and not mutually dependent in a fragile way?
- Are novelty and significance supported by cited literature or supplied evidence?
- Are risks and mitigation plans specific?
- Are deliverables measurable?
- Does the language match the agency style?
- Are budget amounts and PI credentials left as placeholders when unknown?
- Are all citations real or marked `[VERIFY]`?
- Are page-limit or required-section constraints respected?

Apply obvious fixes before presenting the final output. If a weakness cannot be
fixed without user information, mark it as a clear TODO.

## Output Files

Default Markdown output:

```text
grant-proposal/
├── GRANT_PROPOSAL.md
├── GRANT_NOTES.md
├── GRANT_STATE.json
├── references.bib
└── figures/
```

LaTeX output, if requested:

```text
grant-proposal/
├── main.tex
├── sections/
│   ├── aims.tex
│   ├── background.tex
│   ├── research_plan.tex
│   ├── timeline.tex
│   ├── pi_qualification.tex
│   └── budget.tex
├── references.bib
└── figures/
```

If overwriting an existing final file, preserve the previous version by writing a
timestamped copy first, for example `GRANT_PROPOSAL_YYYYMMDD_HHmmss.md`.

`GRANT_NOTES.md` should contain:

- assumptions
- missing user information
- literature/funded-project coverage limitations
- TODO placeholders to fill before submission

`GRANT_STATE.json` should contain only simple recovery metadata:

```json
{
  "grant_type": "NSFC",
  "grant_subtype": "Youth",
  "language": "Chinese",
  "status": "drafted",
  "last_updated": "YYYY-MM-DDTHH:MM:SS"
}
```

## Key Rules

- Do not fabricate budget amounts.
- Do not fabricate PI information, publications, awards, affiliations, or credentials.
- Do not hallucinate citations. Use supplied sources or publicly verified sources; otherwise mark `[VERIFY]`.
- Do not claim novelty from absence of evidence. If search coverage is weak, say so.
- Grant proposals argue for future work. Emphasize what will be done, why it matters, and why the team can execute it.
- Keep agency norms visible: KAKENHI expects 社会的意義, NSF expects Broader Impacts, NSFC expects 国际前沿 positioning and 研究基础.
- Stop for user confirmation at major checkpoints unless the user explicitly requested a one-shot full draft.

## Parameter Examples

```text
/grant-proposal "robotics foundation model safety — NSF CAREER, English, 5 years"
/grant-proposal "低空通信感知一体化 — NSFC 青年, 中文, 3 years"
/grant-proposal "multimodal robot planning — KAKENHI Start-up, Japanese"
```

| Parameter | Default | Description |
|---|---|---|
| `grant type` | KAKENHI | Agency: KAKENHI, NSF, NSFC, ERC, DFG, SNSF, ARC, NWO, GENERIC |
| `grant subtype` | auto | Subtype such as Start-up, Wakate, CAREER, Youth |
| `output format` | markdown | `markdown` or `latex` |
| `language` | auto | Output language override |
| `duration` | inferred | Project length and timeline granularity |
| `auto proceed` | false | Skip checkpoints only when explicitly requested |
