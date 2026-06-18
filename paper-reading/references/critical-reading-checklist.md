# Critical Reading Checklist

A reading note is a record of what the paper actually says and what the evidence actually supports. The note is not a summary, not a press release, not a recommendation. The rules below are the minimum that separate a useful reading note from a vague one.

## The single rule

**Authors claim X. Evidence is at section Y / figure Z / table W. Evidence supports X: yes / no / partial. State the verdict in the note.**

Every claim in the note follows this pattern. No exceptions.

## Number rules

- **Every number carries a unit and a sample size.** "Achieves 92% accuracy" is incomplete. "Achieves 92% accuracy on the 5000-image test set" is complete. If the paper does not report the sample size, say so.
- **Improvement claims name the baseline.** "+3.4% over ResNet-50 on ImageNet val" is meaningful. "Significant improvement" is not. If the paper does not name the baseline, the claim cannot be verified.
- **Improvement claims report the metric, not the paper's words.** The paper says "outperforms all baselines by a large margin". The note says "+1.2 BLEU-4 on the test set vs the strongest baseline".
- **Multi-seed results report mean and spread.** A single-number table row is a red flag. If the paper reports a single number per cell, the note says so.

## Overclaim flags

A claim is an overclaim if any of the following holds. Flag it in section 7 of the note.

- The paper says "novel" or "first" but the same idea appeared in prior work. The note points to the prior work.
- The paper says "significantly better" but the actual number is below the conventional significance threshold (typically +2% on classification, +1 BLEU on translation, +0.05 on standard RL success rates; these are conventions, not absolutes).
- The paper says "state-of-the-art" on a benchmark but the table shows the result is within noise of the previous SOTA.
- The paper says "outperforms" a baseline but the comparison setup favors the proposed method (different hyperparameter budget, different training data, different evaluation protocol).
- The paper generalizes from one task to a broad claim about a subfield. The note narrows back to the specific task.

## Unevaluated scenarios

The paper's experiments do not cover all of the claims. For each broad claim, ask: what would a skeptical reader want to see that is missing?

- The paper claims "robust to distribution shift" but the experiments only test one type of shift.
- The paper claims "scales to large models" but the largest model in the table is still small by the field's standard.
- The paper claims "works in low-resource settings" but the experiments use 100x more data than the actual low-resource regime.
- The paper claims "general purpose" but the experiments are on two datasets.

List the unevaluated scenarios in section 7. The reader can then decide how much weight to give the claim.

## Reproducibility flags

- **Hyperparameter range not reported.** The paper says "we tuned the learning rate" but does not give the search space.
- **Training data not specified.** The paper says "we pre-trained on a large corpus" but does not name the corpus.
- **Single seed.** The paper reports a single number per cell without error bars or standard deviation.
- **Compute not reported.** The paper does not say how many GPUs or how many hours the training took.
- **Code or checkpoints not released.** The paper's results cannot be reproduced by an independent team.

List in section 7. Reproducibility is part of the contribution's weight, not a separate footnote.

## Critique rules

- **Do not use later vocabulary to judge earlier work.** A 2012 paper cannot be faulted for not using a 2020 technique. The critique is "what could the 2012 paper have done given 2012 tools and 2012 knowledge", not "the 2012 paper did not use the 2020 technique".
- **Do not overstate a small number into a dismissal.** A 0.5% improvement on a noisy benchmark is a real but small result. The note says "+0.5% on a noisy benchmark", not "the paper makes an unsubstantiated claim".
- **Do not understate a real gap into a footnote.** If the paper does not test a claimed scenario, the note says so in section 7, not buried in a parenthetical.
- **Cite the paper's own words when paraphrasing a claim.** If the paper says "we outperform the prior SOTA by 1.2 points", the note can say "the paper claims +1.2 over the prior SOTA" and then verify against the table.
- **Separate "the paper says" from "the evidence supports".** Use phrases like "the paper claims ...; the table shows ...". The reader can then judge.

## What the note must never contain

- "Groundbreaking", "revolutionary", "amazing", "stunning", "incredible". Replace with concrete claims and evidence.
- "The authors did a great job". Replace with the specific contribution the reader will use.
- "The paper is well-written". Replace with the specific structural choice that helped comprehension.
- "I recommend reading the paper". The reader is reading the note to decide whether to read the paper. State the criteria instead.
- "Everyone in the field is using this method". State the citation count if relevant, or omit.

## Output hygiene

- The note cites the paper's section, figure, or table for every claim.
- The note cites external sources with `[N]`, where the reference list at the end contains only external URLs.
- The note does not embed a process narration ("I first read the abstract, then I read the experiments"). The note is a deliverable, not a log.
- The note uses cropped figures, not whole-page renders. See `output-contract.md`.
