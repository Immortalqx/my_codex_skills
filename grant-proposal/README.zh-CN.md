# grant-proposal

[English](./README.md) | 中文

`grant-proposal` 用于把研究 idea 和文献材料整理成结构化基金申请书。它支持 KAKENHI、NSF、NSFC、ERC、DFG、SNSF、ARC、NWO 和通用 proposal 格式。

当你希望 Codex 根据一个研究方向起草基金申请时，可以使用 `$grant-proposal`：

```text
Use $grant-proposal to draft an NSFC Youth proposal from this research idea.
```

## 依赖说明

不需要本地 API key。这个 skill 基于用户请求、本地项目文件，以及网络可用时的公开文献和基金机构页面工作。

## 工作流程

1. 自动识别基金机构、子类型、语言和输出格式。
2. 收集项目 idea、PI 背景、文献和相关已获资助项目。
3. 组织 aims、milestones、可行性、风险、预期成果和预算理由。
4. 按机构风格起草申请书。
5. 根据机构评审标准自检，并修正明显弱点。
6. 写出申请书、草稿说明和简单恢复状态文件。

## 内容

- `grant-proposal/SKILL.md`：Codex skill 定义。
- `grant-proposal/agents/openai.yaml`：UI 元数据。
