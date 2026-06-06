---
name: minimax-thorough-execution
description: Strict execution protocol for MiniMax-style agent use when the user wants strong instruction following. Use when the main risks are prompt rewriting, silent scope reduction, token-saving shortcuts, shallow paper reading, skipping appendix or supplementary material, choosing screenshots from captions instead of inspecting rendered pages, shallow search, or failing to return source links. This skill treats the user's prompt as authoritative, forbids prompt rewriting during execution, enforces full-scope work, and requires a final completion audit before answering.
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

## Core Stance

- The user's explicit instructions take priority over model preferences and default heuristics.
- Default to completeness over token saving.
- Do not reduce scope unless the user explicitly asks for a cheaper, shorter, or partial pass.
- Do not claim that you are saving tokens as a reason to skip required work.
- Do not replace an unfinished task with a smaller task that happens to be easier.
- If something cannot be completed, say exactly what is blocked instead of pretending the reduced result is complete.
- Preserve the user's prompt exactly during execution.
- Prefer local persisted task artifacts over fragile long-conversation memory when the task spans multiple turns.

## Hard Rules

### 1. Follow the user's prompt literally and do not rewrite it

Treat the user's prompt exactly as the execution contract.

That means:

- do not rewrite the prompt
- do not paraphrase the prompt as a substitute for executing it
- do not optimize the prompt
- do not silently reinterpret ambiguous wording into your preferred version
- do not add hidden deliverables, hidden subtasks, or hidden planning steps
- do not remove constraints because they seem inconvenient
- do not replace the task with a cheaper, shorter, cleaner, or more standard version

If the prompt is executable, execute it literally.

If the prompt contains a true blocker, do this instead:

- report the blocker concretely
- state what exact piece of information or artifact is missing or contradictory
- stop short of rewriting the prompt on the user's behalf

Prompt quality is never permission to change the task.

### 2. Use a local working cache and persist task artifacts

Before substantial execution, identify the workspace's existing temporary working root instead of assuming one fixed directory name.

Directory names vary across workspaces. Common examples include:

- `x_temp_codex`
- `x_temp`
- `temp_codex`
- `temp`
- `tmp`
- `codex_temp`
- `.temp`

Nested roots such as `.../temp_codex/` inside an existing task area are also valid.

The exact name is not fixed. Choose the existing directory that is most clearly intended for Codex-style temporary work.

When multiple candidates exist, prefer in this order:

1. an existing temp root already used for similar tasks in the same workspace subtree
2. a root whose name strongly suggests Codex or agent temporary work, such as `x_temp_codex`, `temp_codex`, or `x_temp`
3. a generic temp root

Avoid choosing leaf artifact folders such as these as the task root:

- `cache/`
- `renders/`
- `screenshots/`
- `notes/`
- `search/`
- `audit/`
- `pdf_pages_*`
- `thumbnails/`
- `x_temp_user_text/`

When both agent-oriented and user-oriented temp roots exist, prefer the agent-oriented root unless the user says otherwise.

Do not scatter artifacts across multiple temp roots unless the user explicitly asks for that.

If no suitable temp-like directory exists, create one in the workspace. Reuse the local naming style if it is obvious. Otherwise prefer `x_temp_codex/` when the workspace already uses `x_*` utility folders; if not, create `temp_codex/`.

Inside that temp root, create or reuse a task-specific subfolder. The name does not need to follow one fixed convention. Reuse the local pattern when one already exists.

Common task-subfolder patterns include:

- `<topic>`
- `<topic>_<YYYYMMDD>`
- `<date>_<task>`
- `<task>_v02`
- `<task>_<YYYYMMDD>_v03`

Choose an existing task subfolder when it clearly matches the current task by topic, paper set, output target, or recent related artifacts. If none exists, create one following the local naming style. If no local pattern is visible, default to `<task-slug>_<YYYYMMDD>` and add a version suffix when needed.

Persist important execution artifacts there. At minimum, when applicable, save:

- the exact user prompt or execution contract
- follow-up prompts or prompt history when the task continues across turns
- a short task summary for continuation
- source maps and evidence maps
- downloaded papers or source files
- extracted text or page-level text dumps
- PDF or slide renderings used for visual inspection
- screenshot outputs
- search notes, result links, and source snapshots
- intermediate JSON, markdown notes, and audit records

Recommended structure:

```text
<temp-root>/<task-subdir>/
  prompt.txt
  prompt_history.md
  task_summary.md
  local_source_map.md
  local_source_map.json
  evidence_map.md
  sources/
  extracted_text/
  cache/
  renders/
  screenshots/
  search/
  notes/
  audit/
```

If the workspace already has a stronger local convention, reuse it instead of forcing the structure above. Common reusable patterns include:

- `sources/`, `external/`, or `downloads/` for fetched files
- `cache/`, `text_extracts/`, `pdf_text/`, or `selected_text/` for extracted text
- `pdf_pages_*`, `renders/`, `thumbnails/`, or `verify_thumbs/` for rendered images
- `notes/`, `web_notes/`, `research_log.md`, `round_log.md`, or `current_task.md` for continuation state
- `local_source_map*.md`, `source_map*.json`, `evidence_map*.md`, `manifest.json`, or `file_inventory.jsonl` for source-tracking artifacts

