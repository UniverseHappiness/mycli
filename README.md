# mycli

一个智能化的 Agent CLI 工具,为开发者提供强大的命令行交互能力。

## 项目概述

mycli 是一个智能化的 Agent CLI 工具,旨在为开发者提供强大的命令行交互能力,支持与 AI Agent 交互、管理编排多个 Agent,以及执行自动化任务。

### 核心特性

- 🤖 **Agent 管理**: 创建、配置和管理多个 AI Agent
- 💬 **多模式交互**: 支持命令模式和 REPL 对话式交互
- 🔌 **AI 服务集成**: 支持 OpenAI、本地 LLM 等多种 AI 服务
- ⚡ **任务自动化**: 定义和执行自动化任务和工作流
- 🔧 **扩展性强**: 插件系统支持功能扩展
- 📊 **数据持久化**: 本地存储 Agent 配置和对话历史

## 快速开始

### 安装

```bash
# 使用 pip 安装
pip install mycli

# 或从源码安装
git clone https://github.com/mycli/mycli.git
cd mycli
pip install -e .
```

### 基础使用

```bash
# 查看版本
mycli --version

# 查看帮助
mycli --help

# 创建 Agent
mycli agent create --name dev-assistant --type general

# 与 Agent 对话(命令模式)
mycli chat "帮我分析这段代码"

# 启动 REPL 交互模式
mycli repl

# 查看所有 Agent
mycli agent list
```

### 配置

首次运行时,mycli 会引导您完成初始配置。配置文件位于:

- Linux/macOS: `~/.config/mycli/config.yaml`
- Windows: `%APPDATA%\mycli\config.yaml`

您也可以通过环境变量配置 API 密钥:

```bash
export MYCLI_OPENAI_API_KEY="your-api-key"
```

## 主要命令

### Agent 管理

```bash
# 列出所有 Agent
mycli agent list

# 创建 Agent
mycli agent create --name <name> --type <type>

# 查看 Agent 详情
mycli agent show <name>

# 更新 Agent 配置
mycli agent update <name> --model gpt-4

# 删除 Agent
mycli agent delete <name>
```

### 对话交互

```bash
# 快速问答
mycli chat "你的问题"

# 使用指定 Agent
mycli chat --agent dev-assistant "你的问题"

# REPL 交互模式
mycli repl
```

### 配置管理

```bash
# 查看配置
mycli config show

# 设置配置项
mycli config set ai_service.default_provider openai

# 验证配置
mycli config validate
```

## 开发

### 环境设置

```bash
# 克隆仓库
git clone https://github.com/mycli/mycli.git
cd mycli

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 安装开发依赖
pip install -e ".[dev,openai]"
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行测试并查看覆盖率
pytest --cov=mycli --cov-report=html

# 运行特定测试文件
pytest tests/test_agent.py
```

### 代码风格

```bash
# 格式化代码
black src tests

# 代码检查
ruff check src tests

# 类型检查
mypy src
```

## 项目结构

```
mycli/
├── src/
│   └── mycli/
│       ├── __init__.py
│       ├── cli.py              # CLI 入口
│       ├── config/             # 配置管理
│       ├── core/               # 核心业务逻辑
│       │   ├── agent.py        # Agent 管理
│       │   ├── session.py      # 会话管理
│       │   └── task.py         # 任务管理
│       ├── ai/                 # AI 服务层
│       │   ├── base.py         # 统一接口
│       │   ├── openai.py       # OpenAI 集成
│       │   └── local.py        # 本地 LLM
│       ├── storage/            # 存储层
│       │   ├── models.py       # 数据模型
│       │   └── database.py     # 数据库操作
│       ├── repl/               # REPL 交互
│       └── utils/              # 工具函数
├── tests/                      # 测试文件
├── docs/                       # 文档
├── pyproject.toml              # 项目配置
└── README.md                   # 项目说明
```

## 路线图

### MVP 版本 (v0.1)
- [x] 基础 CLI 框架
- [ ] Agent 管理功能
- [ ] 命令模式对话
- [ ] REPL 交互模式
- [ ] OpenAI 集成
- [ ] 本地存储

### v0.5
- [ ] 本地 LLM 支持
- [ ] 多 AI 服务提供商
- [ ] 任务自动化
- [ ] 插件系统
- [ ] 性能优化

### v1.0
- [ ] 完整的多 Agent 编排
- [ ] HTTP API 服务
- [ ] 插件市场
- [ ] Web UI
- [ ] 分布式部署支持

## 贡献

欢迎贡献! 请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 致谢

感谢所有为本项目做出贡献的开发者和用户。
