# arxiv

[English](./README.md) | 中文

`arxiv` 是一个用于搜索 arXiv、按 arXiv ID 获取论文元数据、并把论文 PDF 下载到本地 paper library 的 Codex skill。

当你希望 Codex 查找预印本、根据 arXiv ID 获取 PDF，或者把相关 arXiv 论文保存到 `papers/` 或指定目录时，可以使用 `$arxiv`：

```text
Use $arxiv to search for recent papers about test-time scaling and download the top relevant PDF into papers/.
```

如果已经知道论文 ID，也可以这样说：

```text
Use $arxiv to fetch 2301.07041 and download the PDF into literature/.
```

## 工作流程

1. Codex 解析查询词、arXiv ID、结果数量、输出目录和下载模式。
2. Codex 运行可安装 skill 内置的 `arxiv/scripts/arxiv_fetch.py` 辅助脚本。
3. 搜索结果会以结构化元数据返回，包括 arXiv ID、标题、作者、摘要、日期、分类、PDF 链接和 abstract 链接。
4. 如果用户要求下载，PDF 默认保存到 `papers/`，也可以保存到用户指定目录。
5. 如果目标 PDF 已存在，skill 会跳过而不是覆盖；如果下载到的文件过小，会按错误页面处理。

## 输出

- 在对话中打印搜索结果。
- 可选地把下载的 PDF 保存到 `papers/` 或用户指定目录。

这个 skill 不会把搜索日志、调试 JSON 或缓存文件作为任务结果持久化。

## 辅助脚本

- [arxiv/scripts/arxiv_fetch.py](./arxiv/scripts/arxiv_fetch.py)：用于 arXiv Atom API 搜索和 PDF 下载的小型 CLI。

在可安装 skill 目录内可以直接这样运行：

```bash
python scripts/arxiv_fetch.py search "diffusion policy" --max 10
python scripts/arxiv_fetch.py search "id:2301.07041" --max 1
python scripts/arxiv_fetch.py download 2301.07041 --dir papers
```

## 仓库结构

- `README.md` 和 `README.zh-CN.md`：仓库说明文档。
- `arxiv/`：可安装的 Codex skill 目录。
- `arxiv/SKILL.md`：Codex skill 定义。
- `arxiv/scripts/`：确定性的辅助脚本。
- `arxiv/agents/`：skill 使用的 UI 元数据。
