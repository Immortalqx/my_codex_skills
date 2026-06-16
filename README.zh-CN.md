# my_codex_skills

[English](./README.md) | 中文

这是我个人维护的一组 Codex skills，用来沉淀可复用的科研、写作、文档生产和项目导航工作流。

本仓库中的每个 skill 都是一个顶层目录。一个合法的 skill 目录会在根部包含 `SKILL.md`，并可按需包含 `agents/`、`scripts/`、`references/`、`assets/` 等内容。

除非某个 skill 自己明确说明，否则这些 skills 默认面向独立使用 Codex：本地脚本、本地文件和正常公共网页访问都属于预期路径；隐藏的 reviewer 链路、通知钩子和隐式跨 skill 编排不属于默认流程。

## Skills

| Skill | 简介 | 典型用途 |
| --- | --- | --- |
| [`alphaxiv`](./alphaxiv/) | 快速解释单篇 arXiv 论文，优先使用 AlphaXiv 内容，必要时再回退到源材料。 | 根据 arXiv ID 或 URL 快速理解单篇论文，而不是做大范围文献综述。 |
| [`arxiv`](./arxiv/) | 搜索 arXiv、获取元数据，并把论文 PDF 下载到本地文献库。 | 查找预印本、按查询词或 arXiv ID 下载 PDF，并维护本地论文集合。 |
| [`doc-coauthoring`](./doc-coauthoring/) | 面向 spec、proposal、PRD、RFC、decision document 的结构化协同写作流程。 | 规划、起草和迭代长篇协作文档。 |
| [`docx`](./docx/) | 创建、检查和编辑 Word 文档，支持批注、修订等工作流。 | Word 编辑、修订、批注和 OOXML 感知型文档处理。 |
| [`drawio-diagram`](./drawio-diagram/) | 生成可编辑的 draw.io 科研图，并导出 PNG、SVG、PDF 后做视觉 QA。 | 论文配图、海报和概念图，尤其适合需要保留 draw.io 可编辑草稿的场景。 |
| [`figure-description`](./figure-description/) | 为专利附图生成正式说明文字和附图标记映射。 | 根据本地技术图准备 CN/US/EP 专利附图说明和附图标记索引。 |
| [`formula-derivation`](./formula-derivation/) | 从问题设定和假设出发整理、推导研究公式。 | 把理论笔记整理成论文风格推导框架或 blocker report。 |
| [`grant-proposal`](./grant-proposal/) | 基于研究想法和文献上下文撰写结构化基金申请书。 | 把研究方向转成带机构格式、研究目标、里程碑和预期成果的 funding application。 |
| [`mmx-cli`](./mmx-cli/) | 直接操作本地 MiniMax CLI，处理文本、搜索、视觉、额度和媒体任务。 | 当 Codex 需要通过已配置好的本地 `mmx` 命令工作时使用。 |
| [`mock-review`](./mock-review/) | 在正式投稿前，以 reviewer 视角对论文做一次模拟审稿。 | 投稿前风险排查、rebuttal 准备和 reviewer-style critique。 |
| [`novelty-check`](./novelty-check/) | 围绕相近工作检查研究想法的新颖性风险。 | 在投入实现时间前先筛查一个方法是否可能已经被做过。 |
| [`pdf`](./pdf/) | 处理 PDF 的阅读、提取、填写、编辑和生成任务，包含表单工作流。 | PDF 提取、表单填写、编辑和验证型文档处理。 |
| [`phd-benchmark-paper-template`](./phd-benchmark-paper-template/) | 用五支柱框架组织 benchmark / evaluation 论文。 | 规划 benchmark 或 evaluation 论文的 Introduction 逻辑、pipeline 和实验结构。 |
| [`phd-figure-designer`](./phd-figure-designer/) | 设计并审查 technical paper 中最关键的几类图。 | 决定论文图的范式、布局、标注和 QA 规则。 |
| [`phd-idea-evaluator`](./phd-idea-evaluator/) | 从强度、可行性和生命周期匹配等维度评估研究想法。 | 在实现或写作开始前，对 paper idea 做压力测试。 |
| [`phd-intro-drafter`](./phd-intro-drafter/) | 为 technical paper 构建六段式 Introduction 大纲。 | 在真正写 Introduction prose 前先搭建论文故事骨架。 |
| [`phd-pre-submission-reviewer`](./phd-pre-submission-reviewer/) | 从逻辑、写作、语法、LaTeX、图质量等维度做投稿前审查。 | 正式提交前的终稿审查。 |
| [`phd-tech-paper-template`](./phd-tech-paper-template/) | 构建 technical paper 的逻辑骨架与一致性检查。 | 正式起草前的 technical paper 规划，尤其适合师生讨论。 |
| [`phd-vibe-research-workflow`](./phd-vibe-research-workflow/) | 规划 AI 辅助科研工作流，同时把学术判断牢牢留在用户手里。 | 组织 coding、figure、writing 三类科研 session，并明确研究诚信边界。 |
| [`pptx`](./pptx/) | 创建、检查和编辑 PowerPoint，并要求经过完整 QA 循环。 | 需要 artifact 校验的幻灯片创建和修复工作流。 |
| [`proof-writer`](./proof-writer/) | 把 theorem 或 lemma 的草稿和思路整理成严谨证明。 | 把粗糙命题或证明思路整理成可辩护的证明包。 |
| [`research-lit`](./research-lit/) | 结合本地 PDF、公开网络和 arXiv 元数据做独立文献调研。 | 查找 related work、梳理领域版图并比较相近方法簇。 |
| [`research-survey-loop`](./research-survey-loop/) | 维护长期 survey 任务，持续读文献并迭代写中文综述。 | 需要多轮持续推进的文献综述任务。 |
| [`research-wiki`](./research-wiki/) | 构建项目级持久化 research wiki，沉淀论文、想法、实验和 claim。 | 在多个 session 之间保留项目级研究记忆。 |
| [`theme-factory`](./theme-factory/) | 为 slides、docs 和轻量 artifact 应用内置主题或派生新主题。 | 复用或派生一致的视觉主题。 |
| [`update-source-map`](./update-source-map/) | 为陌生代码仓库建立或刷新结构化 source map。 | 在深入工作前为项目创建或刷新 agent 可读索引。 |
| [`xlsx`](./xlsx/) | 创建、修复、分析和扩展 spreadsheet 文件，同时保留公式和工作簿结构。 | Spreadsheet 编辑、重算和保结构自动化。 |

## 安装

上表中的每个顶层 skill 目录都可以直接安装到 `$CODEX_HOME/skills`。

```text
source: <this-repo>/<skill>/
target: $CODEX_HOME/skills/<skill>/
copy the directory as-is
```

如果想安装整个集合，对上表中的每个顶层 skill 目录重复同样的拷贝规则即可。

安装或更新后，重启 Codex，让新的 skill metadata 生效。

## 说明

- 这些 skills 是个人科研工作流沉淀，不代表任何会议、期刊或机构的官方流程。
- `phd-` 前缀用于给本仓库中的一组论文写作和科研规划类 skill 做命名空间隔离。
- 除非某个 skill 自己明确说明，否则这些 skills 默认面向独立 Codex 使用，允许本地脚本、本地文件和正常网页访问。
- 部分 skill 依赖本地工具，例如 LibreOffice、Poppler、`pandoc`、`markitdown`、`mmx` 或其他运行时，具体要求见对应 skill 目录内说明。
- `mock-review` 这类 review 风格 skill 产生的是模拟反馈，不能冒充正式审稿意见。
- 某个 skill 的具体行为和边界，请直接阅读该目录下的 `SKILL.md` 及其配套 references。
