---
name: ppt-maker
description: 创建、修改和优化 PowerPoint 演示文稿 (.pptx)。当用户提到做 PPT、PowerPoint、幻灯片、演示文稿、slides、presentation、deck、pitch，或需要将内容/数据/报告/论文转换为演示文稿时使用此 skill。支持 6 种视觉风格（corporate/startup/executive/dark/minimal/creative）、真实图表/表格/图表生成、Markdown 大纲和 JSON 输入、模板分析。即使只说"帮我做个 PPT"也应触发——主动询问细节，或根据已有信息直接生成。
---

# PPT Maker

基于 python-pptx 的专业演示文稿制作 skill。提供两种工作模式：

- **Script 模式**：调用内置脚本批量生成（适合大纲/JSON/模板化场景）
- **Custom 模式**：Claude 直接编写 python-pptx 代码（适合复杂定制、精细控制）

核心原则：**先理解意图，再设计方案，最后生成**。

## 工作流

### 阶段 1：需求确认

判断用户提供的信息量：

| 情况 | 操作 |
|------|------|
| 提供了主题 + 内容 + 用途 | 直接进入阶段 2 |
| 只说"帮我做个 PPT" | 用 3-5 个问题确认：主题、用途、风格、页数 |
| 给了链接/文件 | 先读取内容，提炼要点后再进入阶段 2 |

需要确认的要素：

| 要素 | 默认值 |
|------|--------|
| 主题/内容 | 由用户提供 |
| 风格 | corporate（商务蓝） |
| 用途 | 由用户决定 |
| 特殊元素 | 按需添加图表/表格 |
| 语言 | 中文内容自动设置中文字体 |

### 阶段 2：结构设计

用文字列出幻灯片大纲并告知用户：

```
幻灯片结构：
1. 封面页 — 标题 + 副标题
2. 目录页 — 议程
3. 内容页 — [主题]
4. 数据页 — 图表/表格
5. 总结页 — 关键结论
6. 结束页 — Thank You
```

### 阶段 3：选择生成模式

根据场景选择：

| 场景 | 推荐模式 |
|------|----------|
| 有 Markdown 大纲文件 | Script `--outline` |
| 有 JSON 数据结构 | Script `--json` |
| 只有主题话题 | Script `--topic` |
| 需要精细定制（复杂图表、合并表格、流程图等） | Custom（写代码） |
| 用户要求修改已有 PPT | Custom（读取 + 修改代码） |

### 阶段 4-A：Script 模式

使用 `{baseDir}/scripts/create_pptx.py`：

```bash
# 从 Markdown 大纲
python3 {baseDir}/scripts/create_pptx.py --outline outline.md --style corporate --output result.pptx

# 从话题自动生成
python3 {baseDir}/scripts/create_pptx.py --topic "AI in Healthcare" --slides 8 --style startup --output result.pptx

# 从 JSON 结构
python3 {baseDir}/scripts/create_pptx.py --json slides.json --style executive --output result.pptx

# 列出可用风格
python3 {baseDir}/scripts/create_pptx.py --list-styles
```

**6 种内置风格**：

| 风格 | 特点 |
|------|------|
| corporate | 深蓝 + Arial，商务经典 |
| startup | 紫色 + Segoe UI，创投路演 |
| executive | 金色 + Georgia/Calibri，高管汇报 |
| dark | 深色背景 + 青色，科技演示 |
| minimal | 白色 + 蓝色点缀，极简 |
| creative | 橙色 + 浅灰背景，创意设计 |

### 阶段 4-B：Custom 模式

当需要精细控制时，编写 Python 代码生成。设计参考：

- 视觉设计原则：`references/design.md`
- 可用风格常量与 builder 函数：参考 `scripts/create_pptx.py` 中的 `STYLES` 字典

**设计规范速查**：

```
页面尺寸：13.333" x 7.5" (16:9)
边距：左右 0.8"，上下 0.5"
标题大小：Pt(30~48)，加粗
正文大小：Pt(14~18)
每页最多 6 个要点
封面/结束页用深色背景
必须有 accent bar 装饰
必须有页码 footer
```

### 阶段 5：交付

1. 保存文件到 `/root/personal-study/`，命名 `YYYY-MM-DD_主题.pptx`
2. 告知用户：文件路径、幻灯片数量、使用的风格
3. 列出每页的标题
4. 询问是否需要调整

## Markdown 大纲格式

```markdown
# 演示标题
subtitle: 副标题
author: 作者名

## 第一页标题
- 要点 1
- 要点 2
- 要点 3

## 图表页
- chart: bar
- data: Q1=120, Q2=145, Q3=132, Q4=178

## 表格页
- table: data.csv
- 补充说明文字
```

## JSON 输入格式

```json
{
  "title": "标题",
  "subtitle": "副标题",
  "author": "作者",
  "slides": [
    {
      "title": "项目符号页",
      "layout": "title_and_content",
      "bullets": ["要点 1", "要点 2", "要点 3"]
    },
    {
      "title": "柱状图",
      "layout": "chart",
      "chart_type": "bar",
      "chart_data": {
        "categories": ["Q1", "Q2", "Q3", "Q4"],
        "series": [
          {"name": "产品 A", "values": [120, 150, 180, 210]},
          {"name": "产品 B", "values": [90, 110, 130, 145]}
        ]
      }
    },
    {
      "title": "数据表格",
      "layout": "table",
      "table": {
        "headers": ["指标", "Q1", "Q2"],
        "rows": [["收入", "$120K", "$150K"], ["成本", "$80K", "$90K"]]
      }
    },
    {
      "title": "章节分隔",
      "layout": "section",
      "subtitle": "章节描述"
    }
  ]
}
```

## 支持的布局类型

| layout 值 | 说明 |
|-----------|------|
| `title_and_content` | 标题 + 项目符号（默认） |
| `section` | 章节分隔页（深色背景 + 居中大字） |
| `two_column` | 双栏布局 |
| `image_and_text` | 左图右文 |
| `chart` | 图表页（柱状/折线/饼图/散点） |
| `table` | 数据表格 |
| `blank` | 空白页（自由内容） |

## 支持的图表类型

| chart_type | 说明 |
|------------|------|
| `bar` / `column` | 柱状图 |
| `bar_stacked` | 堆叠柱状图 |
| `line` | 折线图 |
| `line_markers` | 带标记折线图 |
| `pie` | 饼图 |
| `area` / `area_stacked` | 面积图 |
| `scatter` | 散点图 |

## 模板分析

分析已有 PPTX 文件的结构：

```bash
python3 {baseDir}/scripts/analyze_template.py existing.pptx
python3 {baseDir}/scripts/analyze_template.py existing.pptx --json --output analysis.json
```

## 错误处理

| 场景 | 处理方式 |
|------|----------|
| python-pptx 未安装 | `pip install python-pptx` |
| 图片文件不存在 | 用带色矩形占位 |
| 图表数据缺失 | 使用示例数据，标注需替换 |
| 文件保存失败 | 检查路径，尝试备用路径 |
