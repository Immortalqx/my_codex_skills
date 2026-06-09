# drawio_diagram

[English](./README.md) | 中文

`drawio_diagram` 是一个独立的 Codex skill 仓库，面向科研图示工作流。核心交付物是可编辑的 `draw.io` / `diagrams.net` 草稿，以及通过严格视觉 QA 的 PNG/SVG/PDF 导出；草图本身就要足够好，用户可以直接在 draw.io 里继续编辑并作为最终配图使用。

让 Codex 对论文、海报或概念图任务使用 `$drawio-diagram`：

```text
Use $drawio-diagram to create a research figure from the current workspace.
Read the available paper assets first, reuse useful figures or plots, create an editable draw.io draft under image_draft/,
export PNG/SVG/PDF, and run visual QA on the PNG. Iterate on the .drawio until the QA loop passes.
Style target: clean technical poster figure.
```

如果你已经有一个 `.drawio` 文件，希望在原图基础上继续细化，也可以这样说：

```text
Use $drawio-diagram on this existing .drawio file.
Keep the structure editable, tighten the layout, re-export, and re-run the QA loop.
```

## 工作流程

1. Codex 先读取本地论文、海报、幻灯片、笔记或实验材料，并检查可复用的视觉素材。
2. Codex 创建或继续完善可编辑的 `sketch.drawio` 草稿。
3. Codex 导出 PNG/SVG/PDF，供用户检查和继续编辑。
4. Codex 在 PNG 上跑视觉 QA 循环，修复 `.drawio` 并重新导出，直到 QA 清单全部通过。

## 输出

默认输出目录为 `image_draft/`，通常会包含：

- `assets/`
- `asset_manifest.md`
- `sketch.drawio`
- `sketch.png`
- `sketch.svg`
- `sketch.pdf`
- `qa_notes.md`

## 辅助脚本

- [drawio-diagram/scripts/inventory_assets.py](./drawio-diagram/scripts/inventory_assets.py)：盘点本地可复用素材
- [drawio-diagram/scripts/render_pdf_pages.py](./drawio-diagram/scripts/render_pdf_pages.py)：把 PDF 页面渲染成可复用图片资产
- [drawio-diagram/scripts/export_drawio.ps1](./drawio-diagram/scripts/export_drawio.ps1)：从 `.drawio` 导出 PNG/SVG/PDF

## 仓库结构

- `README.md` 和 `README.zh-CN.md`：仓库说明文档
- `drawio-diagram/`：Codex 读取的 skill 文件目录
- `drawio-diagram/SKILL.md`：Codex skill 定义
- `drawio-diagram/scripts/`：确定性的辅助脚本
- `drawio-diagram/agents/`：skill 使用的 agent 配置
