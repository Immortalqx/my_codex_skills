# mmx-cli

[English](./README.md) | 中文

`mmx-cli` 是来自 [MiniMax-AI/cli](https://github.com/MiniMax-AI/cli/tree/main/skill) 的官方 MiniMax CLI skill。可安装 skill 本体保持为上游 `SKILL.md` 的原文副本，让 Codex 可以通过本地 `mmx` 命令处理文本、图片、视频、语音、音乐、网页搜索、视觉理解、额度查询、文件管理和 schema 导出等流程。

当你希望 Codex 通过本地 MiniMax CLI 执行任务时使用这个 skill：

```text
Use $mmx-cli to run a MiniMax CLI dry run for an image generation request and show me the request JSON.
```

如果只是做低成本能力检查，要求 Codex 使用 `--dry-run`、`--quiet`、`--output json` 和 `--non-interactive`。

## 可安装目录

真正可安装的 Codex skill 是：

```text
mmx-cli/mmx-cli/
```

不要安装外层 `mmx-cli/` 文件夹。外层只放这个仓库的说明文档。

## 内容

- `mmx-cli/SKILL.md`：上游 MiniMax CLI skill 文档的原文副本。

## 前置条件

使用前需要先安装并配置 MiniMax CLI：

```bash
npm install -g mmx-cli
mmx auth status
```
