# minimax_task_preflight

[English](./README.md) | 中文

`minimax_task_preflight` 是一个专门为 **Codex Desktop App 中的 MiniMax M3** 调过的 Codex skill 仓库。

它是执行前的一层窄 preflight。这个 skill 只负责读取原始用户请求，识别真正影响后续 prompt 的歧义，在必要时做简短追问，然后把请求改写成更清晰的 prompt。

## 重要边界

这个 skill **只用于 prompt 澄清**。

它不能：

- 直接开始做任务
- 设计交付物
- 提前做执行规划
- 自己决定任务 scope
- 优化 token 节省策略

它的目标是让 MiniMax M3 在执行前更准确地理解你的请求，而不是让它提前给自己规划后续执行路径。

## 快速开始

让 Codex 使用 `$minimax-task-preflight` 处理原始请求：

```text
Use $minimax-task-preflight to read my raw request, ask only the necessary clarification questions, and rewrite it into a clearer prompt without planning how to execute it.
```

示例：

```text
Use $minimax-task-preflight for this request:
"Read this paper carefully and explain it to me."
```

## 工作方式

1. Codex 先按字面读取请求。
2. Codex 只识别那些会实质影响后续 prompt 的歧义。
3. 如有必要，Codex 进行简短追问。
4. Codex 最终返回两种结果之一：
   - 一小段澄清问题
   - 一份改写后的 prompt

## 典型输出

当需要澄清时：

```text
Need clarification:
1. Which paper should I read?
2. Do you want a broad explanation, a section-by-section explanation, or a deep technical breakdown?
3. Should I include appendix and supplementary material if they exist?
```

当请求已经足够清晰时：

```text
Rewritten prompt:
Read the paper in paper.pdf and explain the method section in Chinese. If the appendix contains training details, evaluation settings, implementation details, or other information needed to understand the method, include those appendix details in the explanation.
```

## 推荐搭配

这个 skill 设计上就是给严格执行的 skill（看哪个安装了）打前站的。

推荐顺序：

1. 先运行 `$minimax-task-preflight`
2. 如果它提出追问，就先回答追问
3. 再把澄清后的 prompt 交给严格执行的 skill

## 仓库结构

- `README.md` 和 `README.zh-CN.md`：仓库说明
- `minimax-task-preflight/`：Codex 读取的 skill 文件目录
- `minimax-task-preflight/SKILL.md`：skill 定义
- `minimax-task-preflight/agents/`：skill 使用的 agent 配置
