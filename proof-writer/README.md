# proof-writer

English | [中文](./README.zh-CN.md)

`proof-writer` is a Codex skill for writing mathematically honest proofs for ML and AI theory. It helps Codex prove theorem, lemma, proposition, and corollary statements, repair proof sketches, identify missing assumptions, or report when a claim is not currently justified.

Use `$proof-writer` when you want Codex to turn a rough claim or proof sketch into a rigorous proof package:

```text
Use $proof-writer to prove the theorem in appendix_notes.md. If the claim is too strong, weaken it explicitly and write the corrected proof.
```

For a direct prompt:

```text
Use $proof-writer to formalize this proof sketch and tell me whether the lemma is provable under the stated assumptions.
```

## Workflow

1. Codex gathers the theorem statement, assumptions, notation, local drafts, and any proof sketch.
2. Codex normalizes the claim without silently changing what must be proved.
3. Codex classifies the claim as provable as stated, provable after weakening or an extra assumption, or not currently justified.
4. Codex writes a structured proof package with assumptions, notation, dependency map, proof, corrections, and open risks.
5. If a key step cannot be justified, Codex reports the blocker instead of fabricating a proof.

## Outputs

- A proof package, usually `PROOF_PACKAGE.md` unless the user specifies another target file.
- A short chat summary of the proof status, whether the original claim survived unchanged, and which file was updated.

## Installable Directory

The installable Codex skill is:

```text
proof-writer/proof-writer/
```

Do not install the outer `proof-writer/` folder. It contains repository README files only.

## Contents

- `proof-writer/SKILL.md`: proof-writing workflow and rigor rules.
- `proof-writer/agents/openai.yaml`: UI metadata for Codex skill lists.
