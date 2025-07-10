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
cd agent/travel_agent
uv pip install -r requirements.txt

# AI表情包生成器
cd agent/meme_generator_agent  
uv pip install -r requirements.txt
playwright install chromium --with-deps  # 安装浏览器驱动

# AI网页爬虫
cd agent/ai_web_scrapping
uv pip install streamlit scrapegraphai

# AI数据分析智能体
cd agent/data_analysis_agent
uv pip install -r requirements.txt

# AI金融分析团队
cd agent/ai_finance_agent_team
uv pip install -r requirements.txt

# AI深度研究助手
cd agent/ai_deep_research
uv pip install -r requirements.txt

# AI分手治愈助手
cd agent/ai_breakup_recovery_agent
uv pip install -r requirements.txt

# AI博客转播客代理
cd agent/ai_blog_to_podcast_agent
uv pip install -r requirements.txt

# AI国际象棋代理
cd agent/ai_chess_agent
uv pip install -r requirements.txt

# AI 3D 游戏代码生成器
cd agent/ai_3dplaygame
uv pip install -r requirements.txt

# 简单的PDF RAG应用程序
cd rag/simple_rag_for_pdf
uv pip install -r requirements.txt

# 基于 DeepEval 的 RAG 评估
cd rag/deepeval_rag
uv pip install -r requirements.txt

