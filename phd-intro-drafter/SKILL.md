---
name: phd-intro-drafter
description: >-
  Drafts a 6-paragraph Introduction outline for a technical paper from a
  structured Flowchart: background and running example, existing
  limitations, problem essence and goal, key challenges, solution
  overview, contributions. Positions the paper as Technique or New
  Problem/Setting and aligns contributions with challenges. Use when
  the user asks to 'draft the Introduction', 'outline the
  Introduction', 'intro logic needs clarifying', 'help structure the
  paper story', or before writing any Introduction prose.
---

# Introduction Drafter

## Overview

The Introduction is the compressed version of the entire paper. In one and a half to two pages it must state the research object, why the problem matters, why existing work falls short, what the paper contributes, and how the contribution maps to section numbers. Reviewers decide whether to keep reading by the time they finish the Introduction, so the logical throughline has to be airtight.

This skill takes a small set of inputs (research area, limitations, hard constraints, key idea, challenges, solution overview) and produces a six-paragraph outline with an explicit purpose and writing points for every paragraph, plus a positioning as Technique Paper or New Problem/Setting Paper. It enforces the rule that contributions align one-to-one with challenges, and that every claim has a section to deliver it.

## When to use this skill

- Before writing any Introduction prose.
- The user has finished planning but the Intro story feels fragmented.
- The user has a partial Intro and wants to restructure.
- The user asks to 'draft the Introduction', 'outline the Introduction', 'intro logic needs clarifying', or 'help structure the paper story'.
- The paper's contributions are clear, but the storyline connecting them is not.
- `phd-idea-evaluator` has returned Strong Accept and the next step is drafting.

## When NOT to use this skill

- The paper's core idea is not yet stable. Use `phd-idea-evaluator` first.
- The paper is a benchmark paper. Use `phd-benchmark-paper-template` instead; the flowchart differs.
- The user wants to polish Introduction prose that is already structured. Use `phd-pre-submission-reviewer` instead.
- The user wants to evaluate whether the Introduction is ready for submission. Use `phd-pre-submission-reviewer`.

## Core procedure

### Step 1: Paper-type positioning

See: references/paper-types.md for the Technique versus New Problem/Setting distinction, positioning criteria, and worked examples from Alpha-SQL, AFlow, and LEAD.

Decide which type the paper is:

- **Technique Paper**: main contribution is a new method or mechanism solving an existing problem. Narrative axis is Key Idea / Mechanism. Goal gets one sentence in passing.
- **New Problem/Setting Paper**: main contribution is a new problem formulation. Narrative axis is Goal / Problem Formulation. Key Idea supports "why this definition is reasonable".

The positioning decides how much weight Paragraph 3 carries: in Technique papers it is a short bridge; in New Problem papers it is a load-bearing paragraph.

### Step 2: Paragraph-by-paragraph outline

See: references/flowchart.md for each paragraph's canonical purpose, writing points, and common failures.

For each of the six paragraphs, return a mini-section containing:

- **Purpose**: one sentence.
- **Writing points**: three to five bullets derived from the user's inputs, each actionable.
- **Gaps**: what the user's inputs do not yet cover for this paragraph. Tag each with severity (CRITICAL, MAJOR, MINOR).

Paragraphs:

1. Background and Motivation. Running example. Why the problem matters in the real world.
2. Limitations of existing work. At most three, each framed as "prior work X does not handle Y".
3. Problem essence and Our Goal. Hard constraints explicit. In Technique papers this is a bridge; in New Problem/Setting papers this is the contribution itself.
4. Key challenges. At most three, each explaining why naive extension of prior work fails.
5. Solution overview. Each module addresses a challenge. Expect a one-to-one mapping between Paragraph 4 challenges and Paragraph 5 modules.
6. Contributions. Three or four numbered bullets. Each maps to a section reference.

### Step 3: Running example design

See: references/running-example.md for the design principles (real, specific, simple-yet-complete, recurring throughout), two design patterns (concrete-failure versus good-versus-bad), and worked examples.

If the user's inputs do not yet include a running example, propose two or three candidate examples and ask the user to pick. Record the chosen example in Paragraph 1 and make sure Paragraph 5 references it ("the Methodology section applies DynaGraph's hotspot detector to the running example from Section 1").

### Step 4: Contribution alignment check

See: references/contribution-patterns.md for strong-versus-weak contribution patterns, anti-patterns, and the canonical mapping to section numbers.

For each contribution bullet, verify:

- Maps to a challenge in Paragraph 4, a module in Paragraph 5, or a specific experiment result.
- Specific, not vague ("comprehensive evaluation" is not a contribution).
- Cites the section number that delivers it.

### Step 5: Flowchart consistency check

Verify the six paragraphs form a single logical throughline:

- Paragraph 1's running example is referenced in Paragraph 5 or a case study forecast.
- Paragraph 2's limitations motivate Paragraph 4's challenges.
- Paragraph 3's goal aligns with Paragraph 6's contribution 1.
- Paragraph 4's challenges map one-to-one with Paragraph 5's modules.
- Paragraph 5's modules appear in Paragraph 6's contribution 2 or 3.

Any break in the chain is a CRITICAL gap.

### Step 6: Integrity gate

Before emitting the outline, run the checks in the Integrity gate section below.

### Step 7: Output the outline

Emit the outline in the Output format below. For `interactive` mode, do not emit; converse one paragraph at a time.

## Integrity gate

All seven bullets are **[inspection]** class: the LLM verifies each directly from its own output (counting, pattern-matching, or comparing sections). No user-side attestation required.

Before returning the outline:

1. **[inspection]** Running example named in Paragraph 1 reappears in Paragraph 5 or 6 (or the Case Study forecast).
2. **[inspection]** Limitations (Paragraph 2) are at most three and each is specific to a named prior work or a named capability.
3. **[inspection]** Challenges (Paragraph 4) are at most three and each explains why a naive extension of prior work fails.
4. **[inspection]** Challenge-to-module mapping is one-to-one, not one-to-many or many-to-one.
5. **[inspection]** Contributions (Paragraph 6) are three or four and each maps to a section number.
6. **[inspection]** No contribution is vague language ("extensive experiments", "thorough analysis" on their own).
7. **[inspection]** Paper-type positioning from Step 1 is reflected in Paragraph 3's weight.

If any check fails, mark the paragraph as "needs user attention" and do not claim the outline is complete.

## Output format

### 0. Type positioning

### 1. Paragraph 1: Background and Motivation

### 2. Paragraph 2: Limitations (at most 3)

### 3. Paragraph 3: Problem Essence and Our Goal

### 4. Paragraph 4: Key Challenges (at most 3)

### 5. Paragraph 5: Solution Overview

### 6. Paragraph 6: Contributions

### 7. Flowchart consistency

### 8. Integrity gate result

### 9. Severity summary
