# my_codex_skills

[English](./README.md) | 中文

这是我个人维护的 Codex Skills 集合，用来沉淀可复用的科研工作流。

每个顶层 skill 文件夹都会保留自己的 README 文档，并在内部包含真正可安装的 `SKILL.md` 目录。

其中有两个 skill 是专门为 **Codex Desktop App 中使用的 MiniMax M3** 调过的：

- `minimax-task-preflight`：先读懂原始请求，必要时追问，再把请求改写成更清晰的 prompt，但不提前规划执行
- `minimax-thorough-execution`：在 prompt 已经清晰的前提下，强制更完整地执行，防止省 token 式缩任务、跳过图片核验、浅搜索和不贴链接

## Skills

| Skill | 中文简介 | 典型用途 | 可安装目录 |
| --- | --- | --- | --- |
| [`drawio-image2-pipeline`](./drawio-image2-pipeline/) | 面向科研图示的两阶段工作流；先生成可编辑的 draw.io 草稿，尽可能复用论文或海报中的现有图像素材，对导出的图做可视化质检，全部通过后再生成 GPT-Image-2 风格化参考图。 | 论文配图、海报、演示文稿视觉稿、概念图，尤其适合同时需要可编辑 draw.io 资产和高质量参考渲染图的场景。 | [`drawio-image2-pipeline/drawio-image2-pipeline`](./drawio-image2-pipeline/drawio-image2-pipeline/) |
| [`minimax-task-preflight`](./minimax-task-preflight/) | 面向 Codex Desktop App 中 MiniMax M3 的 prompt 澄清 skill。它先读取原始请求，只在必要时追问，再把请求改写成更清晰的 prompt，不滑向任务规划或交付设计。 | 在用 MiniMax M3 执行一个含糊、缺信息或容易歧义的任务前，先把 prompt 澄清到足够明确。 | [`minimax-task-preflight/minimax-task-preflight`](./minimax-task-preflight/minimax-task-preflight/) |
| [`minimax-thorough-execution`](./minimax-thorough-execution/) | 面向 Codex Desktop App 中 MiniMax M3 的彻底执行协议。它禁止为了省 token 悄悄缩 scope，要求截图/逐页任务基于渲染图做核验，要求搜索返回原始链接，并在最终答案里附一个简短的 completion audit。 | 当 prompt 已经清晰，但主要风险是偷懒、跳过正文或补充材料、少看图、少搜索、不贴链接时使用。 | [`minimax-thorough-execution/minimax-thorough-execution`](./minimax-thorough-execution/minimax-thorough-execution/) |
| [`mock-review`](./mock-review/) | 给论文作者使用的模拟审稿工具；按指定会议或期刊调研官方要求，检查稿件 PDF 材料风险，调研相关文献和实验对比，并生成用于准备 rebuttal、发现论文风险和改进论文的模拟审稿意见。 | 投稿前风险排查、rebuttal 准备、论文修改前的 reviewer-style critique。 | [`mock-review/mock-review`](./mock-review/mock-review/) |
| [`research-survey-loop`](./research-survey-loop/) | 长周期文献综述工作流；创建或继续综述任务，维护 `task.md`、`round_log.md`、`current_task.md` 和 `survey.md`，按来源优先级搜索论文，迁移本地 PDF，并逐轮扩展中文综述。 | 机器人、具身智能、计算机视觉、世界模型、导航、操作、3D 感知等方向的持续文献调研。 | [`research-survey-loop/research-survey-loop`](./research-survey-loop/research-survey-loop/) |

## 安装

把真正可安装的 skill 目录复制到 Codex skills 目录即可。

```powershell
# 安装 drawio-image2-pipeline
Copy-Item -Recurse -Force .\drawio-image2-pipeline\drawio-image2-pipeline "$env:USERPROFILE\.codex\skills\drawio-image2-pipeline"

# 安装 minimax-task-preflight
Copy-Item -Recurse -Force .\minimax-task-preflight\minimax-task-preflight "$env:USERPROFILE\.codex\skills\minimax-task-preflight"

# 安装 minimax-thorough-execution
Copy-Item -Recurse -Force .\minimax-thorough-execution\minimax-thorough-execution "$env:USERPROFILE\.codex\skills\minimax-thorough-execution"

# 安装 mock-review
Copy-Item -Recurse -Force .\mock-review\mock-review "$env:USERPROFILE\.codex\skills\mock-review"

# 安装 research-survey-loop
Copy-Item -Recurse -Force .\research-survey-loop\research-survey-loop "$env:USERPROFILE\.codex\skills\research-survey-loop"
```

如果你设置了 `CODEX_HOME`，也可以复制到 `$env:CODEX_HOME\skills\`。

## 说明

- 这些 skills 是个人科研工作流沉淀，不代表任何会议、期刊或机构的官方流程。
- `minimax-task-preflight` 和 `minimax-thorough-execution` 是为 **Codex Desktop App 中的 MiniMax M3** 定制的，目标是改善该模型在这个环境里的 prompt 理解和执行完整度，而不是作为所有模型的通用 prompt 技巧。
- `drawio-image2-pipeline` 适用于需要保留可编辑 draw.io 草稿的图示工作流；在调用 GPT-Image-2 前，必须先完成导出图的可视化质检。
- 使用 `mock-review` 生成的内容应明确标注为 simulated/mock review，不能替代真实同行评审，也不能冒充官方审稿意见。
- 文献下载和调研应优先使用官方开放页面、arXiv、OpenReview、作者主页等合法可访问来源。
- 每个 skill 的具体说明请阅读对应 skill 文件夹内的 README 文档。