# 或使用传统 pip（在虚拟环境中）
pip install -r requirements.txt
```

## 项目列表

### 🌍 [旅行规划助手](./agent/travel_agent/README.md)

基于 Agno 和 Gradio 构建的AI旅行规划助手，使用 DeepSeek 模型和百度搜索API。

### 🎭 [AI表情包生成器](./agent/meme_generator_agent/README.md)

基于 BrowserUse + Streamlit 构建的智能表情包生成器，通过自然语言描述自动生成个性化表情包。

### 🕷️ [AI网页爬虫](./agent/ai_web_scrapping/README.md)

基于 ScrapegraphAI + Streamlit 构建的智能网页爬虫工具，通过自然语言描述自动提取网页内容。

### 📊 [AI数据分析智能体](./agent/data_analysis_agent/README.md)

基于 Streamlit 和 Agno 构建的 AI 数据分析智能体，支持 Excel 和 CSV 文件上传，使用 DeepSeek 模型进行数据分析。提供 Pandas 和 DuckDB 两个版本，满足不同复杂度的数据分析需求。

### 💰 [AI金融分析团队](./agent/ai_finance_agent_team/README.md)

基于 Agno 多 Agent 系统和 Streamlit 的智能金融分析平台，使用阿里云通义千问提供强大的中文金融分析能力。Web Agent 负责搜索最新新闻，Finance Agent 负责财务数据分析，两个 Agent 协同工作生成全面的投资研究报告。

### 🔬 [AI深度研究助手](./agent/ai_deep_research/README.md)

基于 Qwen API 和 Agno 框架的智能研究分析平台，集成深度网络研究和内容阐述功能。使用 Firecrawl 进行全面的网络信息收集，支持参数化配置（深度、时间、URL数量），提供 Research Agent 和 Elaboration Agent 双重智能体协同工作，生成专业的研究报告和深度分析。

### 💔 [AI分手治愈助手](./agent/ai_breakup_recovery_agent/README.md)

基于 Agno 和 Streamlit 构建的智能分手治愈助手，使用阿里云通义千问 Qwen Omni 模型提供全方位的分手恢复支持。通过四个专业的AI代理（情感支持、结束指导、恢复计划、客观建议）协同工作，为用户提供温暖贴心的分手恢复方案，支持流式响应和多模态输入。

### 🎙️ [AI博客转播客代理](./agent/ai_blog_to_podcast_agent/README.md)

基于 Agno + Streamlit 构建的智能播客生成器，使用阿里云通义千问和 ElevenLabs 语音合成技术。通过 Firecrawl 抓取博客内容，AI 智能总结并转换为自然流畅的播客音频，支持多语言语音合成，让文字内容瞬间变成可听的播客节目。

### ♟️ [AI国际象棋代理](./agent/ai_chess_agent/README.md)

基于 AutoGen + Streamlit 构建的智能国际象棋对战系统，使用阿里云通义千问驱动两个AI代理进行自主对战。Agent White 和 Agent Black 通过 Game Master 协调，自动分析棋局、规划策略并执行移动，展示多代理协作在复杂策略游戏中的应用，支持完整的对局记录和可视化。

### 🎮 [AI 3D 游戏代码生成器](./agent/ai_3dplaygame/README.md)

基于 Streamlit + Qwen API + browser-use 构建的智能 3D 游戏代码生成器，通过自然语言描述自动生成 Pygame 代码并在 Trinket.io 上运行。结合了大语言模型的代码生成能力和浏览器自动化技术，实现从创意到可视化的完整闭环，支持 3D 可视化、粒子系统等复杂游戏效果的智能生成。

### 📚 [简单的PDF RAG应用程序](./rag/simple_rag_for_pdf/README.md)

基于阿里百炼 DashScope 和 LangChain 框架构建的智能PDF问答系统。通过先进的RAG（检索增强生成）技术，支持PDF文档上传、智能预处理、向量化存储和精准问答。提供现代化的Streamlit Web界面，支持拖拽上传、实时进度显示、聊天历史记录等功能。包含完整的PDF预处理系统，能够自动清理文本、移除页眉页脚、优化文档结构，显著提升问答准确性。

### 🔬 [基于 DeepEval 和通义千问的 RAG 评估](./rag/deepeval_rag/README.md)

一个完整的示例，展示了如何利用 `deepeval` 框架对一个基于 LangChain 和通义千问大模型的 RAG (Retrieval-Augmented Generation) 应用进行自动化评估。

## 项目结构

```
llm-agent-study/
├── README.md              # 项目主文档
├── .gitignore            # Git 忽略规则
├── LICENSE               # 许可证文件
├── .venv/                # 虚拟环境（使用 uv 创建）
├── agent/                # AI 智能体项目集合
│   ├── travel_agent/         # 旅行规划助手子项目
│   │   ├── README.md
│   │   ├── requirements.txt
│   │   └── *.py
│   ├── meme_generator_agent/  # AI表情包生成器
│   │   ├── README.md
│   │   ├── requirements.txt
│   │   └── ai_meme_generator_agent.py  # 主程序（Streamlit版本）
│   ├── data_analysis_agent/  # AI数据分析智能体
│   │   ├── README.md
│   │   ├── requirements.txt
│   │   ├── app.py            # Pandas版本主程序
│   │   └── app_duckdb.py     # DuckDB版本主程序
│   ├── ai_web_scrapping/     # AI网页爬虫
│   │   ├── README.md
│   │   └── ai_web_scrapping.py  # 主程序
│   ├── ai_finance_agent_team/  # AI金融分析团队
│   │   ├── README.md
│   │   ├── requirements.txt
│   │   ├── agent_team.py        # 核心 Agent 团队逻辑
│   │   └── streamlit_app.py     # Streamlit Web 界面
│   ├── ai_deep_research/       # AI深度研究助手
│   │   ├── README.md
│   │   ├── requirements.txt
│   │   ├── agent.py            # 深度研究工具
│   │   ├── streamlit_app.py    # Streamlit 主应用
│   │   └── run.sh              # 启动脚本
│   ├── ai_breakup_recovery_agent/  # AI分手治愈助手
│   │   ├── README.md
│   │   ├── requirements.txt
│   │   └── ai_breakup_recovery_agent.py  # 主程序文件
│   ├── ai_blog_to_podcast_agent/  # AI博客转播客代理
│   │   ├── requirements.txt
│   │   └── blog_to_podcast_agent.py      # 主程序文件（Streamlit版本）
│   ├── ai_chess_agent/            # AI国际象棋代理
│   │   ├── requirements.txt
│   │   └── ai_chess_agent.py             # 主程序文件（AutoGen + Streamlit）
│   ├── ai_3dplaygame/             # AI 3D 游戏代码生成器
│   │   ├── README.md
│   │   ├── requirements.txt
│   │   ├── ai_3dplaygame.py          # 主程序文件（Streamlit + browser-use）
│   │   └── agent_history.gif         # 演示动图
│   └── ai_tic_tac_toe_game_agent/ # AI井字棋游戏代理
│       ├── agent.py
│       ├── app.py
│       ├── requirements.txt
│       └── utils.py
├── rag/                  # RAG (检索增强生成) 相关项目
│   ├── simple_rag_for_pdf/       # 简单的PDF RAG应用程序
│   │   ├── README.md
│   │   ├── requirements.txt
│   │   └── streamlit_app.py          # Streamlit Web应用（主程序）
│   └── deepeval_rag/           # 基于 DeepEval 的 RAG 评估
│       ├── README.md
│       ├── requirements.txt
│       ├── company_information.txt
│       ├── qa_agent.py
│       ├── dashscope_config.py
│       ├── dataset_generate.py
│       ├── test_qa_agent.py
│       └── test_app.py
└── .yoyo/                # Yoyo 配置文件
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
