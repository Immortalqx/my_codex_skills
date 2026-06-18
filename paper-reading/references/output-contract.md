# Output Contract

These rules are non-negotiable. Every reading note produced by this skill must satisfy them. The rules are not stylistic preferences; they are the boundary between a useful note and a deliverable that misleads the reader.

## Rule 1: Numbered citations, external links only

Every paper, book, report, or other work referenced in the note uses a numbered citation in square brackets, e.g. `[1]`, `[2]`, `[3]`. The reference list at the end of the note contains one entry per citation number, in the form:

```
[1] Author List, "Title", Venue Year. https://external-url
```

The URL in each reference must be an **external** link: an arXiv abstract page, a DOI resolver, or a publisher page. The reference list must **not** contain:

- Local file paths (no `papers/foo.pdf`, no `x_temp/...`, no `D:\...`).
- GitHub URLs to a private fork or to the user's own notes.
- Search-engine query URLs.
- Any URL that is not directly resolvable to the cited work.

If a cited work has no publicly accessible URL, **remove the citation entirely** and rely on whatever in-text citation the note can support without it. Do not invent a URL.

## Rule 2: Read the original, not the summary

Every cited work must have been read in the original during this reading session. The note must not cite a paper based on:

- The target paper's paraphrase of it.
- A blog post or survey.
- A previous reading note (including notes in the same `x_temp/paper-reading/...` tree).
- An LLM's recollection of its content.

If the original could not be obtained, the note says so at the point of citation ("[1] was not directly read; the following is taken from the target paper's description of [1]") and the claim is downgraded.

## Rule 3: Downloaded papers live in the project paper directory

Every paper that is read in original form during this session is downloaded into the **project paper directory** that the skill resolved at the start of the session. The audit files (`benchmark_audit.md`, `related_work_matrix.md`) record the absolute path in their `local_path` columns. The reference list at the end of the note does not need to include these local paths.

Papers never live inside the skill folder. The skill folder is meant to be reusable across projects; copying papers into it makes that impossible.

## Rule 4: The note is a standalone document

The note contains no:

- Conversational artifacts ("the user asked me to...", "I think that...").
- Process narration ("First I read the abstract, then I skimmed the experiments...").
- Local file indices ("papers in this directory: ...").
- TODOs or placeholders.

The note is what the reader needs in order to understand the paper. The reader does not see the session log, the audit files, or the figure-crop script. The note is the deliverable.

## Rule 5: No "rather than" sentence pattern

Avoid the pattern "X is A, rather than B" and the Chinese equivalent "X 是 A，而不是 B". The pattern is overused in this style of writing and obscures the actual claim. Replace with a direct statement:

- Bad: "The method is scalable rather than exhaustive."
- Good: "The method scales linearly with input size; the exhaustive baseline scales quadratically."

## Rule 6: No anachronistic critique

Do not fault an early work for lacking a later technique. If the target paper is from 2018 and uses a method that a 2024 paper improved on, the note does not say "the 2018 paper does not use the 2024 technique" as if that were a flaw. The critique is grounded in the tools and knowledge available at the time the cited work was published.

## Rule 7: Figures are cropped, not whole pages

Every figure embedded in the note is a cropped image that shows the figure body, not the surrounding page. The crop must:

- Contain the figure body (axes, plot, diagram).
- Not contain other figures, page headers, page numbers, or large areas of whitespace.
- Be at a DPI where the figure's internal text is legible in the note.

A figure embedded as a whole-page render, even if the page is mostly the figure, fails this rule. Re-crop until the figure is informative.

The final Markdown note must point only to figure files that resolve relative to `paper_note.md`, typically `figures/figure_N.png`. Do not link the final note to scratch artifacts under `x_temp/`.

## Rule 8: Output language matches user input

The note is written in the language the user used to invoke the skill. Chinese question -> Chinese note. English question -> English note. If the user explicitly specifies a language, that language is used. Section labels in the template can be translated. References stay in their original language (author names, titles). Citation numbers stay as `[1]`, `[2]`, etc., regardless of note language.

## Self-check before delivery

Before declaring the note done, verify every item below. If any item fails, fix and re-check. Do not deliver a note that fails the self-check.

- [ ] All 9 sections from `note-template.md` are present and in order.
- [ ] Every numerical claim in the note carries a unit and a sample size (or the note says the paper does not report the sample size).
- [ ] Every claim in the note cites a section, figure, or table from the paper, or a numbered external reference.
- [ ] The reference list at the end of the note contains only external URLs.
- [ ] No `papers/`, `x_temp/`, or other local path appears in the reference list.
- [ ] No conversational artifact, process narration, or TODO appears anywhere in the note.
- [ ] No "rather than" or "而不是" sentence appears in the note. (This is a style rule; a single occurrence is not a fatal failure, but the note should be reviewed and rewritten if the pattern is heavy.)
- [ ] Every embedded figure is a cropped image, not a whole-page render. The figure is informative at note-zoom.
- [ ] Every embedded figure path resolves relative to `paper_note.md`, typically under `./figures/`.
- [ ] Every benchmark in `benchmark_audit.md` marked `mismatch: yes` or `mismatch: partial` has a corresponding warning in section 7 of the note.
- [ ] Every paper cited in the note was read in original during this session, or the note says at the point of citation that the original was not directly read.
- [ ] The note is in the user's language. If the user did not specify a language, the note is in the language the user used to invoke the skill.
