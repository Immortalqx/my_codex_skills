---
name: "proof-writer"
description: "Writes rigorous mathematical proofs for ML/AI theory. Use when asked to prove a theorem, lemma, proposition, or corollary, fill in missing proof steps, formalize a proof sketch, \u8865\u5168\u8bc1\u660e, \u5199\u8bc1\u660e, \u8bc1\u660e\u67d0\u4e2a\u547d\u9898, or determine whether a claimed proof can actually be completed under the stated assumptions."
---

# Proof Write: Rigorous Theorem / Lemma Drafting

Write a mathematically honest proof package, not a polished fake proof.

## Constants

- DEFAULT_PROOF_DOC = `PROOF_PACKAGE.md` in project root
- STATUS = `PROVABLE AS STATED | PROVABLE AFTER WEAKENING / EXTRA ASSUMPTION | NOT CURRENTLY JUSTIFIED`

## Context: $ARGUMENTS

## Goal

Produce exactly one of: 1. a complete proof of the original claim 2. a corrected claim plus a proof of the corrected claim 3. a blockage report explaining why the claim is not currently justified

## Inputs

Extract and normalize: - exact theorem / lemma / proposition / corollary statement - explicit assumptions - notation and definitions - any user-provided proof sketch, partial proof, or intended strategy - nearby lemmas or claims in local notes, appendix files, or theorem drafts if the request points to them - desired output style if specified: concise, appendix-ready, or full-detail

If notation or assumptions are ambiguous, state the exact interpretation you are using before proving anything.

## Workflow

### Step 1: Gather Proof Context

Read the relevant local context: - the chosen target proof file, if it already exists - theorem notes, appendix drafts, or files explicitly mentioned by the user

Extract: - exact claim - assumptions - notation - proof sketch or partial proof - nearby lemmas that the draft may depend on

### Step 2: Normalize the Claim

Identify: - hidden assumptions - undefined notation - scope ambiguities - whether the available sketch proves the full claim or only a weaker variant

Preserve the user's original theorem statement unless a change is explicitly required. If you use a stronger normalization or cleaner internal formulation only to make the proof easier, keep that as an internal proof device rather than silently replacing the original claim.

### Step 3: Feasibility Triage

Check explicitly: - does the conclusion actually follow from the listed assumptions? - is any cited theorem being used outside its conditions? - is the claim stronger than what the available argument supports? - is there an obvious counterexample, boundary case, or quantifier failure?

If the claim is not provable as stated, do NOT fabricate a proof. Do NOT silently strengthen assumptions or narrow the theorem's scope just to make the proof work.

### Step 4: Build a Dependency Map

Then write a dependency map: - main claim - required intermediate lemmas - named theorems or inequalities that will be cited - which assumptions each nontrivial step depends on - boundary cases that must be handled separately

If one step is substantial, isolate it as a lemma instead of burying it in one sentence.

### Step 5: Write the Proof Document

If the target proof file already exists: - read it first - update the relevant claim section - do not blindly duplicate prior content

If the user does not specify a target, default to `PROOF_PACKAGE.md` in project root.

Do NOT write directly into paper sections or appendix `.tex` files unless the user explicitly asks for that target.

The proof package must include: - exact claim - explicit assumptions - proof status - announced strategy - dependency map - numbered major steps - justification for every nontrivial implication

Mathematical rigor requirements: - never use "clearly", "obviously", "it can be shown", "by standard arguments", or "similarly" to hide a gap - define every constant and symbol before use - check quantifier order carefully - handle degenerate and boundary cases explicitly, or state why they are excluded - if invoking a standard fact, state its name and why its assumptions are satisfied here - use `$...$` for inline math and `$$...$$` for display equations - never write math in plain text - if the proof uses an equivalent normalization that is stronger in appearance than the user's original theorem statement, label it explicitly as a proof device and keep the original claim separate

### Step 6: Final Verification

If a key step still cannot be justified, downgrade the status and write a blockage report instead of forcing a proof.

## Required File Structure

Write the target proof file using this structure:

```md
# Proof Package

## Claim
[exact statement]

## Status
PROVABLE AS STATED / PROVABLE AFTER WEAKENING / NOT CURRENTLY JUSTIFIED

## Assumptions
- ...

## Notation
- ...

## Proof Strategy
[chosen approach and why]

## Dependency Map
1. Main claim depends on ...
2. Lemma A depends on ...
3. Step k uses ...

## Proof
Step 1. ...
Step 2. ...
...
Therefore the claim follows. 鈭?

## Corrections or Missing Assumptions
- [only if needed]

## Open Risks
- [remaining fragile points, if any]
```

## Output Modes

### If the claim is provable as stated

### If the original claim is too strong

### If the proof cannot be completed honestly

## Chat Response

After writing the target proof file, respond briefly with: - status - whether the original claim survived unchanged - what file was updated

## Key Rules

- Never fabricate a missing proof step.
- Prefer weakening the claim over overclaiming.
- Separate assumptions, derived facts, heuristics, and conjectures.
- Preserve the user's original theorem statement unless you explicitly mark a corrected claim or an internal normalization.
- If the statement is false as written, say so explicitly and give a counterexample or repaired statement.
- If uncertainty remains, mark it explicitly in `Open Risks`; do not hide it inside polished prose.
- Correctness matters more than brevity.