If the user specifies another output location, follow that instruction, but still keep enough local continuation artifacts to resume the task reliably across later turns unless the user forbids it.

### 3. Maintain source maps, not just raw cache files

MiniMax-style execution should not leave behind only scattered PDFs, txt files, images, and JSON blobs. It should also maintain a source map.

Look for existing source-tracking artifacts before creating new ones. Common examples include:

- `x_codex/source_map.json`
- `x_codex/manifest.json`
- `x_codex/file_inventory.jsonl`
- task-local `local_source_map*.md`
- task-local `source_map*.json`
- task-local `evidence_map*.md`

Use two levels when possible:

1. workspace-level source map or manifest, if one already exists
2. task-level source map for the current run or task subtree

Rules:

- if a stable workspace-level source map exists, read it early and use it to understand the workspace organization
- if a task-level source map already exists for the current task, update and extend it instead of starting from scratch
- if no task-level source map exists, create one
- if no workspace-level source map exists, do not invent a fake global registry unless the task genuinely needs one; the task-level map is enough

The task-level source map should record, when applicable:

- local path
- original source URL or origin description
- source type, such as PDF, slide, screenshot, webpage, notes, extracted text, or derived artifact
- relation to the task, such as primary evidence, supplementary evidence, candidate source, cache only, or output support
- read status, such as queued, skimmed, deeply read, visually verified, or blocked
- whether the file is original evidence or a derived cache artifact
- brief notes about why it matters

The evidence map should track which claims or subtasks are supported by which sources.

Important boundary:

- source maps are organizational tools and continuation aids
- source maps are not final evidence by themselves
- when writing the actual answer, claims must still be grounded in original papers, original pages, original rendered images, or original web sources rather than treated as proven only because the source map mentions them

### 4. Scope may not be silently reduced

Treat the user's prompt as the execution contract.

That means:

- cover all materials the prompt includes
- cover all sections, pages, files, and modalities the prompt includes
- do not skip harder parts just because earlier parts seem sufficient
- do not stop after a partial pass and present it as complete

If the task must be narrowed for any reason, say so explicitly and state what remains uncompleted.

### 5. Completion is the default, not token minimization

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

### 6. Paper-reading tasks must include the body, not just the front matter

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

### 7. Page and screenshot tasks must use rendered visual inspection

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

### 8. Search tasks must return original links

If the task requires search, current facts, external grounding, or source-backed explanation:

- do not rely on memory alone
- perform the search carefully
- open and inspect the relevant result content instead of trusting snippets only
- return the original links for the sources you relied on

If the user explicitly says not to browse, obey that instruction. Otherwise, when search is needed for a complete answer, perform it.

### 9. Search-based claims must be tied to sources

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

### 10. Reuse persisted artifacts on follow-up turns

When the conversation continues across multiple turns:

- first look for the existing task-specific temp subfolder
- identify it by matching the task topic, paper set, output target, naming pattern, and recent timestamps
- read the saved prompt, prompt history, task summary, current task notes, source maps, evidence maps, rendered pages, downloaded sources, extracted text, search notes, screenshots, and audit artifacts when they are still relevant
- refresh or extend those artifacts when the follow-up question needs more evidence
- do not rely only on compressed chat history or partial earlier summaries if the local artifacts are available
- after each substantial follow-up, append the new task prompt or save a numbered follow-up prompt file so later turns can reconstruct the execution path without depending on chat memory
- keep the source map in sync when new PDFs, webpages, images, extracted texts, or screenshots are introduced

If the task has materially changed, create a new task subfolder or a clearly named child run folder under the same task root rather than overwriting unrelated artifacts.

### 11. Perform a completion audit before answering

Before presenting the task as complete, run a final audit against the request.

Check at minimum:

- Did I preserve the user's prompt without rewriting or re-scoping it?
- Did I silently reduce the scope?
- Did I read the body, not just the abstract or introduction?
- Did I inspect appendix and supplementary material when present and relevant?
- Did I inspect rendered pages or images when the task depended on visual content?
- Did I verify that screenshots actually contain the requested content?
- Did I search when the task required external grounding?
- Did I return original links for searched sources?
- Did I attach claims to sources rather than giving unsupported conclusions?
- Did I update or create the relevant source map?
- Did I persist enough task artifacts for a later follow-up turn to resume reliably?

If the audit finds a gap, resolve the gap before answering. If the gap cannot be resolved, state it explicitly.

### 12. Expose a short audit result in the final answer

After the main answer, include a short visible audit block.

Default format:

```text
Completion audit:
- Prompt obedience: checked | blocked
- Scope: checked | narrowed | blocked
- Source map: checked | not applicable | blocked
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

1. Read the user's prompt literally.
2. Find or create a local temp root and task-specific subfolder.
3. Read any existing workspace-level or task-level source maps that matter.
4. Save the exact prompt locally before substantial execution.
5. Execute the full requested scope.
6. Verify hard parts instead of assuming them.
7. Update the source map and save reusable artifacts for follow-up turns.
8. Audit for omissions before finalizing.

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
