# minimax-image-understand（MiniMax 图像理解）

[English](./README.md) | 中文

通过上游 `minimax-coding-plan-mcp` 的 `understand_image` 工具做图像理解 （描述 / 分析 / OCR），使用用户自己的 MiniMax token-plan 密钥。绕过 Codex 0.137.0 损坏的 MCP 集成 （[openai/codex#23186](https://github.com/openai/codex/issues/23186)）。

支持本地 JPEG / PNG / WebP 文件路径以及 HTTP(S) URL。结果**只打印到 stdout**，不会写入任何本地结果、缓存或调试文件。

## 何时使用

当 Codex 自带的 MCP 集成不可用、且用户希望理解某一张具体的图片 （描述、分析、OCR）时，使用本 skill。常见英文触发词："describe this image"、"what's in this image"、"OCR this"、"read the text in this image"、"analyze this picture"、"caption this"。

**不要**用本 skill 去做：

- 网页搜索 → 改用专门的网页搜索 skill
- 搜索"某主题的图片" → 那是真正的网页搜索
- 编辑 / 转换图片 → 那是别的图片工具
