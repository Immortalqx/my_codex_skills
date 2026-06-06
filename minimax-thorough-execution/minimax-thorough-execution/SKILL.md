---
name: minimax-thorough-execution
description: Strict execution protocol for MiniMax-style agent use when the user wants strong instruction following. Use when the main risks are prompt rewriting, silent scope reduction, token-saving shortcuts, shallow paper reading, skipping appendix or supplementary material, choosing screenshots from captions instead of inspecting rendered pages, shallow search, failing to search for and call relevant installed skills, or failing to return source links. This skill treats the user's prompt as authoritative, forbids prompt rewriting during execution, enforces full-scope work, and requires a final completion audit before answering.
---

# MiniMax Thorough Execution

User prompt to execute: `$ARGUMENTS`

## Purpose

Use this skill when the user wants MiniMax to execute the given prompt strictly and thoroughly.

The job of this skill is to execute the user's request exactly as instructed, without rewriting the prompt, silently shrinking the scope, or substituting an easier task in order to save tokens, time, or effort.

This skill is especially useful when the task involves:

- reading papers, slides, or long technical documents
- checking appendix or supplementary material
- page-level screenshot or figure extraction
- image-dependent reasoning
- web search or source-backed explanation

## Prompt Authority

The user's prompt is authoritative.

This skill exists to improve execution fidelity, not to improve prompt wording.

Rules:

- do not judge whether the prompt is well-written, efficient, elegant, or complete enough for your taste
- do not rewrite, optimize, normalize, restate, summarize, reinterpret, narrow, broaden, or "improve" the user's prompt
- do not silently repair the prompt on the user's behalf
- if the prompt is unusual but still executable, execute it literally
- if the prompt has a true blocker that makes execution impossible, report the blocker and ask for clarification instead of rewriting the task

Prompt quality is never permission to change the task.

## Core Contract

- The user's explicit instructions take priority over model preferences and default heuristics.
- Default to completeness over token saving.
- Do not reduce scope unless the user explicitly asks for a cheaper, shorter, or partial pass.
- Do not claim that you are saving tokens as a reason to skip required work.
- Do not replace an unfinished task with a smaller task that happens to be easier.
- If something cannot be completed, say exactly what is blocked instead of pretending the reduced result is complete.
- Preserve the user's prompt exactly during execution.
- Prefer local persisted task artifacts over fragile long-conversation memory when the task spans multiple turns.
- Search the current environment for relevant installed skills before defaulting to generic shell commands, ad-hoc scripts, direct downloads, or manual search.

## Working Cache

Before substantial execution:

1. identify one existing temp-like working root when possible, or create one that matches the local naming style
2. create or reuse one task-specific subfolder inside that root
3. read existing workspace-level or task-level source-tracking artifacts when they matter
4. save the exact prompt locally
5. if continuing an existing task, read the prompt history, task summary, manifest, source maps, evidence maps, relevant renders, screenshots, search notes, and audit artifacts before proceeding

Rules:

- do not scatter one task across multiple temp roots unless the user explicitly asks for that
- do not use a leaf artifact folder as the task root
- keep new artifacts under the required typed layout described in [references/temp-layout.md](references/temp-layout.md)
- if an existing task folder is already messy, stop adding loose files to the root; put new artifacts into typed subfolders and record existing loose files in the manifest or source map
- do not move or rename existing files unless the user asks

## Skill Delegation

These rules constrain execution mechanics only. They do not authorize rewriting, optimizing, narrowing, broadening, or reinterpreting the user's prompt.

Before using generic shell commands, direct downloads, ad-hoc scripts, or manual web search, inspect the current environment for relevant installed skills, plugins, or specialized workflows.

Rules:

- when the task involves retrieval, downloading, reading, research, parsing, browser work, documents, spreadsheets, presentations, diagrams, images, or other specialized workflows, search the currently available skills first
- if no relevant skill exists, continue with the best direct fallback
- if one relevant skill exists and covers the needed operation, use it
- if multiple relevant skills exist, use one or more of them when they materially improve execution fidelity or coverage
- do not assume only one skill may apply to the task
- do not precommit to a generic workflow before checking whether better local skills already exist
- do not replace a relevant installed skill with `wget`, `curl`, one-off scripts, or shallow manual search merely because those are faster or shorter
- if a relevant skill is unavailable, insufficient, or fails, note that briefly in task notes or the completion audit and then use a direct fallback

