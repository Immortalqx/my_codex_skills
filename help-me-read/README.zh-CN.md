# help_me_read

[English](./README.md)

`help-me-read` 是一个 Codex skill：给一份用户提供的 PDF，**写出一份带故事的精读笔记**（中文或英文，由用户在 prompt 里指定）。

适用场景：用户拿着课件 PDF 或研究论文，想要一份**精读笔记**——

- 用一个贯穿的故事/比喻解释所有概念
- 每个 topic 按 **motivation → problem → solution → why → result** 组织
- 关键术语第一次出现时同时给中英文
- 插入 PDF 截图（课件整页、论文选区域）
- 所有来自 PDF 之外的事实都附原始链接
- 写成带版本号的新文件，**绝不覆盖旧笔记**

可安装的 skill 在 [help-me-read/](./help-me-read/)。

## 适用场景

用户说以下任何一种时使用：

- "close-read this PDF", "detailed study notes", "tutor-style breakdown"
- "精读这份 PDF", "深入解析", "讲清楚"
- "逐节给 motivation-problem-solution-why 解释"
- "写到新文件里，不要覆盖"

**不**适用：粗略摘要、按页转录、一句话问答。

## 快速开始

把 skill 复制到 `$CODEX_HOME/skills/`：

```bash
cp -R help-me-read "$CODEX_HOME/skills/"
```

然后让 Codex 用 `$help-me-read` 处理 PDF：

```text
Use $help-me-read on this PDF: lecture7.pdf
把精读笔记写到 <用户指定的输出目录>/<文档 slug>_精读版_中文_v<N>.md（文件名在运行时根据 PDF slug 和版本号决定）
Use Chinese for the note.
```

如果用户已经装了 web search / image understanding 类型的 skill，本 skill 会**优先调用**；如果没有，会回退到直接 HTTP 和 OCR，并在笔记里如实记录。

## 工作流程

1. 确认输入 PDF、写作语言、目标输出路径
2. 抽文本 + 抽整页 PNG（200+ DPI）。论文还要按需裁剪要插入的图
经典讲解（由 Codex 在写笔记时挑最相关的那一份，比如某个知名博客系列、公开课或教材章节）
4. 对**密集图**（架构图、plot family）调用 image understanding，解释存到 `notes/`
5. 设计**一个贯穿故事**，能一对一映射到文档每个主概念
6. 写精读笔记：每个 topic 一个 block，结尾有 Q&A
7. 验证：图片文件夹独立、每张图都能找到、每个链接可达、没覆盖任何旧笔记

## 输出布局

用户没指定路径时，skill 默认建：

```text
<workspace>/<临时工作根>/help-me-read/<文档 slug>/（临时工作根的名字沿用用户已有的命名习惯，skill 不硬编码）
  prompt.txt
  task_summary.md
  sources/
    user_files/        # 原始 PDF，不动
    fetched/           # 下载的网页 / arXiv 论文
  extracted_text/      # 逐页文本
  renders/pages/       # 整页 PNG
  screenshots/selected/  # 裁好的图
  search/queries/      # 实际跑过的搜索词
  search/results/      # 短笔记 + 原始链接
  notes/               # topic 草稿 + image understanding 输出
  final/
    <doc-slug>_<lang>_<version>.md
    <doc-slug>_<lang>_<version>_assets/  # 紧挨着笔记放，自包含
```

如果用户指定了文件夹（比如用户的输出目标目录），就在那个目录下建子文件夹，不再另开顶层 temp 根。

## 仓库结构

- `README.md` / `README.zh-CN.md`：仓库说明（**给人看**）
- `help-me-read/`：可安装的 Codex skill（**给 Codex 读**，全英文）
- `help-me-read/SKILL.md`：skill 定义和工作流
- `help-me-read/references/style-guide.md`：语气、术语翻译、章节规则
- `help-me-read/assets/template.md`：空白精读笔记骨架
- `help-me-read/agents/openai.yaml`：UI metadata

## 编码说明

**给 Codex 读的 skill 内部文件**（`SKILL.md`、`style-guide.md`、`template.md`、`agents/openai.yaml`、英文 `README.md`）一律全英文，避免编码歧义。

**给人读的 `README.zh-CN.md`** 和 **最终用户要求的精读笔记**（中文为主）才会有中文。这两个文件用 Python 以 UTF-8（无 BOM）写入。

**不要**用 Windows PowerShell 的 `Set-Content` 写中文到任何文件，它会**静默破坏**内容（GBK 误编码）。Python 的 `pathlib.Path.write_text(encoding='utf-8')` 是最稳的。