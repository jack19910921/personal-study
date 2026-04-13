# Claw Code 快速上手

> **仓库地址**: https://github.com/ultraworkers/claw-code
> **Reading Date**: 2026-04-13

## 环境要求

- **操作系统**: macOS / Linux / Windows (PowerShell / Git Bash / WSL)
- **语言版本**: Rust 1.70+ (通过 rustup 安装)
- **其他工具**: Git、curl
- **认证**: Anthropic API Key（`ANTHROPIC_API_KEY`）或其他兼容 API Key

## 安装步骤

### 1. 克隆仓库

```bash
cd ~/personal-study/coding/github
git clone https://github.com/ultraworkers/claw-code.git
cd claw-code/rust
```

### 2. 安装 Rust（如未安装）

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env
cargo --version  # 验证安装
```

### 3. 编译

```bash
cd rust/
cargo build --workspace
```

编译后二进制位于 `target/debug/claw`。

### 4. 设置 API Key

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

或使用其他兼容 provider：

```bash
export OPENAI_API_KEY="sk-..."
export OPENAI_BASE_URL="https://your-openai-compatible-endpoint"
```

### 5. 验证安装

```bash
./target/debug/claw doctor
```

这个命令会检查：
- API Key 是否有效
- 网络连通性
- 工具可用性

## 快速体验

### 交互式 REPL

```bash
./target/debug/claw --model claude-sonnet-4-6
```

进入 REPL 后可以直接对话，使用斜杠命令控制：

```
> /help          # 查看帮助
> /status        # 查看当前状态
> /compact       # 压缩会话
> /cost          # 查看花费
> /doctor        # 诊断环境
> /mcp list      # 查看 MCP 服务器
> /skills list   # 查看可用技能
> /exit          # 退出
```

### 一次性 prompt

```bash
./target/debug/claw prompt "解释这个项目的架构"
```

### JSON 输出（适合脚本自动化）

```bash
./target/debug/claw --output-format json prompt "总结 src/ 目录"
```

### 管道输入

```bash
cat Cargo.toml | ./target/debug/claw prompt "分析这个 workspace 配置"
```

### 恢复上次会话

```bash
./target/debug/claw --resume latest
```

## 配置说明

### 环境变量

| 变量 | 说明 |
|------|------|
| `ANTHROPIC_API_KEY` | Anthropic API Key |
| `ANTHROPIC_BASE_URL` | 自定义 API 端点 |
| `ANTTHROPIC_AUTH_TOKEN` | OAuth bearer token |
| `OPENAI_API_KEY` | OpenAI 兼容 API Key |

### 配置文件

项目级配置：`.claw.json`
全局配置：`~/.claude.json`（兼容 Claude Code 路径）

### 模型别名

| 别名 | 实际模型 |
|------|---------|
| `opus` | `claude-opus-4-6` |
| `sonnet` | `claude-sonnet-4-6` |
| `haiku` | `claude-haiku-4-5-20251213` |

## 常见问题

### Q1: `cargo install claw-code` 装了不对的东西

**问题**: 这个包名是废弃的，会安装一个只打印 `"claw-code has been renamed to agent-code"` 的 stub。

**解决方法**: 不要用 `cargo install claw-code`。要么从源码构建（上面的步骤），要么：

```bash
cargo install agent-code   # 安装上游二进制，名为 'claw'
```

### Q2: 编译太慢 / 内存不够

**问题**: 这台机器只有 1.6GB 内存。

**解决方法**:
```bash
# 只编译主 crate，不编译全部 workspace
cargo build -p rusty-claude-cli

# 或者用 release 模式（编译更慢但运行更快）
cargo build --release -p rusty-claude-cli
```

### Q3: API Key 报错

**问题**: `error: ANTHROPIC_API_KEY not set`

**解决方法**:
```bash
echo $ANTHROPIC_API_KEY  # 确认已设置
export ANTHROPIC_API_KEY="sk-ant-..."
# 如果要持久化，加到 ~/.bashrc 或 ~/.zshrc
```

### Q4: Windows 上运行

**问题**: `claw: command not found`

**解决方法**:
```powershell
# PowerShell 中用 .exe 后缀
.\target\debug\claw.exe prompt "say hello"

# 或者用 cargo run 跳过路径查找
cargo run -p rusty-claude-cli -- prompt "say hello"
```

### Q5: 如何本地测试而不花 API 费用

**解决方法**: 使用 mock Anthropic service：

```bash
cd rust/
# 启动 mock 服务
cargo run -p mock-anthropic-service -- --bind 127.0.0.1:8080

# 在另一个终端设置 mock 端点
export ANTHROPIC_BASE_URL="http://127.0.0.1:8080"
export ANTHROPIC_API_KEY="fake-key-for-testing"

# 然后正常使用 claw
./target/debug/claw prompt "test"
```

## 下一步学习

### 推荐阅读的源码文件

1. **入口**: `rust/crates/rusty-claude-cli/src/main.rs`
   - 说明：CLI 入口、参数解析、REPL 循环
   - 注意：文件很大（410KB），建议先看 `run()` 和 `parse_args()` 函数

2. **核心对话**: `rust/crates/runtime/src/conversation.rs`
   - 说明：核心对话循环，发送请求→接收响应→执行工具→持久化

3. **API 客户端**: `rust/crates/api/src/client.rs`
   - 说明：HTTP 客户端、OAuth、SSE 流式解析

4. **工具系统**: `rust/crates/tools/src/lib.rs`
   - 说明：工具注册和执行分发

5. **权限系统**: `rust/crates/runtime/src/permission_enforcer.rs`
   - 说明：权限判断逻辑

### 实验建议

1. 修改 `rust/crates/rusty-claude-cli/src/main.rs` 中的 `DEFAULT_MODEL`，换成其他模型
2. 在 `rust/crates/tools/src/lib.rs` 中添加一个自定义工具
3. 用 mock service 跑 PARITY.md 中的测试场景
4. 研究 `.claw.json` 配置文件，理解配置合并策略

## 复查记录

- 2026-04-13 23:30: 初版完成，基于 README.md、Cargo.toml、PHILOSOPHY.md、主要源码文件阅读。
