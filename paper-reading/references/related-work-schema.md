# Related Work Matrix Schema

`related_work_matrix.md` is the Phase 3 output: one row per paper in the target paper's comparison set plus the 1-3 "most classic" works in the subfield. This file defines the columns.

## Columns

| Column | What goes here |
|---|---|
| `paper` | Short label used in the matrix, e.g. "Dai et al. 2017" or "ScanNet". |
| `year` | Publication year. |
| `venue` | Conference or journal, e.g. "ICCV", "NeurIPS", "TPAMI". |
| `kind` | One of: `direct_baseline` (target paper compares against this in its tables), `classic_foundation` (1-3 most-cited works in the subfield, not necessarily in target's comparison set), `other_comparison` (mentioned in related work but not in tables). |
| `problem` | One phrase: what problem this paper addressed. |
| `method` | One short paragraph: the method or idea, in plain words. |
| `result` | The key reported result, with the metric and the dataset it was measured on. |
| `why_matters` | Why this paper is in the matrix: the role it plays in the lineage that the target paper builds on or contrasts with. |
| `source_url` | External URL (arXiv, DOI, publisher page) for the paper. |
| `local_path` | Absolute path in the resolved project paper directory where the PDF is saved. |

## Size limits

- **Cap the matrix at 15 rows total.** If the target paper cites more, pick the 15 most central to the target paper's claim. The cap keeps the matrix representative without forcing a shallow read of every cited paper.
- **Always include the 1-3 `classic_foundation` rows.** These may or may not be in the target paper's comparison set. If the target paper's claim depends on a long-standing result (e.g. ResNet, Transformer, CLIP), include that work even if the target paper does not cite it directly. The matrix documents the lineage; the target paper's reference list is not the same thing.
- **The target paper itself is NOT a row in this matrix.** The target paper is the subject of the reading; the matrix is its context.

## When to read what

For each row, read the cited paper's **abstract, introduction, and experiments** sections only. Do not read the full paper. The goal is "what problem, what method, what result, why it matters" - the columns above - and that information is in the first three sections of nearly every paper.

If a row's `method` or `result` column would require reading beyond the abstract, introduction, and experiments to fill in, the row is probably not pulling its weight in the 15-row cap. Replace it with a paper whose key contributions fit in those three sections.

## Worked example

Suppose the target paper is a few-shot 3D segmentation method. Two rows from `related_work_matrix.md`:

| paper | year | venue | kind | problem | method | result | why_matters | source_url | local_path |
|---|---|---|---|---|---|---|---|---|---|
| Dai et al. 2017 (ScanNet) | 2017 | ICCV | direct_baseline | 3D scene reconstruction and per-voxel semantic segmentation on RGB-D scans | RGB-D SLAM reconstruction, per-voxel annotation by crowdsourcing | 74.9% mIoU on the standard test split | Establishes the ScanNet annotation protocol and the RGB-D segmentation baseline that few-shot work measures against | https://arxiv.org/abs/1702.01105 | /home/user/projects/papers/dai-2017-scannet.pdf |
| Long et al. 2015 (FCN) | 2015 | CVPR | classic_foundation | Semantic segmentation on natural images | Fully convolutional networks replace the final FC layer with a 1x1 conv, upsampling via deconvolution | 62.7% mIoU on PASCAL VOC 2012 | Foundational work showing that dense per-pixel classification can be trained end-to-end; the conceptual ancestor of every modern segmentation method | https://arxiv.org/abs/1411.4038 | /home/user/projects/papers/long-2015-fcn.pdf |

## What NOT to do

- Do not pad the matrix to 15 rows when fewer are warranted. The cap is a maximum, not a target. A 5-row matrix from a paper that genuinely has 5 baselines is more useful than a 15-row matrix padded with tangential citations.
- Do not write a row without reading the cited paper. The matrix is a record of what was read, not a reconstruction of the target paper's reference list.
- Do not skip `source_url` or `local_path`. Both are required so the reader (and the writer, six months later) can find the PDF and the external link.
