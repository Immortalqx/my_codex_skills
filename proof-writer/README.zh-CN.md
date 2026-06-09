# proof-writer

[English](./README.md) | 中文

`proof-writer` 是一个用于撰写严谨数学证明的 Codex skill，主要面向 ML/AI 理论场景。它帮助 Codex 证明 theorem、lemma、proposition、corollary，补全证明草稿，识别缺失假设，或者在命题目前无法被证明时给出明确阻塞报告。

当你希望 Codex 把粗略命题或证明草稿整理成严谨证明包时，可以使用 `$proof-writer`：

```text
Use $proof-writer to prove the theorem in appendix_notes.md. If the claim is too strong, weaken it explicitly and write the corrected proof.
```

也可以直接给命题：

```text
Use $proof-writer to formalize this proof sketch and tell me whether the lemma is provable under the stated assumptions.
```

## 工作流程

1. Codex 收集定理陈述、假设、符号、本地草稿和已有证明思路。
2. Codex 规范化命题，但不会悄悄替换需要证明的原始结论。
3. Codex 判断命题属于原样可证、需要削弱或增加假设后可证，还是目前无法支撑。
4. Codex 写出结构化证明包，包括假设、符号、依赖图、证明、修正项和开放风险。
5. 如果关键步骤无法证明，Codex 会报告具体阻塞，而不是伪造证明。

## 输出

- 默认写入 `PROOF_PACKAGE.md`，除非用户指定其他目标文件。
- 在对话中简要说明证明状态、原命题是否保持不变，以及更新了哪个文件。

## 可安装目录

真正可安装的 Codex skill 是：

```text
proof-writer/proof-writer/
```

不要安装外层 `proof-writer/` 文件夹。外层只放这个仓库的说明文档。

## 内容

- `proof-writer/SKILL.md`：证明撰写工作流和严谨性规则。
- `proof-writer/agents/openai.yaml`：Codex skill 列表使用的 UI 元数据。
