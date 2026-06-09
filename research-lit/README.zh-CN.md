# research-lit

[English](./README.md) | 中文

`research-lit` 是一个独立的 Codex skill，用于检索、对比和综合研究论文。默认路径只依赖本地 PDF、公共网页检索和随 skill 打包的 arXiv 元数据脚本。

当你希望 Codex 查找相关工作、总结某个研究方向，或者理解一组论文在讲什么时，可以使用 `$research-lit`：

```text
Use $research-lit to find recent papers about diffusion policies for robot manipulation and summarize the main method families.
```

如果想限制信息来源，也可以这样说：

```text
Use $research-lit to survey test-time scaling for VLM agents, sources: local, web, arxiv download: true.
```

## 工作流程

1. Codex 解析研究主题、信息来源、本地论文库路径和可选的 arXiv 下载设置。
2. Codex 扫描本地 `papers/`、`literature/` 或用户显式指定的论文目录。
3. Codex 使用公共网页检索补充近期论文和官方页面。
4. Codex 使用内置 arXiv 辅助脚本获取结构化元数据，并在用户要求时下载 PDF。
5. Codex 按 arXiv ID、URL 或规范化标题去重。
6. Codex 按问题、方法、结果、相关性和来源分析每篇论文，并输出综合结果。

## 输出

- 带引用元数据、方法摘要、关键结果、相关性和来源的文献表格。
- 对领域格局的简短叙述性总结。
- 可选地把 arXiv PDF 下载到 `papers/`、`literature/` 或用户指定目录。

## 辅助脚本

- [research-lit/scripts/arxiv_fetch.py](./research-lit/scripts/arxiv_fetch.py)：随 skill 打包的 arXiv Atom API 搜索和 PDF 下载辅助脚本。

## 可安装目录

真正可安装的 Codex skill 是：

```text
research-lit/research-lit/
```

不要安装外层 `research-lit/` 文件夹。外层只放这个仓库的说明文档。

## 内容

- `research-lit/SKILL.md`：文献调研工作流。
- `research-lit/scripts/`：skill 自带的确定性辅助脚本。
- `research-lit/agents/openai.yaml`：Codex skill 列表使用的 UI 元数据。
