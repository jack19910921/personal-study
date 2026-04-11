---
name: source-code-reading
description: Deep dive into source code — explain how a library, framework, or codebase works internally. Use when the user asks to "explain this code", "how does X work under the hood", "walk me through this codebase", "源码解读", or wants to understand the internals of a library or framework. Also triggers when the user wants to analyze a specific file, module, or function in depth. Make sure to use this skill whenever the user needs to understand code beyond surface-level explanation.
---

# Source Code Reading

Deep dive into source code and explain how it works, why it was designed that way, and what you can learn from it.

## Workflow

1. **Locate the code** — If the user named a library, find it (installed locally, or search on GitHub). If they provided a file path, read it directly. If they gave a GitHub URL, fetch the relevant files.

2. **Map the structure** — For a codebase, start from the entry point and trace the main execution path. For a single file, understand its role in the larger picture first.

3. **Analyze in depth** — Read the actual code, not just comments/docstrings. Follow function calls, trace data flow, understand design patterns.

4. **Generate a report** — Write a structured analysis and save it as a markdown file in the user's learning repository (`/root/personal-study`, which is the `personal-study` repo at https://github.com/jack19910921/personal-study).

## Report Structure

Use this template for the report:

```markdown
# Source Code Reading: [Library/Module Name]

> **Version**: [Version number or commit hash]
> **Source**: [GitHub URL or package link]
> **Reading Date**: [Date]

## 一句话总结

[One sentence: what is this, and why is it worth reading?]

## 它解决什么问题

[What problem does this library/module solve? What pain point existed before it?]

## 整体架构

[High-level architecture. Use ASCII diagram if helpful.]

```
┌─────────────┐
│   Entry     │
└──────┬──────┘
       │
  ┌────┴────┐
  │         │
Module A  Module B
```

## 核心流程解析

### [Key flow 1, e.g. "请求是如何被处理的"]

[Step-by-step walkthrough with code snippets. Cite file paths and line numbers.]

### [Key flow 2]

[Same pattern.]

## 关键设计决策

| 决策 | 为什么这么做 | 代价 |
|------|-------------|------|
| [Design choice] | [Reasoning] | [Trade-off] |

## 精妙之处

[Highlight clever/well-designed code patterns worth learning from.]

## 可以改进的地方

[Potential issues, outdated patterns, or areas that could be better.]

## 学习收获

[What can we apply to our own code? Practical takeaways.]

## 关键文件索引

| 文件 | 职责 |
|------|------|
| `path/to/file.py` | [What this file does] |
```

## Writing Guidelines

- **语言**: 用中文写报告，代码注释和变量名保留原文
- **深度**: 不要只复述注释和 docstring，要真正读代码逻辑、数据流和控制流
- **引用**: 关键逻辑一定要引用具体的文件和行号（如 `src/handler.py:42-58`）
- **对比**: 如果同类库有多个实现（比如 Flask vs FastAPI 的路由机制），对比分析它们的设计差异
- **实用**: 最终落脚点是 "我能从中学到什么" 和 "怎么用在我的项目里"

## File Naming

Save reports as: `source-code/[library-name]-[topic].md` in the learning repo.

Example: `source-code/flask-request-lifecycle.md`

## After Writing

1. Commit the file to git with message: `add source reading: [short title]`
2. Push to the remote repo
