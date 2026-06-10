---
name: doc-coauthoring
description: Structured co-authoring workflow for specifications, proposals, decision docs, PRDs, RFCs, and other substantial written artifacts. Use when Codex should help a user gather context, shape document structure, draft section by section, and test whether the document works for a cold reader before handoff.
---

# Doc Co-Authoring

## Overview

Use this skill when the user is writing a substantial document and the bottleneck is not grammar, but structure, missing context, or unclear reader expectations. The workflow is:

1. Gather context until the problem, audience, and constraints are concrete.
2. Create a scaffold in a local file or the user-requested output format.
3. Draft the document section by section.
4. Run a cold-reader test and fix gaps before declaring the document done.

This skill is format-agnostic. Use plain Markdown by default. If the requested deliverable is specifically a Word document, slide deck, or spreadsheet-backed document, hand off the file-format work to `docx`, `pptx`, or `xlsx` after the structure is stable.

## Stage 1: Context Gathering

### Goal

Build enough shared context that later drafting steps can focus on tradeoffs and clarity instead of rediscovering basics.

### Start with meta-context

Ask for:

1. Document type.
2. Primary audience.
3. Decision or action the document should drive.
4. Required template or section order.
5. Hard constraints such as deadline, page budget, compatibility requirements, or political constraints.

Accept shorthand answers. If the user already pasted a draft, infer what you can before asking follow-up questions.

### Pull in source material

If the user mentions existing notes, tickets, threads, design docs, or files:

- Read the local files directly when they are available in the workspace.
- Use MCP or other connected tools only when they are actually available in the current environment.
- If a referenced source is not accessible, ask the user to paste the relevant parts instead of pretending the source can be read.

### Ask clarifying questions

After the initial dump, ask focused numbered questions about the gaps that would block drafting. Aim for 5 to 10 high-value questions, not a questionnaire for its own sake.

Good examples:

- What is the concrete failure mode that triggered this document?
- Which alternatives were considered and rejected?
- What does the audience already know, and what must be explained from scratch?
- What decision should a reader be able to make immediately after reading?

### Exit condition

Move on when you can explain, in one short paragraph, what the document is for, who it is for, and what the main recommendation or deliverable is.

## Stage 2: Structure and Scaffolding

### Decide the section set

If the user already has a template, follow it. Otherwise propose a minimal structure that matches the document type.

Examples:

- Decision doc: context, problem, options, recommendation, risks, rollout.
- Technical spec: goal, requirements, design, edge cases, rollout, open questions.
- Proposal: motivation, objectives, plan, budget or resources, risks, ask.

### Create the scaffold

Create a local file with section headings and placeholder text. Prefer Markdown unless the user explicitly asked for another format.

Placeholder text should be short and functional, for example:

```md
## Recommendation

[To be drafted]
```

Do not overdesign the scaffold. Its job is to make iteration easy.

## Stage 3: Section-by-Section Drafting

For each section, run the same loop.

### Step 1: Clarify the section

Ask 3 to 7 questions specific to that section. Keep them concrete and answerable.

### Step 2: Brainstorm candidate points

List 5 to 15 candidate points depending on section complexity. Include:

- facts already provided by the user,
- implications they may have missed,
- tradeoffs or objections the reader is likely to raise.

### Step 3: Curate

Ask the user what to keep, drop, combine, or reorder. If the user gives freeform feedback, translate it into concrete edits.

### Step 4: Draft

Replace the placeholder with real prose. Draft for the target audience, not for the agent. Keep claims tied to the actual context gathered in Stage 1.

### Step 5: Refine

Iterate surgically. Prefer editing the existing file over reprinting the whole document in chat. Track the user's preferences in tone, level of detail, and section length, then apply them to later sections.

### Quality checks during drafting

After a section stabilizes, ask:

- Can anything be deleted without losing meaning?
- Is any paragraph doing more than one job?
- Does this section assume context that the target reader will not have?

## Stage 4: Whole-Document Pass

When most sections are drafted, reread the full document and check:

- flow across sections,
- duplicated content,
- contradictions,
- generic filler,
- missing transitions,
- missing definitions for reader-critical terms.

Surface issues as findings, then edit the file directly.

## Stage 5: Cold-Reader Test

### Goal

Check whether a fresh reader can answer the obvious questions without relying on hidden context from the drafting conversation.

### Produce reader questions

Generate 5 to 10 realistic reader questions such as:

- What problem is this document solving?
- What decision is being requested?
- What changed from the status quo?
- What are the main risks?
- What follow-up action is required from me?

### Testing options

If a fresh subagent, fresh thread, or equivalent independent reader is available, use it with only the document and the reader questions. Do not leak your diagnosis or intended fixes into that test.

If no such isolation mechanism is available, ask the user to test the document manually in a fresh chat or with a real colleague and report back what was unclear.

### Fix loop

If the reader test reveals confusion, go back to the exact section that caused it and fix the missing context, ambiguity, or hidden assumption. Repeat until the main reader questions can be answered correctly from the document alone.

## Final Review

Before declaring the document complete:

1. Confirm the document achieves the intended reader outcome.
2. Ask the user to verify facts, links, metrics, and names.
3. Check that every section still earns its place.

## Working Rules

- Be direct and procedural.
- Prefer local files over large chat-only drafts.
- Do not fabricate access to external systems or documents.
- Do not optimize for elegance before the structure is correct.
- If the user wants to abandon the workflow and draft freeform, switch cleanly without argument.
