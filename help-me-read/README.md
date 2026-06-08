# help_me_read

[Chinese version](./README.zh-CN.md)

`help-me-read` is a Codex skill that **deep-reads a single user-provided PDF** and writes a story-driven close-read note in the user`s working language.

The skill is designed for the case where the user hands over a lecture-slide PDF or a research paper and wants a study note that:

- has a single running metaphor or story that explains every concept
- structures each topic as motivation -> problem -> solution -> why -> result
- glosses every key term on first appearance
- embeds screenshots of slides and cropped figures from the paper
- cites every claim that came from outside the PDF with an original URL
- is written to a new versioned file and never overwrites an existing note

## When To Use

Use this skill when the user asks for:

- a close-read, detailed study notes, tutor-style breakdown, or deep study notes of a single PDF
- per-section motivation-problem-solution-why explanations, not a summary
- a clean new note file next to existing ones, not an overwrite

Do not use this skill for casual summaries, slide-by-slide transcription, or one-line Q&A about a paper.

## How It Works

1. Identify the input PDF, the working language, and the target output path.
2. Extract per-page text and per-page PNG screenshots (200+ DPI). For papers, also crop figures that will be embedded.
3. Run divergent web searches to fill in the background that is not in the PDF: original paper, canonical explainer, predecessor and successor, and a Chinese-language explainer when the working language is Chinese.
4. Call an image-understanding tool on dense figures (architecture diagrams, plot families) and store the explanation next to the figure.
5. Design one running metaphor that maps cleanly to every concept in the document.
6. Write the close-read note in the user`s working language, with one topic block per major idea and a Q&A block at the end.
7. Validate the output: per-note asset folder is isolated, every embedded image resolves, every source link is reachable, no existing note was overwritten.

## Output Layout

When the user does not specify a path, the skill creates:

```text
<workspace>/<temp-root>/help-me-read/<doc-slug>/ (the temp-root name follows the user's existing convention; skill does not hard-code it)
  prompt.txt
  task_summary.md
  sources/
    user_files/        # the original PDF, untouched
    fetched/           # web pages and arXiv papers downloaded for grounding
  extracted_text/      # per-page text
  renders/pages/       # full-page PNGs
  screenshots/selected/  # cropped figures for embedding
  search/queries/      # exact queries that were run
  search/results/      # short notes + original links per result
  notes/               # per-topic drafts, image-understanding outputs
  final/
    <doc-slug>_<lang>_<version>.md
    <doc-slug>_<lang>_<version>_assets/  # self-contained, next to the note
```

When the user points at an existing folder ((the users target output directory)), the skill writes into sibling subfolders instead of a new top-level temp root.

## Repository Layout

- `README.md` and `README.zh-CN.md`: repository docs
- `help-me-read/`: Codex skill files
- `help-me-read/SKILL.md`: skill definition and workflow
- `help-me-read/references/style-guide.md`: voice, term glossing, section rules
- `help-me-read/assets/template.md`: blank close-read note skeleton
- `help-me-read/agents/openai.yaml`: UI metadata
