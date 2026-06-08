# my_codex_skills

[English](./README.md) | 中文

这是我个人维护的 Codex Skills 集合，用来沉淀可复用的科研工作流。

每个顶层 skill 文件夹都会保留自己的 README 文档，并在内部包含真正可安装的 `SKILL.md` 目录。

本仓库里有几个 skill 是专门为 **Codex Desktop App 中使用的 MiniMax M3** 调过的：

- `minimax-task-preflight`：先读懂原始请求，必要时追问，再把请求改写成更清晰的 prompt，但不提前规划执行
- `minimax-thorough-execution`：严格执行用户 prompt，防止执行时擅自改写任务、省 token 式缩任务、跳过图片核验、浅搜索和不贴链接
- `minimax-web-search`：通过上游 `minimax-coding-plan-mcp` 的 `web_search` 工具调用网络搜索，token 来自用户自己的 MiniMax token plan key — 绕过 Codex 0.137.0 损坏的 MCP 集成（[openai/codex#23186](https://github.com/openai/codex/issues/23186)）
- `minimax-image-understand`：通过上游 `minimax-coding-plan-mcp` 的 `understand_image` 工具做图像理解（描述 / 分析 / OCR），同样用 token plan key — 同样的 MCP 绕过方案

`minimax-web-search` 和 `minimax-image-understand` 是**兄弟 skill**：完全独立（各自带自己的 `lib_key.py` + `mcp_client.py`），可以单独装/卸。它们都通过 JSON-RPC 调官方上游 MCP server，**结果与上游工具输出完全一致** — 中间没有 API 翻译层。

这两个 MiniMax MCP wrapper 的任务结果都是 **stdout-only**：不会把搜索结果、图片理解结果、日志、调试 JSON 或业务缓存文件写入本地磁盘。即使使用 `--print`，完整 JSON-RPC 响应也是打印到 stdout 供 Codex 读取，而不是保存到本地文件。Python 解释器可能产生 `__pycache__`，`uvx` / `uv` 也可能使用自己的依赖缓存；这些属于工具链正常运行时副作用，不是 skill 生成的结果文件。

## Skills

| Skill | 中文简介 | 典型用途 | 可安装目录 |
| --- | --- | --- | --- |
| [`drawio-diagram`](./drawio-diagram/) | 面向科研图示的 draw.io 工作流；先生成可编辑的 draw.io 草稿，尽可能复用论文或海报中的现有图像素材，导出 PNG/SVG/PDF，再在 PNG 上跑视觉 QA 循环，直到 QA 清单全部通过。 | 论文配图、海报、演示文稿视觉稿、概念图，尤其适合需要一份可继续在 draw.io 里细化的可编辑草图的场景。 | [`drawio-diagram/drawio-diagram`](./drawio-diagram/drawio-diagram/) |
| [`help-me-read`](./help-me-read/) | 深读用户提供的 PDF，生成带页面截图、图表解释、背景补充和版本化输出文件的故事化精读笔记。 | 当用户需要 lecture slides 或论文的精读笔记、深入解析、tutor-style breakdown 时。 | [`help-me-read/help-me-read`](./help-me-read/help-me-read/) |
| [`minimax-image-understand`](./minimax-image-understand/) | 通过上游 `minimax-coding-plan-mcp` 的 `understand_image` 工具做图像理解。自动从 `~/.codex/switch_model/minimax/config.toml`（或 `~/.codex/config.toml` 的 `[model_providers.minimax].experimental_bearer_token`）读 MiniMax token plan key。支持本地 JPEG/PNG/WebP 路径和 HTTP(S) URL。结果只打印到 stdout，不写本地结果/调试文件。 | 当 Codex 自带的 MCP 集成坏了（#23186）而用户想理解一张图（描述 / 分析 / OCR）时。 | [`minimax-image-understand/minimax-image-understand`](./minimax-image-understand/minimax-image-understand/) |
| [`minimax-task-preflight`](./minimax-task-preflight/) | 面向 Codex Desktop App 中 MiniMax M3 的 prompt 澄清 skill。它先读取原始请求，只在必要时追问，再把请求改写成更清晰的 prompt，不滑向任务规划或交付设计。 | 在用 MiniMax M3 执行一个含糊、缺信息或容易歧义的任务前，先把 prompt 澄清到足够明确。 | [`minimax-task-preflight/minimax-task-preflight`](./minimax-task-preflight/minimax-task-preflight/) |
| [`minimax-thorough-execution`](./minimax-thorough-execution/) | 面向 Codex Desktop App 中 MiniMax M3 的严格执行协议。它禁止执行时改写 prompt，禁止为了省 token 悄悄缩 scope，要求截图/逐页任务基于渲染图做核验，要求搜索返回原始链接，维护 source map，并在最终答案里附一个简短的 completion audit。 | 当主要风险是乱改 prompt、偷懒、跳过正文或补充材料、少看图、少搜索、不贴链接时使用。 | [`minimax-thorough-execution/minimax-thorough-execution`](./minimax-thorough-execution/minimax-thorough-execution/) |
| [`minimax-web-search`](./minimax-web-search/) | 通过上游 `minimax-coding-plan-mcp` 的 `web_search` 工具做网络搜索。Key 解析方式与 `minimax-image-understand` 一致。返回最多 15 条 organic 结果（标题、链接、摘要）外加相关搜索建议。结果只打印到 stdout，不写本地结果/调试文件。 | 当 Codex 自带的 MCP 集成坏了（#23186）而用户想搜网（新闻、查最新动态、查事实等）时。 | [`minimax-web-search/minimax-web-search`](./minimax-web-search/minimax-web-search/) |
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

Skills to install: drawio-diagram, help-me-read, minimax-image-understand, minimax-task-preflight, minimax-thorough-execution, minimax-web-search, mock-review, research-survey-loop, update-source-map.
```

如果只安装单个 skill，也沿用同样的目录规则并缩短 skill 列表。不要安装外层 `<skill>/` 目录，否则中英文 README 会被复制进已安装的 skill。

### 两个 MiniMax MCP skill 的前置依赖

`minimax-web-search` 和 `minimax-image-understand` 都会 spawn `uvx minimax-coding-plan-mcp` 来跟上游 server 通信。`uvx`、MCP 和 key 的安装配置请参考 MiniMax Token Plan MCP guide：

<https://platform.minimax.io/docs/token-plan/mcp-guide>

两个 skill 自动从以下任一位置发现你的 MiniMax token plan key：
- `$MINIMAX_API_KEY` 环境变量
- `~/.codex/config.toml` 里的 `[model_providers.minimax].experimental_bearer_token`
- `~/.codex/switch_model/minimax/config.toml` 里的 `[model_providers.minimax].experimental_bearer_token`

只要其中任一位置已经有 key，就不需要额外配置。

运行时说明：两个 MiniMax wrapper 脚本本身不会持久化搜索或图像理解输出，只会打印到 stdout。CPython 运行脚本时仍可能创建 `__pycache__` 字节码文件，`uvx` / `uv` 也可能使用自己的依赖缓存目录。这些是解释器和包管理器的正常行为，不是这些 skill 生成的结果文件。

## 说明

- 这些 skills 是个人科研工作流沉淀，不代表任何会议、期刊或机构的官方流程。
- `minimax-task-preflight`、`minimax-thorough-execution`、`minimax-web-search` 和 `minimax-image-understand` 是为 **Codex Desktop App 中的 MiniMax M3** 定制的。前两个改善 prompt 理解和执行完整度；后两个提供 Codex 0.137.0 因 namespace-tools bug（openai/codex#23186）而无法通过自带 MCP 集成交付的网络搜索和图像理解能力。
- `minimax-web-search` 和 `minimax-image-understand` 调的是**上游** `minimax-coding-plan-mcp` server（JSON-RPC），结果与官方工具输出**完全一致** — 中间没有翻译层。
- `drawio-diagram` 适用于需要保留可编辑 draw.io 草稿的图示工作流；它会产出 `.drawio` 草图与 PNG/SVG/PDF 导出，必须在视觉 QA 循环通过后才能宣布图完成。
- 使用 `mock-review` 生成的内容应明确标注为 simulated/mock review，不能替代真实同行评审，也不能冒充官方审稿意见。
- 文献下载和调研应优先使用官方开放页面、arXiv、OpenReview、作者主页等合法可访问来源。
- 每个 skill 的具体说明请阅读对应 skill 文件夹内的 README 文档。
