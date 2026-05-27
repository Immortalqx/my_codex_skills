# drawio_image2_pipeline

[English](./README.md) | 中文

`drawio_image2_pipeline` 是一个面向科研图示的 Codex skill 仓库，核心是先整理可编辑的 `draw.io` / `diagrams.net` 草稿，再生成与之对应的 GPT-Image-2 风格化参考图。

可安装的 skill 位于 [drawio-image2-pipeline/](./drawio-image2-pipeline/)。

## 快速开始

把 skill 复制到 `$CODEX_HOME/skills/`：

```bash
cp -R drawio-image2-pipeline "$CODEX_HOME/skills/"
```

然后让 Codex 对论文、海报或概念图任务使用 `$drawio-image2-pipeline`：

```text
Use $drawio-image2-pipeline to create a research figure from the current workspace.
Read the available paper assets first, reuse useful figures or plots, create an editable draw.io draft under image_draft/,
export PNG/SVG/PDF, run visual QA on the PNG, and only then produce a polished GPT-Image-2 reference image.
Style target: clean technical poster figure.
```

如果你已经有一个 `.drawio` 文件，希望在原图基础上继续细化，也可以这样说：

```text
Use $drawio-image2-pipeline on this existing .drawio file.
Keep the structure editable, connect an auto_drawio bridge if available, tighten the layout, re-export, run QA, and then generate the Image2 reference.
```

## 工作流程

1. Codex 先读取本地论文、海报、幻灯片、笔记或实验材料，并检查可复用的视觉素材。
2. Codex 创建或继续完善可编辑的 `sketch.drawio` 草稿。
3. Codex 导出 PNG/SVG/PDF，供用户检查和继续编辑。
4. Codex 准备 GPT-Image-2 的提示词，并生成和草稿结构一致的高质量参考图。

## 输出

默认输出目录为 `image_draft/`，通常会包含：

- `assets/`
- `asset_manifest.md`
- `sketch.drawio`
- `sketch.png`
- `sketch.svg`
- `sketch.pdf`
- `qa_notes.md`
- `image2_prompt.txt`
- `image2_result.png`
- `image2_response.json`

## Bridge 兼容性

如果工作区里已经有 `auto_drawio` bridge，这个 skill 可以接入那套流程。

接入方式写在 [drawio-image2-pipeline/references/auto_drawio.md](./drawio-image2-pipeline/references/auto_drawio.md) 里。典型场景是：工作区已经有 `auto_presentation/auto_drawio`，用户希望 Codex 一边细化图，一边通过 bridge 进行实时编辑和自动刷新。

这里并不内置 bridge 本体；仓库中保留的是 skill 定义，以及适配这类工作流的辅助脚本。

## 辅助脚本

- [drawio-image2-pipeline/scripts/inventory_assets.py](./drawio-image2-pipeline/scripts/inventory_assets.py)：盘点本地可复用素材
- [drawio-image2-pipeline/scripts/render_pdf_pages.py](./drawio-image2-pipeline/scripts/render_pdf_pages.py)：把 PDF 页面渲染成可复用图片资产
- [drawio-image2-pipeline/scripts/export_drawio.ps1](./drawio-image2-pipeline/scripts/export_drawio.ps1)：从 `.drawio` 导出 PNG/SVG/PDF
- [drawio-image2-pipeline/scripts/rightcode_image2.py](./drawio-image2-pipeline/scripts/rightcode_image2.py)：把通过 QA 的 PNG 草稿提交给 GPT-Image-2，并保存返回产物

## 参考

这套工作流兼容下列仓库中的 `auto_drawio` bridge 风格：

- [ziyuhuang123/auto_presentation](https://github.com/ziyuhuang123/auto_presentation)

这个参考仓库更偏向通用的 draw.io bridge 工作流；当前 skill 则把这套方式聚焦到科研配图、海报和演示视觉稿场景。

## 仓库结构

- `README.md` 和 `README.zh-CN.md`：仓库说明文档
- `drawio-image2-pipeline/`：可安装的 Codex skill
- `drawio-image2-pipeline/SKILL.md`：可安装的 Codex skill 定义
- `drawio-image2-pipeline/scripts/`：确定性的辅助脚本
- `drawio-image2-pipeline/references/`：bridge 和流程参考文档
- `drawio-image2-pipeline/agents/`：skill 使用的 agent 配置
