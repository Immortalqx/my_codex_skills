# figure-spec

[English](./README.md) | 中文

`figure-spec` 从结构化 FigureSpec JSON 生成确定性的、可编辑的 SVG 图。它适合论文级架构图、workflow 图、pipeline 图、审计级联图和系统拓扑图。

当你需要一张布局可复现、可继续编辑的精确矢量图时，可以使用 `$figure-spec`：

```text
Use $figure-spec to create an editable SVG workflow diagram for this method.
```

## 依赖说明

不需要 API key。渲染器通过随 skill 携带的 Python 脚本在本地运行。

## 工作流程

1. 把图的目标转成结构化 FigureSpec JSON。
2. 使用 `scripts/figure_renderer.py` 校验 spec。
3. 根据 spec 渲染 SVG。
4. 检查 SVG/PDF，并修改 JSON，而不是直接改生成的 SVG。

## 辅助脚本

- `figure-spec/scripts/figure_renderer.py`：校验并渲染 FigureSpec JSON。

## 内容

- `figure-spec/SKILL.md`：Codex skill 定义。
- `figure-spec/scripts/`：确定性渲染器。
- `figure-spec/agents/openai.yaml`：UI 元数据。
