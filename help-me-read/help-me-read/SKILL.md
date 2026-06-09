---
name: help-me-read
description: Deep-read a single user-provided PDF (lecture slides or academic paper) and produce a story-driven close-read note in the user`s working language. Use when the user asks Codex to "close-read", "detailed study notes", "tutor-style breakdown", "deep study notes", "open-book review", or hands over a PDF plus a target output path. The skill reads every page, captures full-page screenshots of slides and region screenshots of paper figures, runs divergent web searches to fill in background that is not in the PDF, uses available image-understanding tools for non-OCR figure analysis, and writes a new note file with a single unified narrative metaphor, motivation-problem-solution-why sections per topic, key term glosses, and source links. The skill never overwrites an existing note and writes per-note assets in a sibling folder.
---

# Help Me Read

User-provided PDF: `$ARGUMENTS`

The user wants a story-driven close-read of a PDF. Treat the PDF as the primary source. Everything that is not in the PDF must be searched or visually inspected, not invented.

## Working Language

The note itself is written in the **user`s working language**. Detect it from the most recent user message:

- if the user wrote in Chinese, default to Chinese for the note
- if the user wrote in English, default to English
- if the user wrote in another language, default to that language
- if ambiguous, ask one concise question

Technical terms inside the note may stay in English (with a Chinese gloss in parentheses on first appearance) even when the surrounding prose is Chinese, or vice versa. The glossary follows the same rule.

The skill itself (this file, `style-guide.md`, `template.md`) is in English. Only the **final note** follows the user`s working language.

## When This Skill Applies

Use this skill when the user:

- hands you a PDF path and asks for a close-read, detailed study notes, tutor-style breakdown, or deep study notes
- wants per-section motivation-problem-solution-why explanations, not a summary
- expects key terms to be glossed, equations to be motivated, and the output to use a single unified story or metaphor that runs through the whole document
- wants a clean new note file next to existing ones, not an overwrite

Do not use this skill for casual summaries, slide-by-slide transcription, or one-line Q&A about a paper.

## Core Boundary

The output is a single close-read note that lets the user read the original PDF less and understand it more. It is not a translation. It is not a reference manual. It is a tutor-style study note.

The note must:

- follow the PDF structure, but group content by topic rather than by page
- introduce one running metaphor or story that explains every concept in the note
- give every major concept a motivation-problem-solution-why block
- gloss every key term the first time it appears
- embed figures that come from the original PDF as inline images, plus source links for any claim that came from outside the PDF
- be written to a brand new file with a suffix that makes the version obvious, and never overwrite an existing note

## Working Directory Contract

When the user does not specify a path:

1. Look for a recent temp-like working root in the workspace that follows the users existing convention. Names like `x_temp_codex`, `x_temp`, `temp_codex`, `temp`, `tmp`, `codex_temp`, or `.temp` are common patterns the user may already use; reuse whatever style the workspace already follows. If the workspace has a different convention, follow that. If the workspace has no obvious convention at all, pick a temp-like folder name that fits and record the choice in `task_summary.md`.
2. Otherwise create a skill-scoped task folder under that root, named for this skill and the document slug (e.g. `<workspace>/<temp-root>/help-me-read/<doc-slug>/`). The exact names of the temp root and the task folder are runtime choices, not hard-coded in this skill.
3. Inside that task folder, create typed subfolders:
   ```text
   prompt.txt
   task_summary.md
   sources/
     user_files/        # the original PDF, untouched
     fetched/           # web pages and arXiv papers downloaded for grounding
   extracted_text/      # per-page text from the PDF
   renders/             # full-page screenshots of slides, or full pages for paper
     pages/             # one PNG per PDF page
   screenshots/
     selected/          # cropped figures that will be embedded in the note
   search/
     queries/           # search queries that were actually run
     results/           # short notes + original links from each search
   notes/               # per-topic or per-section drafts
   final/               # the final close-read note
   ```
4. The final note goes to `final/<doc-slug>_<lang>_<version>.md`. If the user named a path, use that path; otherwise this is the default.
5. Per-note image assets live in `final/<doc-slug>_<lang>_<version>_assets/` so the note folder is self-contained and the next revision will not break image links.

When the user already pointed at an existing folder (their target output directory):

- Do not create a new top-level temp root.
- Reuse that folder as the working directory.
- Put extracted text, renders, screenshots, search notes, and the final note in sibling subfolders next to the existing notes.
- Keep the same `final/<doc-slug>_<lang>_<version>.md` plus `final/<doc-slug>_<lang>_<version>_assets/` convention for the note itself.

Never write a note into a folder that already contains a note with the same slug, suffix, and language. If a collision is about to happen, change the version suffix before writing.

## Workflow

### 1. Identify the Input and the Reader

Determine:

- the PDF path
- the document type: lecture slides, research paper, technical report, book chapter, or other
- the working language for the note (default to the language of the most recent user message, or ask one concise question if ambiguous)
- the target output path, or the default path from the working-directory contract
- the user`s existing notes folder if there is one

Read `references/style-guide.md` before writing any prose.

### 2. Extract the PDF

Extract text and per-page screenshots:

- Use any Python tool already installed in the environment that can read PDF text and render pages. The skill does not pin a specific library; pick whatever is available and works.
- Write per-page text to `extracted_text/page_<n>.txt`.
- For lecture slides, render every page as a PNG into `renders/pages/lecture_p<NN>.png` at 200 DPI or higher.
- For research papers, render every page as a PNG into `renders/pages/paper_p<NN>.png`. Cropped figures go to `screenshots/selected/figure_<n>.png` when the user will reference them in the note.

