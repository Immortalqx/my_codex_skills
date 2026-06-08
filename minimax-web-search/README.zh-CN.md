# minimax-web-search（MiniMax 网页搜索）

[English](./README.md) | 中文

通过上游 `minimax-coding-plan-mcp` 的 `web_search` 工具做网页搜索， 使用用户自己的 MiniMax token-plan 密钥。绕过 Codex 0.137.0 损坏的 MCP 集成（[openai/codex#23186](https://github.com/openai/codex/issues/23186)）。

最多返回 15 条自然结果（标题、链接、摘要）以及相关搜索建议。结果**只 打印到 stdout**，不会写入任何本地结果、缓存或调试文件。

`SKILL.md` 与所有脚本都**仅使用英文**——这是有意为之，避免 Codex 在 读取该 skill 时把里面的中文渲染成乱码（控制台 / 终端编码差异引起）。

## 何时使用

当 Codex 自带的 MCP 集成不可用、且用户希望搜索网页（新闻、最新动态、 事实查询等）时，使用本 skill。常见英文触发词："search"、"find"、 "look up"、"google"、"latest news on"、"what's the latest"、 "any updates on"、"current status of"。

**不要**用本 skill 去做：

- 图像理解 → 改用专门的图像理解 skill
- 抓取 / 阅读某个具体 URL → 改用 `curl` / `wget`

## 双语搜索（推荐用于广覆盖查询）

对于范围广、信息更新快、或者用户希望得到权威覆盖的查询，skill 建议把 脚本**调用两次**，用同一种意图的两种语言版本，再合并结果：

1. **英文关键词** —— 查询翻译成英文
2. **中文关键词** —— 同一意图翻译成中文

然后按 URL 去重，同一 URL 优先保留排名更高的那条，再把合并后的集合 呈现给用户。对于范围窄的技术查询（具体 API、具体报错信息、某个库）， 单次调用通常就够了 —— `SKILL.md` 的 "Bilingual search" 段落里也 明确这么建议，并给出了一个完整例子。

## 可安装的 skill 目录

真正可安装的 skill（含 `SKILL.md`、`agents/`、`scripts/`）位于：

```
minimax-web-search/minimax-web-search/
```

请把 Codex skill 安装器指向这个嵌套子目录。本目录顶层的 `README.md` 和 `README.zh-CN.md` 只是仓库级说明，**不属于**可安装的 skill，因此 安装器不会把它们误当成 `SKILL.md`。

## 配置

脚本会按以下顺序自动寻找 MiniMax API 密钥：

1. 环境变量 `$MINIMAX_API_KEY`
2. `~/.codex/config.toml` 中的 `[model_providers.minimax].experimental_bearer_token`
3. `~/.codex/switch_model/minimax/config.toml` 中的 `[model_providers.minimax].experimental_bearer_token`

第三个位置是 Codex 在配置了 `switch_model` 后保存 token-plan 密钥的 地方 —— 它最可靠，因为 Codex 有时会剥离 `[mcp_servers.*]` 块。

你无需手动配置 —— 只要上面任何一处有合法密钥，本 skill 就能直接工作。

## 参考

- 完整 skill 说明：[`minimax-web-search/SKILL.md`](./minimax-web-search/SKILL.md)
- 上游 MCP 服务：[MiniMax-AI/MiniMax-Coding-Plan-MCP](https://github.com/MiniMax-AI/MiniMax-Coding-Plan-MCP)
- Codex MCP 相关 issue：[openai/codex#23186](https://github.com/openai/codex/issues/23186)
- 另请参考：图像理解 skill（如果一起安装了）
