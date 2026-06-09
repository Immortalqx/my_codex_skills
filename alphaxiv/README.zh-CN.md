# alphaxiv

[English](./README.md) | 中文

`alphaxiv` 是一个面向 arXiv 单篇论文的快速查询 skill。它优先读取公开的 AlphaXiv Markdown 页面；如果信息不足，再降级读取完整 AlphaXiv Markdown 或 arXiv LaTeX 源码。

当你给出 arXiv ID、arXiv URL、PDF URL 或 AlphaXiv URL，并希望 Codex 快速解释单篇论文时，可以使用 `$alphaxiv`：

```text
Use $alphaxiv to explain https://arxiv.org/abs/2401.12345 and focus on the method.
```

## 依赖说明

不需要本地 API key。这个 skill 依赖下列公开页面可访问：

- `https://alphaxiv.org/overview/<paper-id>.md`
- `https://alphaxiv.org/abs/<paper-id>.md`
- `https://arxiv.org/src/<paper-id>`

如果 AlphaXiv 尚未处理某篇论文，skill 会降级到更深层的公开来源。

## 工作流程

1. 从裸 arXiv ID、arXiv URL、PDF URL 或 AlphaXiv URL 中提取论文 ID。
2. 优先读取 AlphaXiv overview。
3. overview 不足时再读取完整 AlphaXiv Markdown。
4. 只有在用户需要公式、证明、附录细节或实现细节时，才读取 arXiv LaTeX 源码。
5. 返回简洁回答，并说明使用的来源深度。

## 内容

- `alphaxiv/SKILL.md`：Codex skill 定义。
- `alphaxiv/agents/openai.yaml`：UI 元数据。
