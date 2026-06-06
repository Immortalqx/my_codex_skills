# update_source_map

[English](./README.md) | 中文

`update_source_map` 是一个 Codex skill，用于为任意项目目录**创建或更新**一份 agent 可读的 source map。

Source map 是一份对项目文件（`.md` 笔记 + `.pdf` 文档）的结构化索引，包含每个文件的 1 行摘要、文件大小、修改时间，以及每个 markdown 文件的标题骨架。它让 AI agent（或人）能快速回答"这个项目里有什么？X 在哪里？"而无需逐个读取文件。

Skill 会自动检测 workspace 中是否已经存在 source map：
- **Create** 模式：从零生成 `SOURCE_MAP.md` + `source_map.json`
- **Update** 模式：重新扫描 workspace，保留手写的 per-file 摘要，并显示与上次扫描的 diff

可安装的 skill 在 [update-source-map/](./update-source-map/)。

## 何时使用

- 开始处理一个新的 / 不熟悉的 workspace 时
- 文件被增删改，原索引已过期时
- 为多轮任务准备上下文（任务会触碰很多文件）时
- 把项目交给另一个 agent、需要给 ta 提供导航时

## 它会产出什么

在 `<workspace>/x_temp/`（或你指定的输出目录）下生成 3 个文件：

| 文件 | 格式 | 用途 |
|---|---|---|
| `SOURCE_MAP.md` | Markdown | 主交付物 — 人 + agent 都能读 |
| `source_map.json` | JSON | 结构化数据 — 程序化查询用 |
| `curated_summaries.json` | JSON | 手写的 per-file 摘要（跨更新保留） |

## 快速开始

把可安装的 skill 复制到 `$CODEX_HOME/skills/`：

```bash
cp -R update-source-map "$CODEX_HOME/skills/"
```

然后让 Codex 使用 `$update-source-map`：

```text
Use $update-source-map to create or update the source map for this project.
```

或直接运行脚本：

```bash
python3 update-source-map/scripts/regenerate.py /path/to/workspace
```

## 重要边界

这个 skill 用于**导航和清单**，不是用于：
- 读取或总结文件内容（用其他 skill）
- 重构或编辑文件
- 跑实验

Source map 告诉 agent 项目里有什么、在哪里找。它不替代原始文件。

## 来源

这个 skill 的模式来自一次实际的 source map 运行（一个 43 文件 / 66MB 的个人知识库）。完整工作流见 [SKILL.md](./update-source-map/SKILL.md)，格式规范见 [references/](./update-source-map/references/)，可执行代码见 [scripts/](./update-source-map/scripts/)。
