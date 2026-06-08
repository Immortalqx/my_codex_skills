# minimax-image-understand（MiniMax 图像理解）

[English](./README.md) | 中文

通过上游 `minimax-coding-plan-mcp` 的 `understand_image` 工具做图像理解 （描述 / 分析 / OCR），使用用户自己的 MiniMax token-plan 密钥。绕过 Codex 0.137.0 损坏的 MCP 集成 （[openai/codex#23186](https://github.com/openai/codex/issues/23186)）。

支持本地 JPEG / PNG / WebP 文件路径以及 HTTP(S) URL。结果**只打印到 stdout**，不会写入任何本地结果、缓存或调试文件。

`SKILL.md` 与所有脚本都**仅使用英文**——这是有意为之，避免 Codex 在 读取该 skill 时把里面的中文渲染成乱码（控制台 / 终端编码差异引起）。

## 何时使用

当 Codex 自带的 MCP 集成不可用、且用户希望理解某一张具体的图片 （描述、分析、OCR）时，使用本 skill。常见英文触发词："describe this image"、"what's in this image"、"OCR this"、"read the text in this image"、"analyze this picture"、"caption this"。

**不要**用本 skill 去做：

- 网页搜索 → 改用专门的网页搜索 skill
- 搜索"某主题的图片" → 那是真正的网页搜索
- 编辑 / 转换图片 → 那是别的图片工具

## 可安装的 skill 目录

真正可安装的 skill（含 `SKILL.md`、`agents/`、`scripts/`）位于：

```
minimax-image-understand/minimax-image-understand/
```

请把 Codex skill 安装器指向这个嵌套子目录。本目录顶层的 `README.md` 和 `README.zh-CN.md` 只是仓库级说明，**不属于**可安装的 skill，因此 安装器不会把它们误当成 `SKILL.md`。

## 配置

脚本会按以下顺序自动寻找 MiniMax API 密钥：

1. 环境变量 `$MINIMAX_API_KEY`
2. `~/.codex/config.toml` 中的 `[model_providers.minimax].experimental_bearer_token`
3. `~/.codex/switch_model/minimax/config.toml` 中的 `[model_providers.minimax].experimental_bearer_token`

你无需手动配置 —— 只要上面任何一处有合法密钥，本 skill 就能直接工作。

## 参考

- 完整 skill 说明：[`minimax-image-understand/SKILL.md`](./minimax-image-understand/SKILL.md)
- 上游 MCP 服务：[MiniMax-AI/MiniMax-Coding-Plan-MCP](https://github.com/MiniMax-AI/MiniMax-Coding-Plan-MCP)
- Codex MCP 相关 issue：[openai/codex#23186](https://github.com/openai/codex/issues/23186)
- 另请参考：网页搜索 skill（如果一起安装了）
