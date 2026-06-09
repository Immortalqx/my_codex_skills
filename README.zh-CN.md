# my_codex_skills

[English](./README.md) | 中文

这是我个人维护的 Codex Skills 集合，用来沉淀可复用的科研工作流。

每个顶层 skill 文件夹都会保留自己的 README 文档，并在内部包含真正可安装的 `SKILL.md` 目录。

`mmx-cli` skill 保持为上游 MiniMax CLI skill 的原文副本，本仓库只在外层补充中英文说明文档。

## Skills

| Skill | 中文简介 | 典型用途 | 可安装目录 |
| --- | --- | --- | --- |
| [`arxiv`](./arxiv/) | 搜索 arXiv、按 arXiv ID 获取论文元数据，并通过内置 arXiv Atom API 辅助脚本把论文 PDF 下载到本地 paper library。 | 查找预印本、按查询词或 arXiv ID 下载 PDF，以及维护本地 `papers/` 或 `literature/` 论文集合。 | [`arxiv/arxiv`](./arxiv/arxiv/) |
| [`drawio-diagram`](./drawio-diagram/) | 面向科研图示的 draw.io 工作流；先生成可编辑的 draw.io 草稿，尽可能复用论文或海报中的现有图像素材，导出 PNG/SVG/PDF，再在 PNG 上跑视觉 QA 循环，直到 QA 清单全部通过。 | 论文配图、海报、演示文稿视觉稿、概念图，尤其适合需要一份可继续在 draw.io 里细化的可编辑草图的场景。 | [`drawio-diagram/drawio-diagram`](./drawio-diagram/drawio-diagram/) |
| [`help-me-read`](./help-me-read/) | 深读用户提供的 PDF，生成带页面截图、图表解释、背景补充和版本化输出文件的故事化精读笔记。 | 当用户需要 lecture slides 或论文的精读笔记、深入解析、tutor-style breakdown 时。 | [`help-me-read/help-me-read`](./help-me-read/help-me-read/) |
| [`mmx-cli`](./mmx-cli/) | 官方 MiniMax CLI skill，用本地 `mmx` 命令生成文本、图片、视频、语音和音乐，执行网页搜索和视觉理解，查询额度，管理文件，并导出命令 schema。内层 `SKILL.md` 保持为上游原文副本。 | 当 Codex 应该通过已配置好的本地 MiniMax CLI 工作时使用；低成本检查时尤其适合配合 `--dry-run`、`--quiet`、`--output json` 和 `--non-interactive`。 | [`mmx-cli/mmx-cli`](./mmx-cli/mmx-cli/) |
| [`mock-review`](./mock-review/) | 给论文作者使用的模拟审稿工具；按指定会议或期刊调研官方要求，检查稿件 PDF 材料风险，调研相关文献和实验对比，并生成用于准备 rebuttal、发现论文风险和改进论文的模拟审稿意见。 | 投稿前风险排查、rebuttal 准备、论文修改前的 reviewer-style critique。 | [`mock-review/mock-review`](./mock-review/mock-review/) |
| [`research-survey-loop`](./research-survey-loop/) | 长周期文献综述工作流；创建或继续综述任务，维护 `task.md`、`round_log.md`、`current_task.md` 和 `survey.md`，按来源优先级搜索论文，迁移本地 PDF，并逐轮扩展中文综述。 | 机器人、具身智能、计算机视觉、世界模型、导航、操作、3D 感知等方向的持续文献调研。 | [`research-survey-loop/research-survey-loop`](./research-survey-loop/research-survey-loop/) |
| [`update-source-map`](./update-source-map/) | 为任意项目目录创建或更新一份 agent 可读的 source map（Markdown + JSON）。自动检测是该新建还是刷新，并跨更新保留手写的 per-file 摘要。 | 处理新 / 不熟悉的 workspace；为多轮任务准备上下文；把项目交给另一个 agent 时。 | [`update-source-map/update-source-map`](./update-source-map/update-source-map/) |

## 安装

每个 skill 真正可安装的单元都是仓库里的内层 `<skill>/<skill>/` 目录。外层 `<skill>/README.md` 和 `<skill>/README.zh-CN.md` 只是仓库说明，不能安装进 Codex skills 目录。

让 Codex 安装即可。这个仓库只需要约束源目录和目标目录；具体复制命令由 Codex 根据 Windows / macOS / Linux 环境自行处理。

```text
Use $skill-installer to install the following skills from this repo into the local Codex skills directory.

For each <skill> below:
  - source: <this-repo>/<skill>/<skill>/
  - target:$CODEX_HOME/skills/<skill>/
  - copy the contents flat (not the outer folder)
  - skip any __pycache__ directory

Skills to install: arxiv, drawio-diagram, help-me-read, mmx-cli, mock-review, research-survey-loop, update-source-map.
```

如果只安装单个 skill，也沿用同样的目录规则并缩短 skill 列表。不要安装外层 `<skill>/` 目录，否则中英文 README 会被复制进已安装的 skill。

## 说明

- 这些 skills 是个人科研工作流沉淀，不代表任何会议、期刊或机构的官方流程。
- `mmx-cli` 需要本地已经配置好 `mmx` 命令；低成本 agent 检查建议使用 `--dry-run`、`--quiet`、`--output json` 和 `--non-interactive`。
- `drawio-diagram` 适用于需要保留可编辑 draw.io 草稿的图示工作流；它会产出 `.drawio` 草图与 PNG/SVG/PDF 导出，必须在视觉 QA 循环通过后才能宣布图完成。
- 使用 `mock-review` 生成的内容应明确标注为 simulated/mock review，不能替代真实同行评审，也不能冒充官方审稿意见。
- 文献下载和调研应优先使用官方开放页面、arXiv、OpenReview、作者主页等合法可访问来源。
- 每个 skill 的具体说明请阅读对应 skill 文件夹内的 README 文档。
