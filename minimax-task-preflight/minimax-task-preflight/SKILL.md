---
name: minimax-task-preflight
description: Preflight prompt clarification for MiniMax-style agent use. Use when the user wants Codex to first read a raw request, identify ambiguities, ask concise follow-up questions, and rewrite the request into a clearer and more detailed prompt before execution. This skill is for prompt understanding and clarification only. It must not pre-plan the task, design deliverables, break the work into execution steps, or optimize the later workflow.
---

# MiniMax Task Preflight

Original request: `$ARGUMENTS`

## Purpose

Use this skill to convert an underspecified or ambiguous user request into a clearer prompt that is easier for a later execution pass to follow.

This skill has a narrow role:

- read the user's request carefully
- detect ambiguity, omission, or conflicting wording
- ask concise follow-up questions when needed
- produce a rewritten prompt that preserves the user's intent

This skill does not execute the task. It also does not plan how the task should be executed.

## Hard Boundary

Do not do any of the following inside this skill:

- do not start solving the task
- do not propose an execution plan
- do not infer or design deliverables beyond what the user asked for
- do not decide task scope on the model's own authority
- do not optimize for cost, speed, or token savings
- do not decompose the work into implementation steps
- do not write acceptance criteria for downstream execution unless the user already stated them

If you find yourself deciding how the later task should be carried out, stop and return to clarification only.

## What This Skill Should Produce

The output of this skill is one of two things:

1. a short set of follow-up questions, when important ambiguity remains
2. a rewritten prompt, when the request is already clear enough or after the needed answers are available

The rewritten prompt should be more explicit than the original, but it must remain a user-facing task prompt rather than an internal plan.

## Clarification Workflow

### 1. Read the request literally

Extract only what the user explicitly asked for or strongly implied.

Focus on:

- the task the user wants done
- the subject or material involved
- any stated constraints
- any stated preferences
- any missing information that would materially change the request

Do not expand the task with assumptions about hidden requirements unless the user has already implied them.

### 2. Identify ambiguity

Ask follow-up questions only when the missing information matters.

Good reasons to ask:

- the target input is unclear
- the intended depth is unclear
- the output language or format is unclear
- multiple plausible interpretations would lead to different prompts
- the request references files, links, images, papers, or slides that are not clearly identified
- the user said something broad like "analyze this" or "read this" without enough detail to rewrite it safely

Do not ask questions that are cosmetic, low-impact, or answerable from obvious local context.

### 3. Ask concise questions

When clarification is needed:

- ask the minimum number of questions needed to remove the ambiguity
- keep questions concrete and short
- prefer high-impact questions first
- avoid bundling many minor questions together

When several questions are needed, present them as a short numbered list.

### 4. Rewrite the prompt

Once the request is clear enough, rewrite it into a stronger prompt.

The rewritten prompt should:

- preserve the user's actual intent
- remove ambiguity
- make implicit references explicit when the user has identified them
- keep the original task boundaries intact
- stay neutral about how the task will be executed

The rewritten prompt should not include internal commentary such as:

- "first think step by step"
- "make a detailed plan"
- "optimize token usage"
- "use the most efficient workflow"
- "before answering, decide the deliverable"

Those phrases shift the model into planning behavior, which this skill must avoid.

## Output Format

If clarification is required, output:

```text
Need clarification:
1. ...
2. ...
```

If the request is clear enough, output:

```text
Rewritten prompt:
<clean rewritten prompt>
```

If partial clarification has already been answered in the conversation, incorporate it and only ask the remaining necessary questions.

## Style Rules

- Keep the wording direct and plain.
- Do not add motivational language.
- Do not explain your hidden reasoning.
- Do not mention token efficiency unless the user explicitly asks for it.
- Do not praise or criticize the original prompt.
- Prefer exact wording over broad paraphrase when the user's intent is specific.

## Examples

### Example 1: ambiguous paper-reading request

User request:

```text
Read this paper carefully and explain it to me.
```

Allowed response:

```text
Need clarification:
1. Which paper should I read?
2. Do you want a broad explanation, a section-by-section explanation, or a deep technical breakdown?
3. Should I include appendix and supplementary material if they exist?
```

### Example 2: clear rewrite without planning

User request:

```text
Read the paper in paper.pdf and explain the method section in Chinese. Include the appendix if it contains training or evaluation details.
```

Allowed response:

```text
Rewritten prompt:
Read the paper in paper.pdf and explain the method section in Chinese. If the appendix contains training details, evaluation settings, implementation details, or other information needed to understand the method, include those appendix details in the explanation.
```

### Example 3: forbidden overreach

Forbidden response:

```text
Rewritten prompt:
Read the paper, make a complete execution plan, decide the final deliverable format, then summarize each section and produce a structured report.
```

Why forbidden:

- it adds deliverable design not requested by the user
- it introduces execution planning
- it changes the task instead of clarifying it

