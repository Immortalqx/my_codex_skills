# novelty-check

[English](./README.md) | 中文

`novelty-check` 用于检查一个研究 idea 或方法是否已经被近期文献做过。它会抽取核心技术 claim，搜索重叠工作，并给出直接的新颖性判断。

在投入实现时间之前，可以使用 `$novelty-check`：

```text
Use $novelty-check to check whether this method idea has already been done.
```

## 依赖说明

不需要本地 API key。网络可用时，这个 skill 使用公开检索结果和公开论文页面完成查新。

## 工作流程

1. 从 proposed idea 中抽取 3-5 个核心技术 claim。
2. 检索 arXiv、Google Scholar、Semantic Scholar 和近期顶会。
3. 阅读可能重叠论文的摘要和 related work。
4. 根据收集到的证据，对比 proposed idea 和 closest prior work。
5. 输出 novelty score、closest prior work 表格、建议和定位方式。

## 内容

- `novelty-check/SKILL.md`：Codex skill 定义。
- `novelty-check/agents/openai.yaml`：UI 元数据。
