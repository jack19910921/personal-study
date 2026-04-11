---
name: paper-reading
description: Analyze and explain academic papers. Use when the user provides a paper URL, PDF, arXiv link, DOI, or asks about a specific research paper. Also triggers for requests to "explain this paper", "summarize this paper", "read this paper", "paper on", or when the user pastes paper content/abstract. Makes sure to use this skill whenever academic papers, research articles, or technical documents need to be broken down and explained. Make sure to use this skill when the user mentions arXiv, ACL, NeurIPS, ICML, CVPR, EMNLP, or any academic conference/journal paper.
---

# Paper Reading

Analyze and explain academic papers in a structured, accessible way. Deliver a draft first, then optionally review for deeper detail if the user confirms.

## Workflow

### 0. Quick confirmation (optional)

If the user hasn't already made it clear, give a brief acknowledgment before starting — something like "收到，我来解读这篇论文"。Don't over-ask; if the intent is clear, just proceed.

### 1. Identify and fetch the paper

- If the user provided a URL, fetch it. For arXiv links, prefer the abstract page to get metadata (title, authors, abstract) and the PDF for full text.
- If the user provided a local file path, read it directly.
- If the user just named a paper, search for it and get the abstract page.

### 2. Download resources (best-effort)

Try to download:
- **PDF** — save to `papers/{paper-slug}/pdf/` under the learning repo.
- **LaTeX source** — if available on arXiv, save to `papers/{paper-slug}/source/`.

Don't fail the whole process if download fails — note it and continue with whatever content you can read.

### 3. Read the paper

Read at minimum the **abstract, introduction, and conclusion**. If the full text is accessible, read the methodology and experiments too.

### 4. Generate the draft report

Write the report as a Markdown file and save it to the learning repo (`/root/personal-study`, which is the `personal-study` repo at https://github.com/jack19910921/personal-study).

### 5. Deliver the draft

After the draft is done, tell the user:

```
论文初稿已生成：{file path}

如果你需要更详细的实验细节、公式推导或边界条件，我可以复查一轮。
```

### 6. Review (only if user confirms)

If the user wants more detail, do an incremental update — don't rewrite the whole report. Append a review section or create a `_review.md` companion file. Record what was changed and why.

## Report Structure

Use this template for the report:

```markdown
# Paper Reading: [Paper Title]

> **Authors**: [Author list]
> **Published**: [Year/Venue]
> **Source**: [URL or DOI]
> **Reading Date**: [Date]

## 一句话总结

[One sentence summary in Chinese]

## 核心问题

[What problem does this paper try to solve? Why does it matter?]

## 核心方法

[How does the paper approach the problem? Key technical contributions. Use mermaid diagrams if they help clarify architecture or flow.]

## 关键创新点

1. [Innovation 1]
2. [Innovation 2]
3. [Innovation 3]

## 实验与结果

[Key experiments, datasets, metrics, and results. Highlight what's impressive vs. what's merely adequate. Include comparison tables if helpful.]

## 优点

- [Strength 1]
- [Strength 2]

## 局限与不足

- [Limitation 1]
- [Limitation 2]

## 对我 (blog_sre) 的启发

[How does this paper relate to the user's work/interests? Practical takeaways.]

## 关键术语

| 术语 | 解释 |
|------|------|
| [Term] | [Explanation in Chinese] |
```

## Mermaid Diagrams

When the paper describes system architecture, data flow, or process steps, consider adding mermaid diagrams:

- `flowchart TD` or `flowchart LR` — for system architecture and processing pipelines
- `sequenceDiagram` — for interaction flows between components
- `graph TD` — for dependency or hierarchy

Only include diagrams that genuinely help understanding — don't add them just for the sake of having visuals.

## Writing Guidelines

- **语言**: 用中文写报告，专业术语保留英文原文，首次出现时附中文解释
- **深度**: 假设读者有工程背景但不一定是该领域的专家，解释要通俗但准确
- **重点**: 突出 "这篇文章新在哪" 和 "对我有什么用"，而不是复述已知知识
- **诚实**: 明确指出论文的不足之处，不盲目背书
- **引用**: 如果涉及公式或关键图表，注明原文位置
- **节奏**: 先交付完整初稿，不默认展开复查；用户明确要求后再深入

## File Naming

Save reports as: `papers/[year]-[month]-[short-title].md` in the learning repo.

Example: `papers/2026-04-attention-is-all-you-need.md`

PDF files go to: `papers/[year]-[month]-[short-title]/pdf/`
LaTeX source goes to: `papers/[year]-[month]-[short-title]/source/` (if available)

## After Writing

1. Commit the file to git with message: `add paper reading: [short title]`
2. Push to the remote repo
