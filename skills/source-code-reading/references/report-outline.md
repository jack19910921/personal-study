# 源码解读报告建议结构

报告文件默认以 `<library-name>-<topic>.md` 命名。如果需要多份报告，继续沿用同一标题前缀并追加后缀区分。建议使用以下结构，并按项目内容裁剪。

```markdown
# 源码解读：[项目名称]

> **仓库地址**: https://github.com/<user>/<repo>
> **版本**: [版本号或 commit hash]
> **技术栈**: [语言、框架、关键依赖]
> **最后更新**: YYYY-MM-DD
> **Reading Date**: [阅读日期]

## 一句话总结

用一句话概括这个项目的核心价值和特点，以及为什么值得读它的源码。

## 它解决什么问题

- 项目的核心问题域
- 这个项目出现之前，开发者面临什么痛点
- 它的切入点是什么

## 整体架构

```mermaid
flowchart TD
    A[入口模块] --> B[核心模块]
    B --> C[子模块 C]
    B --> D[子模块 D]
    A --> E[工具模块]
```

### 模块划分原则

- 目录结构说明
- 关注点分离策略
- 扩展点设计

## 核心流程解析

### 流程 1：[例如"请求是如何被处理的"]

[Step-by-step walkthrough。引用具体文件和行号，如 `src/handler.py:42-58`。]

```mermaid
sequenceDiagram
    participant Client
    participant Entry
    participant Core
    Client->>Entry: 发起请求
    Entry->>Core: 调用核心逻辑
    Core-->>Entry: 返回结果
    Entry-->>Client: 响应
```

### 流程 2：[例如"配置是如何加载的"]

同上。

## 关键设计决策

| 决策 | 为什么这么做 | 代价 |
|------|-------------|------|
| [Design choice] | [Reasoning] | [Trade-off] |
| [Design choice] | [Reasoning] | [Trade-off] |

## 精妙之处

[Highlight clever/well-designed code patterns worth learning from.]

- [设计点 1]: 具体说明
- [设计点 2]: 具体说明

## 可以改进的地方

[Potential issues, outdated patterns, or areas that could be better.]

- [问题 1]: 详细说明
- [问题 2]: 详细说明

## 学习收获

### 可借鉴的设计思路

1. [思路 1]: 具体说明
2. [思路 2]: 具体说明

### 可应用到自己的项目

- 在 [具体项目] 中可以借鉴 [具体方法]
- 在 [具体场景] 下可以应用 [具体设计]

## 关键文件索引

| 文件 | 职责 |
|------|------|
| `src/index.ts` | 程序入口，了解启动流程 |
| `src/core/` | 核心实现逻辑 |
| `src/utils/` | 辅助工具函数 |

## 术语解释

| 术语 | 解释 |
|------|------|
| Term 1 | 解释 1 |
| Term 2 | 解释 2 |

## 复查记录

- YYYY-MM-DD HH:mm: 初版完成，包含哪些内容
- YYYY-MM-DD HH:mm: 第一次复查，补充了什么
- YYYY-MM-DD HH:mm: 第二次复查，修正了什么
```

## 使用要求

- 中文表达优先自然、准确，不写"AI 味"空话
- 关键逻辑一定要引用具体的文件和行号
- 如需生成 Mermaid 图，只画关键链路，不画装饰图
- 不能确认的地方要显式标注不确定性
- 区分"代码体现的"和"我的推断"
- 不要只复述注释和 docstring，要真正读代码逻辑