Verify: every page of the source PDF has a corresponding text file and a corresponding PNG. If a page is image-only and text extraction failed, run OCR on the rendered PNG, or call an image-understanding tool on the rendered page, and record the result.

### 3. Divergent Web Search

For every concept the user is likely to find confusing, run a divergent search. Do not just search the exact phrase from the slide. Search for the concept`s motivation, naming origin, predecessor algorithms, common pitfalls, and modern alternatives.

Strong search categories:

- the original paper or first-author blog for the named algorithm
- canonical explainers (the agent picks the most relevant one at write time, e.g. a well-known blog series, an open course, or a textbook chapter that matches the topic)
- surveys or textbook chapters that put the concept in context
- a Chinese-language explainer for the same concept when the user`s working language is Chinese, so the note can borrow good phrasings
- the predecessor and successor of the concept, so motivation and "why not the old way" can be filled in

Save to `search/queries/` one short text file per search with the exact query and date, and to `search/results/` a short markdown note per result with the original URL and a 1-3 sentence summary.

Use the best web-search capability available to the current agent. Prefer a real web-search tool over manual `curl` or `wget`, but if none is available, fall back to direct HTTP and record the source.

### 4. Image Understanding for Non-OCR Figures

For figures that are dense diagrams, plot families, or architecture overviews:

- call an image-understanding tool on the rendered PNG and ask for: what is being plotted, what axes mean, what each curve or block represents, and what the reader should take away
- write the explanation into `notes/figure_<n>_explanation.md`
- prefer the image-understanding tool over manual OCR; OCR is a fallback for text inside an image, not for understanding a figure

Use the best image-understanding capability available to the current agent. Prefer a real image-understanding tool over guessing, but if none is available, say so in the note and fall back to the closest OCR you can manage.

### 5. Design the Running Story

Before writing prose, pick **one** running metaphor or story that maps cleanly to every major concept in the document. Write a 3-5 sentence description of the metaphor into `notes/story_design.md` so the choice is intentional and auditable. The metaphor must:

- be concrete and physical, not abstract
- map one-to-one with the document`s main concepts
- support a "before / after" structure that explains motivation
- be easy to reuse in figures, code, and Q&A at the end of the note

Bad: "RL is like teaching a child." Good: "PPO is teaching a 5-year-old to ride a bike with soft training wheels; SAC is a bartender learning to make a Long Island Iced Tea who is rewarded for being adventurous."

### 6. Write the Close-Read Note

The note is the only deliverable. Section structure:

```text
0. How to read this note         # 1-2 paragraphs
1. <running story, in 1 page>    # introduce the metaphor, link the cast of "characters"
2. Topic block 1                 # motivation -> problem -> solution -> why -> result
3. Topic block 2
...
N. Q&A                          # 9-15 user-style questions answered in the same story voice
N+1. Glossary                   # key terms, in the user`s working language
N+2. Source map                 # what came from where
```

For each topic block:

- start with **why this topic exists** (motivation), told through the running story
- list the **problem** the previous approach could not solve, again through the story
- explain the **solution** in the story first, then write the formal definition, equation, or algorithm
- answer **why this design is enough**, with the strongest argument for and against
- close with **result** evidence when the original document gives it

Figure rules:

- For lecture slides, embed the full slide screenshot from `renders/pages/`.
- For research papers, embed a cropped figure from `screenshots/selected/`.
- Every embedded figure carries a one-line caption that says what the reader should take from it.
- Figures that needed image understanding cite that explanation file in `notes/`.

Link rules:

- Every claim that came from outside the PDF has a working URL.
- Every search query and result is in `search/`.
- The `N+2. Source map` section lists: PDF page references, search results used, and any image-understanding outputs used.

Style rules:

- Default to the user`s working language. Mix in English for technical terms in parentheses the first time they appear.
- Lead with story, follow with theory. Never lead with a definition.
- Use tables only as a support, not as the spine of a section.
- Use one warning block per major topic for the most common pitfall.
- Insert a real robotics or domain example for every abstract idea; if the PDF does not give one, search for one.

### 7. Validate Outputs

Before finishing, verify:

- a final note exists at the documented path, with a unique versioned filename
- a sibling `final/<doc-slug>_<lang>_<version>_assets/` directory exists and contains every image the note embeds
- every concept the user asked about in the original prompt is covered, in story form, in the note
- the running story is named once, in section 1, and reused consistently
- per-section motivation-problem-solution-why ordering holds for every topic block
- every search result used in the note has a URL in `N+2. Source map`
- every figure embedded in the note is present in the per-note assets folder

If the user is on a non-Default mode and asked for completion audit, append a short audit:

```text
Help-me-read audit:
- Page-by-page read: checked | blocked
- Divergent web search: checked | blocked
- Image understanding: checked | not applicable | blocked
- Story consistency: checked | blocked
- Image folder isolation: checked | blocked
- Source links: checked | blocked
- New-file rule: checked | blocked
```

## Failure Handling

- If the PDF is encrypted, record the error and ask the user for a decrypted copy.
- If text extraction returns empty for a page, render the page and run image understanding on it. Do not skip the page.
- If a search returns nothing useful, broaden the query by removing the technical noun and trying a Chinese variant.
- If image understanding returns nonsense, fall back to manual reading of the rendered page and label the explanation as "manual" in `notes/`.
- If the user`s chosen output path already has a note with the same slug+lang+version, do not overwrite. Bump the version and write the new file.
- If the user only has OCR available, treat OCR output as low-confidence and cross-check with a search for the same figure.

## Resources

Read these before writing prose:

- `references/style-guide.md` for the "story + theory" voice, term translation rules, and section rules
- `assets/template.md` for a blank close-read note skeleton to fill in
