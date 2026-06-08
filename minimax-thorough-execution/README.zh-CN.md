# minimax_thorough_execution

[English](./README.md) | 中文

`minimax_thorough_execution` 是一个专门为 **Codex Desktop App 中的 MiniMax M3** 调过的 Codex skill 仓库。

它是一个**严格按用户 prompt 干活**的执行层。这个 skill 的目标是压制 MiniMax 常见的失败模式，比如擅自改写任务、为了省 token 悄悄缩小任务范围、只读 abstract 和 introduction、跳过 appendix 或 supplementary material、不认真做视觉核验、浅搜索，以及搜完不给原始链接。

真正可安装的 skill 位于 [minimax-thorough-execution/](./minimax-thorough-execution/)。

## 重要边界

这个 skill 不负责澄清、评价、优化或改写 prompt。

如果你想先单独做一轮澄清，可以先用 prompt 澄清类的 skill，但这个 skill 自己仍然必须按 prompt 原样执行，不能再次改写。

## 它强制的内容

- 严格服从用户 prompt
- 执行阶段不允许改写、优化或悄悄重解释 prompt
- 不允许为了省 token 悄悄缩 scope
- 除非用户明确要求更便宜、更短或部分执行，否则默认优先完成度
- 优先依赖本地落盘的任务工件，而不是脆弱的长对话记忆
- temp 工件必须按类型放入任务子目录，不能堆在任务根目录
- 模型应该搜索当前环境中的可用 skill，并在有帮助时调用零个、一个或多个合适 skill
- 维护 source map 和 evidence map，而不是只留下零散缓存文件
- 读论文时必须读正文，不能只看 abstract/introduction
- 存在且相关时，必须检查 appendix 和 supplementary material
- 截图和逐页任务必须基于渲染后的页面做视觉核验，不能只靠 caption 猜测或只看 OCR/抽取文本
- 需要搜索支撑的回答必须返回原始链接
- 搜索得到的结论必须绑定来源
- 最终答案必须附一个简短的 `Completion audit`

## 本地 Temp 缓存

这个 skill 现在默认认为：只靠聊天上下文不够稳，多轮任务应该尽量依赖本地落盘工件续跑。

在开始实质执行前，它应该：

1. 先在工作区里查找已有的 temp 类目录，例如 `x_temp_codex`、`x_temp`、`temp_codex`、`temp`、`tmp`、`codex_temp`、`.temp`
2. 如果没有合适目录，就按本地命名风格创建新的 temp 根目录；如果工作区明显在用 `x_*` 工具目录，则优先创建 `x_temp_codex/`，否则创建 `temp_codex/`
3. 在该 temp 根目录下按任务创建或复用子目录
4. 读取已有的工作区级或任务级 source map
5. 把用户原始 prompt 和可复用的中间工件保存进去

典型工件包括：

- `prompt.txt`
- `task_summary.md`
- `local_source_map.md` / `local_source_map.json`
- `evidence_map.md`
- 下载的论文和源文件
- 抽取文本或 scan 输出
- PDF 或幻灯片的渲染图片
- 截图结果
- 搜索笔记和原始链接
- 中间 JSON 或 Markdown 笔记
- 审计记录

强制目录结构：

```text
<temp-root>/<task-subdir>/
  prompt.txt
  prompt_history.md
  task_summary.md
  manifest.json
  local_source_map.md
  local_source_map.json
  evidence_map.md
  completion_audit.md
  sources/
    user_files/
    fetched/
  extracted_text/
    page_text/
    ocr/
  renders/
    pages/
    verification/
  screenshots/
    selected/
  search/
    queries/
    results/
  notes/
  scripts/
  logs/
  audit/
```

只有 prompt、summary、manifest、source map、evidence map 和 audit 文件应该直接放在任务子目录根部。PDF、网页、图片、抽取文本、临时脚本、日志和中间笔记应该进入类型化子目录，或本地已有约定中最接近的等价目录。

如果已有任务目录已经很乱，这个 skill 应该停止继续往根目录扔零散文件。新工件应该放进类型化子目录，已有散落文件应该记录进 source map 或 manifest。除非用户要求，不要移动已有文件。

