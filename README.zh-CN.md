# my_codex_skills

[English](./README.md) | 中文

这是我维护的一组 Codex skills，主要覆盖科研、写作、文档生产、项目导航等可复用工作流。

本仓库的每个顶层目录都是一个可安装的 skill。一个合法的 skill 目录会在根部包含 `SKILL.md`，并可按需包含 `agents/`、`scripts/`、`references/`、`assets/` 等目录。

## Skill 列表

- [`alphaxiv`](./alphaxiv/) - 快速解释单篇 arXiv 论文，优先使用 AlphaXiv 内容，必要时再回退到源材料。
- [`arxiv`](./arxiv/) - 搜索 arXiv、获取元数据，并把论文 PDF 下载到本地文献库。
- [`doc-coauthoring`](./doc-coauthoring/) - 面向 spec、proposal、PRD、RFC、decision doc 的结构化协同写作流程。
- [`docx`](./docx/) - 创建、检查和编辑 Word 文档，支持批注、修订等工作流。
- [`drawio-diagram`](./drawio-diagram/) - 生成可编辑的 draw.io 科研图，并导出 PNG、SVG、PDF 后做视觉 QA。
- [`figure-description`](./figure-description/) - 为专利附图生成正式说明文字和附图标记映射。
- [`formula-derivation`](./formula-derivation/) - 从问题设定和假设出发整理、推导研究公式。
- [`grant-proposal`](./grant-proposal/) - 基于研究想法和文献上下文撰写结构化基金申请书。
- [`help-me-read`](./help-me-read/) - 深读用户提供的 PDF，并生成故事化、教学式的学习笔记。
- [`mmx-cli`](./mmx-cli/) - 直接操作本地 MiniMax CLI，处理文本、搜索、视觉、额度和媒体任务。
- [`mock-review`](./mock-review/) - 在正式投稿前，以 reviewer 视角对论文做一次模拟审稿。
- [`novelty-check`](./novelty-check/) - 围绕相近工作检查研究想法的新颖性风险。
- [`pdf`](./pdf/) - 处理 PDF 的阅读、提取、填写、编辑和生成任务，包含表单工作流。
- [`phd-benchmark-paper-template`](./phd-benchmark-paper-template/) - 用五支柱框架组织 benchmark / evaluation 论文。
- [`phd-figure-designer`](./phd-figure-designer/) - 设计并审查 technical paper 中最关键的几类图。
- [`phd-idea-evaluator`](./phd-idea-evaluator/) - 从强度、可行性和生命周期匹配等维度评估研究想法。
- [`phd-intro-drafter`](./phd-intro-drafter/) - 为 technical paper 构建六段式 Introduction 大纲。
- [`phd-pre-submission-reviewer`](./phd-pre-submission-reviewer/) - 从逻辑、写作、语法、LaTeX、图质量等维度做投稿前审查。
- [`phd-tech-paper-template`](./phd-tech-paper-template/) - 构建 technical paper 的逻辑骨架与一致性检查。
- [`phd-vibe-research-workflow`](./phd-vibe-research-workflow/) - 规划 AI 辅助科研工作流，同时把学术判断牢牢留在用户手里。
- [`pptx`](./pptx/) - 创建、检查和编辑 PowerPoint，并要求经过完整 QA 循环。
- [`proof-writer`](./proof-writer/) - 把 theorem / lemma 的草稿和思路整理成严谨证明。
- [`research-lit`](./research-lit/) - 结合本地 PDF、公开网络和 arXiv 元数据做独立文献调研。
- [`research-survey-loop`](./research-survey-loop/) - 维护长期 survey 任务，持续读文献并迭代写中文综述。
- [`research-wiki`](./research-wiki/) - 构建项目级持久化 research wiki，沉淀论文、想法、实验和 claim。
- [`theme-factory`](./theme-factory/) - 为 slides、docs 和轻量 artifact 应用内置主题或派生新主题。
- [`update-source-map`](./update-source-map/) - 为陌生代码仓库建立或刷新结构化 source map。
- [`xlsx`](./xlsx/) - 创建、修复、分析和扩展 spreadsheet 文件，同时保留公式和工作簿结构。

## 安装

把每个顶层 skill 目录直接复制到 `$CODEX_HOME/skills`：

```text
source: <this-repo>/<skill>/
target: $CODEX_HOME/skills/<skill>/
copy the directory contents as-is
skip any __pycache__ directory
```

不要把 `temp/` 这类仓库内的辅助目录安装进去。

安装或更新后，重启 Codex，让新的 skill metadata 生效。

## 说明

- `phd-` 前缀用于给导入的论文写作和科研规划类 skill 做命名空间隔离。
- 这些 skill 按“独立 Codex 使用”设计，默认可以使用本地脚本、本地文件和常规网页访问。
- 部分 skill 依赖本地工具，例如 LibreOffice、Poppler、`pandoc`、`markitdown`、`mmx` 或其他运行时，具体要求见各 skill 内部说明。
- `mock-review` 这类 review 风格 skill 产生的是模拟反馈，不能冒充正式审稿意见。
