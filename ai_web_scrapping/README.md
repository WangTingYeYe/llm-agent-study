# 🕷️ AI 网页爬虫

基于 ScrapegraphAI + Streamlit 构建的智能网页爬虫工具，通过自然语言描述自动提取网页内容。

## 📸 项目简介

这是一个使用 AI 驱动的智能网页爬虫工具，能够根据用户的自然语言提示，自动从指定网页中提取所需信息。无需编写复杂的爬虫代码，只需描述你想要的内容即可。

## ✨ 功能特点

- 🤖 **AI智能理解**：支持自然语言描述爬取需求
- 🌐 **智能内容提取**：自动识别和提取网页关键信息
- 🎯 **精准定位**：根据用户提示精确定位目标内容
- 🖥️ **简洁界面**：基于 Streamlit 的用户友好界面
- 🔧 **多模型支持**：支持 DeepSeek 多种模型选择

## 🚀 快速开始

### 安装依赖

```bash
pip install streamlit scrapegraphai
```

### 启动应用

```bash
streamlit run ai_web_scrapping.py
```

### 使用方法

1. **打开浏览器**：访问 http://localhost:8501
2. **配置 API Key**：输入 DeepSeek API Key
3. **选择模型**：选择 deepseek-chat 或 deepseek-coder
4. **输入网址**：填写要爬取的网页 URL
5. **描述需求**：用自然语言描述想要提取的内容
6. **开始爬取**：点击"立即爬取！"按钮

## 🎯 使用示例

### 输入示例
- **URL**: `https://www.baidu.com`
- **用户提示**: `请爬取百度首页的标题`

### 更多示例
- 提取新闻网站的标题和摘要
- 获取电商网站的商品价格和描述
- 抓取博客文章的作者和发布时间
- 收集论坛帖子的回复数量

## 🛠️ 技术栈

- **前端界面**：Streamlit
- **AI 模型**：DeepSeek (deepseek-chat/deepseek-coder)
- **爬虫框架**：ScrapegraphAI
- **编程语言**：Python 3.8+

## 🔐 API Key 获取

访问 [DeepSeek 平台](https://platform.deepseek.com/) 注册账号并获取 API Key。

## 📁 项目结构

```
ai_web_scrapping/
├── ai_web_scrapping.py  # 主程序
└── README.md           # 项目说明
```

## 🚨 注意事项

1. **网络访问**：确保能正常访问目标网站
2. **API 额度**：注意 API 调用次数和费用
3. **网站规则**：遵守网站的 robots.txt 和使用条款
4. **请求频率**：避免过于频繁的请求，以免被封禁

## 📄 许可证

MIT License

---

**Made with ❤️ by ScrapegraphAI + DeepSeek** 