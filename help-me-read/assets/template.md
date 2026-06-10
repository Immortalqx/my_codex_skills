# <Doc Title> Close-Read Note

> **Source PDF**: <relative or absolute path to the source PDF> > **Note type**: Close-read (tutor-style), not a reference manual > **Working language**: <the user`s working language for this note, e.g. "Chinese" or "English"> > **Running story**: <one sentence naming the metaphor> > > If a prior note for the same PDF already exists in this folder, **do not overwrite it**. Bump the version suffix on this file.

---

## 0. How To Read This Note

- First time: read section 0 -> section 1 -> topic blocks in order
- Looking up a concept: jump to the matching topic block, or to the Glossary in N+1
- Auditing sources: jump to N+2 Source Map

---

## 1. Running Story: <metaphor name>

> 3-5 sentences that establish the metaphor in the user`s working language. Include a "cast of characters" table (story role <-> formal concept) so the rest of the note can lean on it.

| Story role | Formal concept |
|---|---|
| ... | ... |
| ... | ... |

---

## 2. Topic Block 1

### 2.1 Motivation: Why does this topic exist?

**Story beat.** 2-4 sentences in the running story that set up *why this topic exists at all*.

### 2.2 Problem: Where did the previous approach break?

- The previous approach is a *named* thing (DQN, VPG, DDPG, ...), not "old methods".
- Show the failure through the story.
- Cite a search result or paper when the PDF does not give the full history.

### 2.3 Solution: How is it fixed?

**Story beat.** Walk through the new idea in the story first, 3-6 sentences.

**Formal.** Equation or algorithm pseudocode, in a fenced code block.

**Reading.** 2-3 sentences that translate the formal block into plain words.

**Example.** One concrete scenario with real numbers and real objects (e.g. a 7-DOF arm, HalfCheetah, CartPole).

### 2.4 Why is this design enough?

- Strongest argument for the design.
- Strongest argument against, or known caveat.
- One `> Warning ...` block allowed here.

### 2.5 Result

- Concrete numbers from the PDF or a search result.
- Cite the URL in N+2 Source Map.

---

## 3. Topic Block 2

(Same structure as block 1.)

---

## N. Q&A

1. **<question>** -> <3-8 sentences in story voice>
2. **<question>** -> ...
3. ...

---

## N+1. Glossary (in user`s working language)

| English | Chinese (if applicable) | One-sentence definition |
|---|---|---|
| ... | ... | ... |

---

## N+2. Source Map

### From the PDF

- Page P3: definition of the MDP tuple
- Page P12: actor-critic architecture diagram
- ...

### From Web Search (saved to `search/results/`)

- `<query-slug>.md`: 1-3 sentence takeaway + original URL
- ...

### From Image Understanding (saved to `notes/`)

- `figure_<n>_explanation.md`: 1-3 sentences on what the figure conveys
- ...

---

## Appendix A: Figure Index

| Figure | Source | Caption | File |
|---|---|---|---|
| Figure 1 | PDF P3, full page | MDP tuple structure | `_assets/pages/lecture_p03.png` |
| Figure 2 | PDF P7, region crop | Bellman backup flow | `_assets/selected/figure_02.png` |
| ... | ... | ... | ... |