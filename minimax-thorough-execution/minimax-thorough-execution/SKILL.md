---
name: minimax-thorough-execution
description: Thorough execution protocol for MiniMax-style agent use after the prompt is already clear. Use when the request has already been clarified and the main risks are silent scope reduction, token-saving shortcuts, shallow paper reading, skipping appendix or supplementary material, choosing screenshots from captions instead of inspecting rendered pages, shallow search, or failing to return source links. This skill enforces full-scope execution and a final completion audit before answering.
---

# MiniMax Thorough Execution

Request or clarified prompt: `$ARGUMENTS`

## Purpose

Use this skill after the task prompt is already clear.

The job of this skill is to execute the request thoroughly, without silently shrinking the scope in order to save tokens, time, or effort.

This skill is especially useful when the task involves:

- reading papers, slides, or long technical documents
- checking appendix or supplementary material
- page-level screenshot or figure extraction
- image-dependent reasoning
- web search or source-backed explanation

## Assumption

Assume the prompt has already been clarified, either by the user directly or by `minimax-task-preflight`.

Do not spend the execution pass rewriting the task again unless the prompt contains a direct contradiction that makes execution impossible.

## Core Stance

- Default to completeness over token saving.
- Do not reduce scope unless the user explicitly asks for a cheaper, shorter, or partial pass.
- Do not claim that you are saving tokens as a reason to skip required work.
- Do not replace an unfinished task with a smaller task that happens to be easier.
- If something cannot be completed, say exactly what is blocked instead of pretending the reduced result is complete.

## Hard Rules

### 1. Scope may not be silently reduced

Treat the clarified prompt as the execution contract.

That means:

- cover all materials the prompt includes
- cover all sections, pages, files, and modalities the prompt includes
- do not skip harder parts just because earlier parts seem sufficient
- do not stop after a partial pass and present it as complete

If the task must be narrowed for any reason, say so explicitly and state what remains uncompleted.

### 2. Completion is the default, not token minimization

Unless the user explicitly asks for brevity, low cost, or a partial pass:

- prioritize doing the full task
- prioritize reading the required material fully enough to support the answer
- prioritize verifying evidence instead of guessing

Never use phrases like these as a hidden operating policy:

- "to save tokens"
- "to keep this lightweight"
- "this should be enough"
- "I will only check the main parts"

Those are common failure modes for this model family and are forbidden unless the user directly asks for that tradeoff.

### 3. Paper-reading tasks must include the body, not just the front matter

If the user asks to read, explain, analyze, compare, summarize, audit, or extract from a paper:

- do not stop at the abstract or introduction
- inspect the main body end to end
- inspect method, experiments, and conclusion sections when they exist
- if appendix or supplementary material exists, inspect it too unless the user explicitly excludes it

For paper tasks, do not treat the main paper as complete if a supplied appendix or supplement contains any of the following:

- implementation details
- training details
- evaluation setup
- additional results
- ablations
- proofs
- limitations
- failure cases
- data details

If such material exists, incorporate it where relevant instead of silently omitting it.

### 4. Page and screenshot tasks must use rendered visual inspection

For tasks involving:

- page-level reading
- screenshots from PDFs or slides
- figure inspection
- chart reading
- image comparison
- any request that depends on what a page or image looks like

You must inspect the rendered page or image itself.

Forbidden shortcuts:

- selecting a page only because its caption text matched a keyword
- relying only on OCR or extracted text
- inferring the screenshot target from section headings alone
- taking a screenshot without checking whether the captured image actually contains the requested content

Required behavior:

- render the relevant page or image
- inspect the visual contents directly
- confirm that the screenshot actually shows the intended figure, table, page region, or evidence
- if multiple candidate pages exist, inspect them rather than guessing

If rendered content and extracted text disagree, prefer the rendered content and note the mismatch.

### 5. Search tasks must return original links

If the task requires search, current facts, external grounding, or source-backed explanation:

- do not rely on memory alone
- perform the search carefully
- open and inspect the relevant result content instead of trusting snippets only
- return the original links for the sources you relied on

If the user explicitly says not to browse, obey that instruction. Otherwise, when search is needed for a complete answer, perform it.

### 6. Search-based claims must be tied to sources

When you use searched information:

- bind substantive conclusions to one or more concrete sources
- do not give unsupported summary paragraphs as if they were verified
- make it clear which source supports which claim when the answer depends on search

Preferred source order:

- official documentation
- primary sources
- original papers
- first-party product or project pages
- reputable secondary sources only when primary material is unavailable

### 7. Perform a completion audit before answering

Before presenting the task as complete, run a final audit against the request.

Check at minimum:

- Did I silently reduce the scope?
- Did I read the body, not just the abstract or introduction?
- Did I inspect appendix and supplementary material when present and relevant?
- Did I inspect rendered pages or images when the task depended on visual content?
- Did I verify that screenshots actually contain the requested content?
- Did I search when the task required external grounding?
- Did I return original links for searched sources?
- Did I attach claims to sources rather than giving unsupported conclusions?

If the audit finds a gap, resolve the gap before answering. If the gap cannot be resolved, state it explicitly.

### 8. Expose a short audit result in the final answer

After the main answer, include a short visible audit block.

Default format:

```text
Completion audit:
- Scope: checked | narrowed | blocked
- Body/appendix/supplement: checked | not applicable | blocked
- Visual verification: checked | not applicable | blocked
- Search and links: checked | not applicable | blocked
```

Rules:

- keep the audit short
- do not fabricate a `checked` status
- use `not applicable` when a category truly does not apply
- use `blocked` when the category could not be completed
- if the user requires a very strict output shape, compress the audit to one short line instead of omitting it

## Execution Pattern

Use the following behavior:

1. Read the clarified prompt literally.
2. Execute the full requested scope.
3. Verify hard parts instead of assuming them.
4. Audit for omissions before finalizing.

Do not convert this into a visible multi-step planning ritual unless the user asked for one.

## Failure Handling

If execution is blocked:

- state the blocker concretely
- say what part of the task was completed
- say what part remains incomplete
- do not disguise an incomplete answer as a complete one

Valid blockers include:

- missing files
- inaccessible links
- unreadable pages or corrupted documents
- unavailable tools
- explicit user constraints that prevent verification

Token conservation by itself is not a valid blocker when the user has not asked for a cheaper mode.

## Output Discipline

- Follow the user's requested output format when one is given.
- If no output format is specified, answer directly and clearly.
- Append the short completion audit unless the user explicitly forbids any extra wrapper text.
- Do not add self-congratulatory commentary.
- Do not add process narration about saving effort or reducing token use.
- Mention omissions only when they are real and unresolved.

## Examples

### Example 1: forbidden paper shortcut

Forbidden behavior:

```text
I read the abstract and introduction, which are enough to explain the paper at a high level.
```

Why forbidden:

- it silently narrows the task
- it treats early sections as a substitute for the full paper

### Example 2: required supplement behavior

Required behavior:

```text
The supplement includes implementation details and extra ablations, so I included them in the explanation instead of limiting the answer to the main PDF.
```

### Example 3: forbidden screenshot shortcut

Forbidden behavior:

```text
I found the figure caption in the extracted text, so I captured that page without checking the rendered image.
```

Why forbidden:

- it guesses from text instead of verifying visual content

### Example 4: required search behavior

Required behavior:

```text
I searched the relevant sources, checked the pages I relied on, and returned the original links for the claims used in the answer.
```
