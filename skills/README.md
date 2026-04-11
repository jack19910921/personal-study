# Skills

本目录存放自定义 Claude Code 技能（SKILL.md），已全局注册到 `~/.claude/plugins/custom/skills/`。

## 可用技能

| 技能 | 说明 | 触发条件 |
|------|------|---------|
| `paper-reading` | 论文解读助手 | arXiv 链接、PDF 文件、"解读这篇论文" |
| `source-code-reading` | 源码深度解读 | "这个库是怎么实现的"、"解释这段代码" |

## 产出规范

- 论文报告 → `papers/` 目录
- 源码解读 → `source-code/` 目录
- 每次产出自动 commit + push 到远程仓库