如果工作区里已经有更强的本地约定，这个 skill 应该直接复用。例如在你的工作区里，常见做法是先读取工作区级的 `x_codex/source_map.json`，再在当前 `x_temp_codex/`、`x_temp/` 或类似 temp task 子目录里维护 `local_source_map` 或 `evidence_map`。

后续追问时，MiniMax M3 应该优先查找这个已有的任务子目录，读取保存下来的 prompt history、task summary、manifest、source maps、evidence maps、rendered pages、下载文件、抽取文本、screenshots、notes 和 audit artifacts，再从这些本地工件继续，而不是只依赖已经压缩或漂移的对话上下文。

当答案依赖视觉内容时，MiniMax M3 应该重新打开相关渲染页面或图片，再做新的判断或选择截图。

## Skill 搜索与调用

在使用通用 shell 命令、直接下载、临时脚本或手动搜索之前，MiniMax M3 应该先搜索当前环境中的可用 skill、plugin 或专用工作流。

规则：

- 只有在没有相关 skill 时，才直接走通用 fallback
- 如果只有一个明显相关的 skill，就调用它
- 如果任务适合组合能力，就调用多个相关 skill
- 不要默认任务只能调用一个 skill
- 不要在检查本地 skill 环境之前就预设通用工作流
- 不要因为 `wget`、`curl` 或手动搜索更短，就跳过 skill 搜索

这只是执行路由规则，不授权改写 prompt 或重新解释任务。

## Source Map

这个 skill 现在把 `source map` 维护视为执行协议的一部分。

也就是说，MiniMax M3 应该：

- 先查找已有的工作区级 source-tracking 文件，例如 `x_codex/source_map.json`、`manifest.json`、`file_inventory.jsonl`
- 再查找任务级 map，例如 `local_source_map*.md`、`source_map*.json`、`evidence_map*.md`
- 当引入新的 PDF、网页、截图、抽取文本或派生笔记时，持续更新这些 map

一个合格的 source map 至少应记录：

- 本地路径
- 原始 URL 或来源描述
- source 类型
- 在当前任务中的角色，例如 primary evidence、supplementary evidence、candidate source、cache only
- 阅读状态
- 该文件是原始证据还是派生工件

source map 只是组织和续跑工具，本身不能替代最终证据。

## 快速开始

把可安装的 skill 复制到 `$CODEX_HOME/skills/`：

```bash
cp -R minimax-thorough-execution "$CODEX_HOME/skills/"
```

然后让 Codex 对用户给出的 prompt 使用 `$minimax-thorough-execution`：

```text
Use $minimax-thorough-execution to execute my prompt exactly as written, without rewriting it, silently shrinking scope, skipping appendix or supplement, guessing from text instead of inspecting images, or omitting source links.
```

## 典型用法

示例：

```text
Use $minimax-thorough-execution on this prompt:
"Read paper.pdf carefully, including any appendix or supplementary PDF in the workspace. Explain the method and experiments in Chinese, and if you cite any current external facts, search for them and return the original links."
```

## Completion Audit

这个 skill 要求最终答案附带一个简短的审计块：

```text
Completion audit:
- Prompt obedience: checked | blocked
- Scope: checked | narrowed | blocked
- Skill search and delegation: checked | not applicable | blocked
- Temp artifact layout: checked | blocked
- Source map: checked | not applicable | blocked
- Local artifact re-read: checked | not applicable | blocked
- Body/appendix/supplement: checked | not applicable | blocked
- Visual verification: checked | not applicable | blocked
- Search and links: checked | not applicable | blocked
```

这个审计块故意做得很短。目的不是增加格式负担，而是强迫 MiniMax M3 把关键检查是否真的完成暴露出来，而不是悄悄默认自己已经做了。

如果合适，最终答案里也可以顺手提一句本地工件目录，方便下一轮继续。

## 推荐搭配

推荐顺序：

1. 先运行 prompt 澄清类 skill（如果安装了）
2. 如果它提出追问，就先回答追问
3. 再把得到的 prompt 原样交给 `$minimax-thorough-execution`

## 仓库结构

- `README.md` 和 `README.zh-CN.md`：仓库说明
- `minimax-thorough-execution/`：真正用于安装的 Codex skill
- `minimax-thorough-execution/SKILL.md`：skill 定义
- `minimax-thorough-execution/agents/`：skill 使用的 agent 配置
