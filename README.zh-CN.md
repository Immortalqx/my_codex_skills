# my_codex_skills

[English](./README.md) | 中文

这是我个人维护的 Codex skills 集合，用于沉淀可复用的科研、写作和项目理解工作流。

每个 skill 都是一个顶层目录。合法的 skill 目录会在根部包含 `SKILL.md`，并且可以按需包含
`agents/`、`scripts/`、`references/` 或 `assets/`。本仓库不再使用嵌套的可安装目录，也不再保留每个 skill 自己的 README。

除非某个 skill 明确说明，否则这些 skills 默认面向独立、单 agent 使用：可以使用 skill 自带脚本、本地文件和公共网页来源；通知钩子、reviewer agent 链路或隐藏的跨 skill 钩子都不是默认路径。

## Skills

| Skill | 简介 | 典型用途 |
| --- | --- | --- |
| [`alphaxiv`](./alphaxiv/) | 使用公开 AlphaXiv Markdown 快速查询单篇 arXiv 论文，必要时降级读取完整 AlphaXiv Markdown 或 arXiv LaTeX 源码。 | 根据 arXiv ID 或 URL 快速解释单篇论文，而不是做大范围文献综述。 |
| [`arxiv`](./arxiv/) | 搜索 arXiv、按 arXiv ID 获取论文元数据，并通过内置 arXiv Atom API 辅助脚本把 PDF 下载到本地论文库。 | 查找预印本、按查询词或 arXiv ID 下载 PDF，以及维护本地 `papers/` 或 `literature/` 论文集合。 |
| [`drawio-diagram`](./drawio-diagram/) | 面向科研图示的 draw.io 工作流：生成可编辑 `.drawio` 草稿，导出 PNG/SVG/PDF，并在 PNG 上执行视觉 QA。 | 论文配图、海报、演示文稿视觉稿、概念图，尤其适合需要保留可编辑 draw.io 文件的场景。 |
| [`figure-description`](./figure-description/) | 专利附图处理工作流：识别图中部件、分配附图标记，并生成正式附图说明。 | 根据本地技术图准备 CN/US/EP 专利附图说明和附图标记索引。 |
| [`formula-derivation`](./formula-derivation/) | 研究公式推导工作流：澄清假设，并区分恒等式、命题、近似和解释。 | 把杂乱理论笔记整理成内部推导笔记、论文风格理论草稿或 blocker report。 |
| [`grant-proposal`](./grant-proposal/) | 从研究 idea 和文献材料撰写结构化基金申请书，支持机构特定格式和通用格式。 | 把研究方向转成包含研究目标、里程碑、可行性和预期成果的 funding application。 |
| [`help-me-read`](./help-me-read/) | 深读用户提供的 PDF，生成带页面截图、图表解释和背景补充的故事化精读笔记。 | 生成 lecture slides 或论文的精读笔记、深入解析和 tutor-style breakdown。 |
| [`mmx-cli`](./mmx-cli/) | MiniMax CLI skill，用本地 `mmx` 命令执行文本、搜索、视觉、额度、文件和多媒体任务。 | 当 Codex 需要直接调用已配置好的本地 MiniMax CLI 时使用，尤其适合中英文混合多次搜索，以及 `--quiet`、`--output json`、`--non-interactive` 的非交互式工作流。 |
| [`mock-review`](./mock-review/) | 给论文作者使用的模拟审稿工作流：调研 venue 要求、检查稿件 PDF、研究相关工作并生成模拟审稿意见。 | 投稿前风险排查、rebuttal 准备、论文修改前的 reviewer-style critique。 |
| [`novelty-check`](./novelty-check/) | 研究 idea 查新工具：抽取核心 claim，检索文献，对比 closest prior work，并报告 novelty 风险。 | 在投入实现时间前检查一个方法是否看起来已经被做过。 |
| [`proof-writer`](./proof-writer/) | 面向 theorem、lemma、proposition、corollary 等命题的严谨证明写作工作流。 | 把粗糙命题或证明草稿整理成可辩护的证明包。 |
| [`research-lit`](./research-lit/) | 独立文献调研工作流：结合本地 PDF、公共网页检索和结构化 arXiv 元数据进行相关工作检索、比较和综合。 | 围绕某个研究主题查找相关工作、梳理论文版图并比较不同方法簇。 |
| [`research-survey-loop`](./research-survey-loop/) | 长周期文献综述工作流：维护稳定任务文档、按来源优先级搜索论文、分块阅读论文，并逐轮扩展中文综述。 | 机器人、具身智能、计算机视觉、世界模型、导航、操作、3D 感知等方向的持续文献调研。 |
| [`research-wiki`](./research-wiki/) | 持久化项目级科研知识库，用于沉淀论文、想法、实验、主张以及它们之间的有类型关系。 | 把项目研究记忆固定下来，避免每个 session 都重新搭一遍同一张领域地图。 |
| [`update-source-map`](./update-source-map/) | 为任意项目目录创建或更新 agent 可读的 source map，并在刷新时保留手写的 per-file 摘要。 | 处理新的或不熟悉的 workspace、刷新过期索引，或把项目交给另一个 agent。 |

## 安装

安装单元就是每个顶层 skill 目录本身：

```text
source: <this-repo>/<skill>/
target: $CODEX_HOME/skills/<skill>/
copy the directory contents as-is
skip any __pycache__ directory
```

如果要安装本仓库的全部 skills，请把以下目录复制到本地 Codex skills 目录：

```text
alphaxiv, arxiv, drawio-diagram, figure-description, formula-derivation,
grant-proposal, help-me-read, mmx-cli, mock-review, novelty-check,
proof-writer, research-lit, research-survey-loop, research-wiki,
update-source-map
```

不要把 `scripts/` 这样的仓库工具目录安装进 `$CODEX_HOME/skills`。

安装或更新本地 skills 后，需要重启 Codex，新的 skill metadata 才会被加载。

## 说明

- 这些 skills 是个人科研工作流沉淀，不代表任何会议、期刊或机构的官方流程。
- `mmx-cli` 需要本地已经配置好 `mmx` 命令。
- `drawio-diagram` 面向需要保留可编辑 draw.io 草稿的图示工作流；只有视觉 QA 循环通过后才应宣布图已完成。
- 使用 `mock-review` 生成的内容应明确标注为 simulated/mock review，不能冒充官方审稿意见。
- 文献下载和调研应优先使用官方开放页面、arXiv、OpenReview、作者主页等合法可访问来源。
