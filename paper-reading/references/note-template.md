# Note Template

Use this 9-section structure verbatim. Section order is fixed. Section labels can be translated into the user's language when writing the final note.

The 9 sections correspond to the workflow phases: framing (1-5), depth (6), evaluation (7), critical reflection (8-9). Each section ends with a `**Citations used:**` line listing the numbered references invoked in that section. The full reference list lives once at the end of the note.

```markdown
# Paper Reading Note: <Title>

> Paper: <title>
> Authors: <authors>
> Venue / Year: <venue, year>
> arXiv / DOI: <link>
> Read on: <date>
> Language: <the language this note is written in>

## 1. Title

<Original title.>
<One-sentence core claim in plain words.>

**Citations used:** [1]

## 2. TL;DR (one-page summary)

<3-5 sentences: what this paper does, how, what result, why it matters.>
<If the paper claims X but evidence is weak, say so here.>

**Citations used:** [1]

## 3. What problem class does this paper belong to?

This section defines the problem class so the reader can understand the specific contribution in context. Read 1-2 foundational works during Phase 1 (see SKILL.md) and cite them here. Without the foundational works, this section reduces to a paraphrase of the target paper's introduction and is not informative on its own.

(a) **Input**: what does the model take in? (For example: RGB camera frames, language instruction string, robot proprioceptive state. Cite the section of the foundational work that defines the input schema.)
(b) **Output**: what does the model produce? (For example: action trajectory, per-timestep motor commands, gripper state. Cite the section of the foundational work that defines the output schema.)
(c) **Why this is hard**: long-horizon credit assignment, distribution shift between training and deployment, embodiment variability, reward sparsity for RL approaches, data collection cost. Cite specific limitations named in the foundational works.
(d) **Why this paper's specific claim matters within the problem class**: what gap or limitation in prior approaches does the paper position itself against? Quote the relevant transition paragraph from the target paper's introduction.

Cite BOTH the target paper (abstract + intro) AND the foundational works. Reference at least 1-2 entries from `related_work_matrix.md`.

**Citations used:** [1][N][M]

## 4. How did people solve this problem before this paper?

<3-5 most relevant prior works, one short paragraph each.>
<The single most classic prior work gets a longer paragraph: what it proposed, what its key result is, why it is foundational in the subfield.>
<See related_work_matrix.md for the full comparison set.>

**Citations used:** [2][3][4][5]

## 5. What is this paper's motivation?

<Author's stated pain point. The gap in prior work that the paper claims to close.>
<Quote the relevant transition paragraph at the end of the introduction or the start of the method section.>

**Citations used:** [1]

## 6. How does this paper solve the problem?

For each major design choice in the method, write a 1-paragraph block that follows the **Problem observed → Solution chosen → Why this design** pattern. Do not just list modules or describe the architecture; the reader needs to understand why each design choice exists.

### 6.1 <Design choice name, e.g. "Context conditioning">

- **Problem observed**: what limitation of prior work or what property of the data did the paper identify that motivated this design? Cite the section of the target paper where this observation is made.
- **Solution chosen**: what did the paper build, in plain words? Cite the section / equation / figure that describes the solution.
- **Why this design**: why does this solution address the observed problem? Reference how it relates to the limitation of prior work (cite entries from `related_work_matrix.md`).

### 6.2 <Design choice name>

(repeat the block above for each major design choice — typically 2-4 blocks per paper)

### 6.3 How the pieces fit together

<1-paragraph summary of the integrated system, then embed the architecture figure.>

![Figure N: <short caption summary>](figures/figure_N.png)

**Citations used:** [1][N][...]

## 7. What results did this paper achieve?

<Main table result, with concrete numbers and the baseline being beaten.>
<Insert a cropped figure for the headline result:>
![Figure 4: <short caption summary>](figures/figure_4.png)
<For each claimed improvement, note: by how much, on which benchmark, vs which baseline.>
<Then the critical observations:>
- Overclaim flags: <places where the paper says "significantly better" but the number is small, etc.>
- Unevaluated scenarios: <settings the paper does not test.>
- Benchmark mismatch flags: <link to benchmark_audit.md rows marked `mismatch: yes` or `mismatch: partial`.>
- Reproducibility notes: <missing details, hyperparameter ranges not reported, single-seed results, etc.>

**Citations used:** [1][6][7]

## 8. What are this paper's limitations?

<Author-stated limitations, from the limitations section or appendix.>
<Reader-identified limitations, from the experimental details and from the comparison to prior work.>
<Cite the section / appendix where each limitation is discussed.>

**Citations used:** [1]

## 9. What is this paper's contribution and significance?

<3 bullets:>
- Academic contribution: <what the paper adds to the body of knowledge.>
- Practical significance: <who can use this and for what.>
- Influence on follow-up work: <which subfield or problem this paper has shifted, and which open questions remain.>

<End with a 1-3 sentence qualitative verdict covering three points:

- what kind of paper this is (e.g., "method contribution with empirical validation on internal benchmarks", "survey with a strong opinionated framing", "incremental extension of a well-known method")
- who would benefit from reading it (e.g., "researchers working on VLA / data curation / RL post-training", "ML engineers evaluating generalist policies for their product")
- what is missing (e.g., "no external baseline comparison", "no code release", "limited ablation of the key design choice")

Do not give a numeric rating. Numeric ratings invite controversy and false precision; a qualitative verdict with explicit caveats is more useful and harder to misinterpret.>

**Citations used:** [1]

## References

[1] <author list>, "<title>", <venue> <year>. <external URL: arXiv / DOI / publisher page>
[2] <author list>, "<title>", <venue> <year>. <external URL>
[3] <author list>, "<title>", <venue> <year>. <external URL>
...
```

## How to fill this template

- **Section 1-2**: write after Phase 1 (skimming).
- **Section 3-5**: write after Phase 3 (prior art understood). Without prior art, "How did people solve this before" is shallow.
- **Section 6**: write after Phase 4 (deep read of method).
- **Section 7**: write after Phase 4 (deep read of experiments) **and** Phase 2 (benchmark audit). The benchmark-mismatch section in 7 is mandatory if any audit row is flagged.
- **Section 8-9**: write last, after the rest of the note is drafted, so the limitations and significance are grounded in the actual content rather than first impressions.

The cropped figures referenced in the note must exist in `figures/figure_N.png` relative to `paper_note.md`. A broken or missing figure must be fixed (re-crop, re-render, or re-copy into the note's `figures/` directory) before the note is declared done.

## Citation numbering convention

`[1]` is always the target paper itself. `[2]`, `[3]`, ... are the works cited in the note, in the order they are first introduced. The reference list at the end mirrors the numbering. The same number is used everywhere the work is cited. Numbers do not change between sections.
