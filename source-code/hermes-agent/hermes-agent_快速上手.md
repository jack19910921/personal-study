# Hermes Agent 快速上手指南

> **仓库**: [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)
> **文档版本**: v1.0

---

## 1. 环境要求

| 项目 | 要求 |
|------|------|
| **操作系统** | Linux、macOS、WSL2、Android (Termux) |
| **Python** | 3.11+ |
| **工具链** | `git`、`curl`、`uv`（推荐）或 `pip` |
| **不支持** | 原生 Windows（需 WSL2） |

## 2. 安装

### 方式一：一键安装（推荐）

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
source ~/.bashrc    # 或 source ~/.zshrc
hermes              # 启动！
```

### 方式二：开发者模式

```bash
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent

# 使用 uv（推荐）
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv venv --python 3.11
source venv/bin/activate
uv pip install -e ".[all,dev]"

# 或使用 pip
python -m venv venv
source venv/bin/activate
pip install -e ".[all,dev]"

# 验证安装
python -m pytest tests/ -q
```

### 方式三：Docker

```bash
docker build -t hermes-agent .
docker run -it hermes-agent
```

## 3. 首次配置

```bash
hermes              # 启动交互模式
hermes setup        # 运行完整配置向导（推荐新手）
```

向导会引导你完成：
1. **模型选择**——选择 LLM 提供商和模型
2. **API Key 配置**——输入对应的 API 密钥
3. **工具配置**——启用/禁用工具集
4. **记忆系统**——是否启用持久化记忆
5. **消息网关**——是否配置 Telegram/Discord 等平台

## 4. 日常使用

### CLI 模式

```bash
hermes                           # 交互式聊天
hermes -q "写一个快速排序"        # 单条查询（非交互）
hermes --toolsets web,terminal   # 指定工具集
hermes model                     # 切换模型
hermes tools                     # 管理工具
hermes config set                # 修改配置
hermes doctor                    # 诊断问题
hermes update                    # 更新到最新版
```

### 消息网关模式

```bash
hermes gateway setup             # 配置平台（Telegram/Discord 等）
hermes gateway start             # 启动网关（前台）
hermes gateway start --daemon    # 启动网关（后台）
hermes gateway status            # 查看状态
hermes gateway stop              # 停止网关
```

### 常用斜杠命令（CLI 和消息平台通用）

| 命令 | 说明 |
|------|------|
| `/new` | 新会话 |
| `/reset` | 重置当前对话 |
| `/model [provider:model]` | 切换模型 |
| `/personality [name]` | 切换人格（kawaii、pirate、noir 等 12 种） |
| `/retry` | 重试上一轮 |
| `/undo` | 撤销上一轮 |
| `/compress` | 手动压缩上下文 |
| `/usage` | 查看 token 用量 |
| `/skills` | 浏览/安装技能 |
| `/stop` | 停止当前任务（消息平台） |

## 5. 配置文件位置

| 文件 | 路径 | 内容 |
|------|------|------|
| 主配置 | `~/.hermes/config.yaml` | 所有设置 |
| API Key | `~/.hermes/.env` | 密钥（不进入 Git） |
| 记忆 | `~/.hermes/memory/MEMORY.md` | Agent 记忆 |
| 用户画像 | `~/.hermes/memory/USER.md` | 用户信息 |
| 技能 | `~/.hermes/skills/` | 自定义技能 |
| 会话日志 | `~/.hermes/sessions/` | SQLite + JSON 日志 |
| 运行日志 | `~/.hermes/logs/` | agent.log / errors.log |

## 6. 多 Profile（多实例）

```bash
hermes -p coder              # 使用 "coder" profile
hermes -p research profile create personal   # 创建新 profile
hermes -p coder profile list                 # 列出所有 profile
```

每个 profile 有完全独立的 `~/.hermes/profiles/<name>/` 目录，包含独立的配置、记忆、会话和技能。

## 7. 最小可运行示例

```python
from run_agent import AIAgent

# 创建 agent
agent = AIAgent(
    model="anthropic/claude-sonnet-4-20250514",
    max_iterations=30,
    quiet_mode=True,
)

# 发起对话
result = agent.chat("用 Python 写一个快速排序")
print(result)
```

## 8. 常见问题

### Q: `ModuleNotFoundError` 怎么办？

确保在虚拟环境中：
```bash
source venv/bin/activate
```

### Q: 如何切换模型？

```bash
hermes model
# 或在对话中输入 /model openrouter/anthropic/claude-sonnet-4-20250514
```

### Q: 工具不生效？

```bash
hermes doctor              # 检查依赖
hermes tools               # 确认工具已启用
# 检查对应的 API Key 是否在 ~/.hermes/.env 中
```

### Q: 从 OpenClaw 迁移？

```bash
hermes claw migrate            # 自动导入配置、记忆、技能
hermes claw migrate --dry-run  # 先预览
```

### Q: Android Termux 安装？

```bash
# Termux 使用受限依赖
pip install -e ".[termux]"
```

### Q: 自定义人格？

编辑 `~/.hermes/config.yaml`：
```yaml
agent:
  personalities:
    my_custom: "你是一位资深的系统架构师，擅长用简洁的语言解释复杂概念。"
```

## 9. 下一步建议

如果你想深入学习源码，建议按以下顺序阅读：

1. **`hermes_constants.py`** —— 理解 HOME 路径和 Profile 机制
2. **`tools/registry.py`** —— 理解工具注册模式
3. **`model_tools.py`** —— 理解工具编排和异步桥接
4. **`run_agent.py`** 的 `AIAgent.__init__()` —— 理解 Agent 初始化流程
5. **`run_agent.py`** 的 `run_conversation()` —— 理解核心对话循环
6. **`agent/prompt_builder.py`** —— 理解系统提示词构建
7. **`gateway/run.py`** —— 理解多平台网关架构
8. **`tools/environments/base.py`** —— 理解终端后端抽象
