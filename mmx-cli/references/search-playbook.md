# MiniMax CLI Search Playbook

Use this file when the task depends on `mmx search query`.

## Core Rule

Default to mixed Chinese + English and multiple search passes. One query is not enough for a non-trivial search task.

Minimum query set:

1. English technical query
2. Chinese query for the same concept
3. Mixed-language query that preserves the canonical English term

## Query Templates

### Papers / Methods / Models

English:

```text
"world model" embodied navigation benchmark
```

Chinese:

```text
具身 导航 世界模型 基准
```

Mixed:

```text
具身 导航 "world model" benchmark
```

### Product / Company / Feature

English:

```text
MiniMax M2.7 latest API update
```

Chinese:

```text
MiniMax M2.7 最新 API 更新
```

Mixed:

```text
MiniMax M2.7 最新 API update
```

### Person / Organization / Project

English:

```text
"John Smith" robotics lab
```

Chinese:

```text
"John Smith" 机器人 实验室
```

Mixed:

```text
"John Smith" robotics 实验室
```

## Expansion Rules

If the first query set is weak, add more passes with:

- abbreviations and full names
- Chinese translations and original English terms together
- venue names, domains, or site filters inside the query text
- recency modifiers such as `latest`, `today`, `2026`, `最新`, `近况`, `近期`

Example:

```text
"embodied navigation" site:openreview.net
具身 导航 site:arxiv.org
具身 导航 "embodied navigation" OpenReview
```

## Result Handling

- Compare titles and URLs across the whole query set before answering.
- Prefer primary sources, official pages, arXiv, OpenReview, or author pages when they exist.
- Do not trust a single search result when names are ambiguous.
- When the user asks for the latest or most recent status, mention concrete dates from the results you rely on.
