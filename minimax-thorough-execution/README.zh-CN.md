# minimax_thorough_execution

[English](./README.md) | 中文

`minimax_thorough_execution` 是一个专门为 **Codex Desktop App 中的 MiniMax M3** 调过的 Codex skill 仓库。

它是 prompt 已经清晰之后使用的执行层。这个 skill 的目标是压制 MiniMax 常见的捷径行为，比如为了省 token 悄悄缩小任务范围、只读 abstract 和 introduction、跳过 appendix 或 supplementary material、不认真做视觉核验、浅搜索，以及搜完不给原始链接。

真正可安装的 skill 位于 [minimax-thorough-execution/](./minimax-thorough-execution/)。

## 重要边界

这个 skill 默认 prompt 已经是清晰的。

它负责强化执行纪律，不负责做 prompt 澄清。正常工作流里，如果请求本身还有歧义，应该先用 [`minimax-task-preflight`](../minimax-task-preflight/)。

## 它强制的内容

- 不允许为了省 token 悄悄缩 scope
- 除非用户明确要求更便宜、更短或部分执行，否则默认优先完成度
- 读论文时必须读正文，不能只看 abstract/introduction
- 存在且相关时，必须检查 appendix 和 supplementary material
- 截图和逐页任务必须基于渲染后的页面做视觉核验，不能只靠 caption 猜测或只看 OCR/抽取文本
- 需要搜索支撑的回答必须返回原始链接
- 搜索得到的结论必须绑定来源
- 最终答案必须附一个简短的 `Completion audit`

## 快速开始

把可安装的 skill 复制到 `$CODEX_HOME/skills/`：

```bash
cp -R minimax-thorough-execution "$CODEX_HOME/skills/"
```

然后让 Codex 对一条已经清晰的 prompt 使用 `$minimax-thorough-execution`：

```text
Use $minimax-thorough-execution to execute this already-clear prompt thoroughly, without silently shrinking scope, skipping appendix or supplement, guessing from text instead of inspecting images, or omitting source links.
```

## 典型用法

示例：

```text
Use $minimax-thorough-execution on this clarified prompt:
"Read paper.pdf carefully, including any appendix or supplementary PDF in the workspace. Explain the method and experiments in Chinese, and if you cite any current external facts, search for them and return the original links."
```

## Completion Audit

这个 skill 要求最终答案附带一个简短的审计块：

```text
Completion audit:
- Scope: checked | narrowed | blocked
- Body/appendix/supplement: checked | not applicable | blocked
- Visual verification: checked | not applicable | blocked
- Search and links: checked | not applicable | blocked
```

这个审计块故意做得很短。目的不是增加格式负担，而是强迫 MiniMax M3 把关键检查是否真的完成暴露出来，而不是悄悄默认自己已经做了。

## 推荐搭配

推荐顺序：

1. 先运行 [`$minimax-task-preflight`](../minimax-task-preflight/)
2. 如果它提出追问，就先回答追问
3. 再对澄清后的 prompt 使用 `$minimax-thorough-execution`

## 仓库结构

- `README.md` 和 `README.zh-CN.md`：仓库说明
- `minimax-thorough-execution/`：真正用于安装的 Codex skill
- `minimax-thorough-execution/SKILL.md`：skill 定义
- `minimax-thorough-execution/agents/`：skill 使用的 agent 配置
