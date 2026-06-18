# Benchmark Guard

A benchmark is a test, not an oracle. The way a paper uses a benchmark is part of its claim, and that claim needs verification.

## Why this matters

Benchmarks are designed for specific tasks. A benchmark designed for task A is not automatically a valid test for task B. The borrow is sometimes legitimate (the benchmark happens to be a clean proxy for B), and sometimes not (the paper uses A to claim progress on B without explaining how A tests B). Examples of the failure mode:

- An embodied agent paper borrows a static-image classification benchmark to claim "generalization to novel objects". The benchmark was never designed to test object-level physical interaction.
- A 3D-reconstruction paper borrows a semantic-segmentation benchmark to claim "semantic understanding of scenes". The benchmark scores per-pixel class labels, not reconstruction quality.
- A navigation paper borrows a VQA benchmark to claim "language-grounded navigation". The benchmark tests static-image VQA, not sequential decision-making.

The paper's own framing of the benchmark is not enough. The auditor reads the original benchmark paper to confirm the original purpose and the input and output schema.

## The audit row schema

For every benchmark the paper uses, fill one row in `benchmark_audit.md` using this schema:

| Field | What goes here |
|---|---|
| `benchmark` | Common name, e.g. "ScanNet", "ImageNet", "CLEVR". |
| `original_paper` | Title, authors, year. The first public paper that introduced the benchmark, not a survey. |
| `original_task` | One phrase: classification, detection, reconstruction, VQA, navigation, and so on. |
| `input` | Concrete input: RGB image, RGB-D pair, mesh, point cloud, video, text prompt, and so on. |
| `output` | Concrete output: class label, mask, mesh, answer string, action sequence, and so on. |
| `metric` | The score used: accuracy, mIoU, Chamfer distance, BLEU, success rate, and so on. |
| `paper_usage` | One-sentence description of how the target paper uses this benchmark. Quote or paraphrase from the target paper. |
| `local_path` | The resolved project paper directory path where the original benchmark paper PDF is saved. |
| `mismatch` | One of: `no` (task matches), `partial` (overlap but not exact), `yes` (the original task differs significantly from the paper's use). |

A row with `mismatch: yes` or `mismatch: partial` must be **flagged in the final note**, in section 7 "What results did this paper achieve?" under a "Benchmark mismatch flags" bullet.

## How to fill the row

For each benchmark:

1. **Locate the original benchmark paper.** If the target paper cites a primary source, that is the primary source. If the target paper only cites a survey, follow the survey's citations to the primary source.
2. **Download the primary source PDF** into the resolved project paper directory. Record the absolute path in `local_path`. Do not rely on a survey, the original paper's arXiv landing page, or a third-party blog post.
3. **Read the primary source's abstract, introduction, and task-definition section.** These three pieces answer `original_task`, `input`, `output`, and `metric`. Skim the rest.
4. **Read the target paper's section that introduces this benchmark.** Usually in the "Experimental setup" or "Datasets" subsection of the experiments chapter. Find the one paragraph that says what the paper does with this benchmark.
5. **Compare the two.** Ask: is the paper using this benchmark in the way the original task definition supports? Or has the paper redefined the task in a way the original benchmark was not designed for?
6. **Set `mismatch`.** If the paper's usage matches the original task definition, set `mismatch: no`. If the paper's usage is a strict subset of the original task and the metrics carry over, set `mismatch: no`. If the paper extends the task but the extension is reasonable, set `mismatch: partial`. If the paper's claim is "we improve X" and the benchmark does not test X, set `mismatch: yes`.

## Worked example

Suppose the target paper claims "we improve few-shot semantic segmentation on ScanNet". Row:

- `benchmark`: ScanNet
- `original_paper`: Dai et al., "ScanNet: Richly-annotated 3D reconstructions of indoor scenes", ICCV 2017
- `original_task`: 3D scene reconstruction and instance-level semantic segmentation on RGB-D scans
- `input`: RGB-D sequence of an indoor scene
- `output`: Per-voxel semantic label and instance mask
- `metric`: mIoU, per-class accuracy
- `paper_usage`: Used as a few-shot segmentation benchmark. Three labeled examples per novel class.
- `local_path`: /home/user/projects/papers/dai-2017-scannet.pdf
- `mismatch`: no

Suppose instead the target paper claims "we improve embodied navigation on ScanNet". Row:

- `benchmark`: ScanNet
- `original_paper`: Dai et al., "ScanNet: Richly-annotated 3D reconstructions of indoor scenes", ICCV 2017
- `original_task`: 3D scene reconstruction and instance-level semantic segmentation
- `input`: RGB-D sequence
- `output`: Per-voxel label and instance mask
- `metric`: mIoU
- `paper_usage`: Used as a navigation benchmark. The agent moves in a ScanNet scene and must reach a target.
- `local_path`: /home/user/projects/papers/dai-2017-scannet.pdf
- `mismatch`: yes

In the second case, the original benchmark did not test navigation. The paper's "navigation on ScanNet" is a new evaluation protocol overlaid on an existing dataset, which is fine if the paper is honest about it. If the paper says "we improve ScanNet performance" without disambiguating, the note must flag this.

## What to put in the final note when a mismatch is found

In `paper_note.md` section 7, under "Critical observations", include a bullet like:

- **Benchmark mismatch warning**: `<paper> uses <benchmark> for <paper's task>, but the original benchmark task is <original task>. The paper's metric on this benchmark therefore does not directly support the paper's claim of progress on <paper's task>. See benchmark_audit.md row "<benchmark>".`

The warning is in the user's language. Keep it factual. Do not overstate ("the paper is wrong") or understate ("the benchmark might not be perfect"). State the gap.

## What NOT to do

- Do not assume the target paper's framing of a benchmark is correct without reading the original.
- Do not skip audits because the benchmark is "well-known". Famous benchmarks are borrowed across mismatched tasks more often than obscure ones.
- Do not silently merge two distinct benchmarks into one audit row. If the paper uses ScanNet for segmentation and ScanNet for navigation, that is two rows.
- Do not audit a benchmark the paper does not use. Audit only what the paper actually runs experiments on.