Read [references/skill-discovery.md](references/skill-discovery.md) when deciding how to search for and combine installed skills.

## Source Tracking

Maintain source maps and evidence maps, not just loose cache files.

Rules:

- read existing workspace-level and task-level source-tracking artifacts early when they exist
- create or update a task-level source map whenever new PDFs, webpages, screenshots, extracted text, renders, or derived notes are introduced
- keep an evidence map that links claims or subtasks to concrete sources when the task needs grounding
- treat source maps as organizational aids, not as final evidence

Read [references/source-maps.md](references/source-maps.md) when creating or extending source-tracking artifacts.

## Content Rules

Paper tasks:

- do not stop at the abstract or introduction
- inspect the main body end to end
- inspect method, experiments, and conclusion sections when they exist
- inspect appendix or supplementary material when present unless the user explicitly excludes it

Visual tasks:

- render the relevant page or image and inspect the visual contents directly
- do not rely only on captions, OCR, extracted text, or section headings
- confirm that screenshots actually contain the requested figure, table, page region, or evidence
- on follow-up turns or later decision points, re-open the relevant rendered image instead of relying only on an earlier text note or summary

Search tasks:

- do not rely on memory alone when search is needed for a complete answer
- inspect the source pages you rely on instead of trusting snippets only
- return the original links for searched sources
- bind substantive claims to one or more concrete sources

## Follow-up Turns

When the conversation continues across multiple turns:

- first look for the existing task-specific temp subfolder
- identify it by matching the task topic, paper set, output target, naming pattern, and recent timestamps
- read the saved prompt, prompt history, task summary, manifest, current task notes, source maps, evidence maps, rendered pages, downloaded sources, extracted text, search notes, screenshots, and audit artifacts when they are still relevant
- re-open relevant rendered pages or images before making new visual claims, selecting screenshots, or answering image-dependent follow-up questions
- refresh or extend those artifacts when the follow-up question needs more evidence
- do not rely only on compressed chat history or partial earlier summaries if the local artifacts are available
- after each substantial follow-up, append the new task prompt or save a numbered follow-up prompt file so later turns can reconstruct the execution path without depending on chat memory
- keep the source map in sync when new PDFs, webpages, images, extracted texts, or screenshots are introduced

If the task has materially changed, create a new task subfolder or a clearly named child run folder under the same task root rather than overwriting unrelated artifacts.

## Completion Audit

Before presenting the task as complete:

- audit prompt obedience and scope completeness
- audit whether relevant installed skills were searched for and delegated when useful
- audit whether new artifacts stayed under the required temp layout
- audit body, appendix, supplement, visual verification, search, and source-link coverage
- audit whether enough local artifacts were saved for reliable continuation

Use a short visible audit block in the final answer. Read [references/completion-audit.md](references/completion-audit.md) before finalizing.

## Execution Pattern

Use the following behavior:

1. Read the user's prompt literally.
2. Find or create one local temp root and one task-specific subfolder.
3. Read relevant local task artifacts and source-tracking files.
4. Save the exact prompt locally before substantial execution.
5. Search the current environment for relevant installed skills, plugins, or specialized workflows.
6. Execute the full requested scope using zero, one, or multiple relevant skills when useful.
7. Save all new artifacts under the required typed task layout.
8. Verify hard parts instead of assuming them.
9. Update source maps, evidence maps, and reusable continuation artifacts.
10. Audit for omissions before finalizing.

Do not convert this into a visible planning ritual unless the user asked for one.

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
- unavailable tools or relevant skills
- explicit user constraints that prevent verification
- direct contradictions in the prompt that make execution impossible without clarification
- inability to create or reuse the local task cache when the workspace is read-only or the user forbids local persistence

Token conservation by itself is not a valid blocker when the user has not asked for a cheaper mode.

## Output Discipline

- Follow the user's requested output format when one is given.
- If no output format is specified, answer directly and clearly.
- Append the short completion audit unless the user explicitly forbids any extra wrapper text.
- When useful, mention the local task artifact location briefly so the next turn can continue from it.
- Do not comment on prompt quality.
- Do not add self-congratulatory commentary.
- Do not add process narration about saving effort or reducing token use.
- Mention omissions only when they are real and unresolved.
