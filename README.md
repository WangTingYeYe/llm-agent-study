# llm-agent-study

大模型应用开发学习项目

## 项目简介

这是一个专注于大模型应用开发的学习项目，包含多个AI应用实例和最佳实践。

## 使用环境

### 系统要求

- **Python**: 3.10+
- **包管理器**: uv (推荐) 或 pip
- **操作系统**: macOS / Linux / Windows

### 环境管理

本项目推荐使用 [uv](https://github.com/astral-sh/uv) 进行 Python 环境和依赖管理，它比传统的 pip + venv 更快更可靠。

## 快速开始

### 1. 安装 uv

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 或使用 pip 安装
pip install uv
```

### 2. 创建虚拟环境

```bash
# 使用 uv 创建虚拟环境（自动选择 Python 3.10+）
uv venv

# 激活虚拟环境
# macOS/Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate
```

### 3. 安装项目依赖

```bash
# 安装具体项目依赖
# 旅行规划助手
cd travel_agent
uv pip install -r requirements.txt

# AI表情包生成器
cd meme_generator_agent  
uv pip install -r requirements.txt
playwright install chromium --with-deps  # 安装浏览器驱动

# AI网页爬虫
cd ai_web_scrapping
uv pip install streamlit scrapegraphai

# AI数据分析智能体
cd data_analysis_agent
uv pip install -r requirements.txt

# AI金融分析团队
cd ai_finance_agent_team
uv pip install -r requirements.txt

# AI深度研究助手
cd ai_deep_research
uv pip install -r requirements.txt

# AI分手治愈助手
cd ai_breakup_recovery_agent
uv pip install -r requirements.txt

# 或使用传统 pip（在虚拟环境中）
pip install -r requirements.txt
```

## 项目列表

### 🌍 [旅行规划助手](./travel_agent/README.md)

基于 Agno 和 Gradio 构建的AI旅行规划助手，使用 DeepSeek 模型和百度搜索API。

### 🎭 [AI表情包生成器](./meme_generator_agent/README.md)

基于 BrowserUse + Streamlit 构建的智能表情包生成器，通过自然语言描述自动生成个性化表情包。

### 🕷️ [AI网页爬虫](./ai_web_scrapping/README.md)

基于 ScrapegraphAI + Streamlit 构建的智能网页爬虫工具，通过自然语言描述自动提取网页内容。

### 📊 [AI数据分析智能体](./data_analysis_agent/README.md)

基于 Streamlit 和 Agno 构建的 AI 数据分析智能体，支持 Excel 和 CSV 文件上传，使用 DeepSeek 模型进行数据分析。提供 Pandas 和 DuckDB 两个版本，满足不同复杂度的数据分析需求。

### 💰 [AI金融分析团队](./ai_finance_agent_team/README.md)

基于 Agno 多 Agent 系统和 Streamlit 的智能金融分析平台，使用阿里云通义千问提供强大的中文金融分析能力。Web Agent 负责搜索最新新闻，Finance Agent 负责财务数据分析，两个 Agent 协同工作生成全面的投资研究报告。

### 🔬 [AI深度研究助手](./ai_deep_research/README.md)

基于 Qwen API 和 Agno 框架的智能研究分析平台，集成深度网络研究和内容阐述功能。使用 Firecrawl 进行全面的网络信息收集，支持参数化配置（深度、时间、URL数量），提供 Research Agent 和 Elaboration Agent 双重智能体协同工作，生成专业的研究报告和深度分析。

### 💔 [AI分手治愈助手](./ai_breakup_recovery_agent/README.md)

基于 Agno 和 Streamlit 构建的智能分手治愈助手，使用阿里云通义千问 Qwen Omni 模型提供全方位的分手恢复支持。通过四个专业的AI代理（情感支持、结束指导、恢复计划、客观建议）协同工作，为用户提供温暖贴心的分手恢复方案，支持流式响应和多模态输入。

## 项目结构

```
llm-agent-study/
├── README.md              # 项目主文档
├── .gitignore            # Git 忽略规则
├── .venv/                # 虚拟环境（使用 uv 创建）
├── travel_agent/         # 旅行规划助手子项目
│   ├── README.md
│   ├── requirements.txt
│   └── *.py
├── meme_generator_agent/  # AI表情包生成器
│   ├── README.md
│   ├── requirements.txt
│   └── ai_meme_generator_agent.py  # 主程序（Streamlit版本）
├── data_analysis_agent/  # AI数据分析智能体
│   ├── README.md
│   ├── requirements.txt
│   ├── app.py            # Pandas版本主程序
│   └── app_duckdb.py     # DuckDB版本主程序
├── ai_web_scrapping/     # AI网页爬虫
│   ├── README.md
│   └── ai_web_scrapping.py  # 主程序
├── ai_finance_agent_team/  # AI金融分析团队
│   ├── README.md
│   ├── requirements.txt
│   ├── agent_team.py        # 核心 Agent 团队逻辑
│   └── streamlit_app.py     # Streamlit Web 界面
├── ai_deep_research/       # AI深度研究助手
│   ├── README.md
│   ├── requirements.txt
│   ├── agent.py            # 深度研究工具
│   ├── streamlit_app.py    # Streamlit 主应用
│   └── run.sh              # 启动脚本
└── ai_breakup_recovery_agent/  # AI分手治愈助手
    ├── README.md
    ├── requirements.txt
    └── ai_breakup_recovery_agent.py  # 主程序文件
```

## 开发指南

### 环境配置最佳实践

1. **使用 uv 管理依赖**: 比 pip 更快的包安装和解析
2. **虚拟环境隔离**: 每个项目使用独立的虚拟环境
3. **API Key 管理**: 使用环境变量或 `.env` 文件存储敏感信息
4. **代码规范**: 遵循 PEP 8 和项目内的 Cursor Rules

### 常用命令

```bash
# 检查 Python 版本
python --version

# 查看已安装包
uv pip list

# 更新所有包
uv pip install -r requirements.txt --upgrade

# 导出当前环境依赖
uv pip freeze > requirements.txt
```

## 许可证

MIT License
