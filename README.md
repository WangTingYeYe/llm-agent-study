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

# 或使用传统 pip（在虚拟环境中）
pip install -r requirements.txt
```

## 项目列表

### 🌍 [旅行规划助手](./travel_agent/README.md)

基于 Agno 和 Gradio 构建的AI旅行规划助手，使用 DeepSeek 模型和百度搜索API。

### 🎭 [AI表情包生成器](./meme_generator_agent/README.md)

基于 BrowserUse + Streamlit 构建的智能表情包生成器，通过自然语言描述自动生成个性化表情包。

**技术栈**：
- **BrowserUse**: AI浏览器自动化框架
- **DeepSeek/OpenAI**: 大语言模型支持
- **Streamlit**: 现代化Web UI框架
- **Playwright**: 浏览器驱动引擎

**功能特点**：
- 🤖 **AI智能理解**：支持中文自然语言输入，理解用户意图
- 🌐 **浏览器自动化**：自动访问imgflip.com完成表情包制作
- 🎨 **智能模板选择**：根据主题自动选择合适的表情包模板
- ✏️ **智能文案生成**：自动生成上下文相关的表情包文字
- 🖥️ **友好界面**：基于Streamlit的现代化Web界面
- 🔧 **多模型支持**：支持DeepSeek和OpenAI两种AI模型

**快速体验**：
```bash
cd meme_generator_agent
pip install -r requirements.txt
playwright install chromium --with-deps
streamlit run ai_meme_generator_agent.py
```

### 🕷️ [AI网页爬虫](./ai_web_scrapping/README.md)

基于 ScrapegraphAI + Streamlit 构建的智能网页爬虫工具，通过自然语言描述自动提取网页内容。

**技术栈**：
- **ScrapegraphAI**: AI驱动的网页爬虫框架
- **DeepSeek**: 大语言模型支持
- **Streamlit**: 现代化Web UI框架

**功能特点**：
- 🤖 **AI智能理解**：支持自然语言描述爬取需求
- 🌐 **智能内容提取**：自动识别和提取网页关键信息
- 🎯 **精准定位**：根据用户提示精确定位目标内容
- 🖥️ **简洁界面**：基于Streamlit的用户友好界面

**快速体验**：
```bash
cd ai_web_scrapping
pip install streamlit scrapegraphai
streamlit run ai_web_scrapping.py
```

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
└── ai_web_scrapping/     # AI网页爬虫
    ├── README.md
    └── ai_web_scrapping.py  # 主程序
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
