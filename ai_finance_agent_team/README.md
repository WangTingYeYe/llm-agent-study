# AI 金融分析团队 🤖📈

基于 Agno 多 Agent 系统和 Streamlit 的智能金融分析平台，使用阿里云通义千问提供强大的中文金融分析能力。

## 系统架构

### 🌐 Web Search Agent
- **角色**: 互联网搜索专家
- **功能**: 
  - 收集最新的公司新闻和公告
  - 分析行业趋势和市场动态
  - 监控监管变化和政策影响
  - 跟踪竞争对手动态
- **工具**: DuckDuckGo 搜索

### 💰 Finance Analysis Agent  
- **角色**: 财务分析专家
- **功能**:
  - 股价表现和技术指标分析
  - 基本面分析（P/E、市值、收入增长等）
  - 分析师评级和目标价收集
  - 财务健康状况评估
  - 行业比较和估值分析
- **工具**: YFinance 财务数据

### 🤝 Team 协作模式
- **协调**: 两个 Agent 协同工作
- **流程**: Web Agent 搜索新闻 → Finance Agent 分析数据 → 综合生成报告
- **输出**: 结构化的投资研究报告

## 功能特性

✅ **多 Agent 协作**: Web Agent 和 Finance Agent 协同工作  
✅ **实时数据**: 获取最新的财务数据和市场新闻  
✅ **智能分析**: 基于阿里云通义千问的深度中文分析能力  
✅ **可视化界面**: Streamlit 提供用户友好的 Web 界面  
✅ **流式输出**: 支持实时显示分析过程  
✅ **历史记录**: 保存分析历史便于回顾  
✅ **报告下载**: 支持 Markdown 格式报告下载  
✅ **安全配置**: 用户自主配置 API Key，不存储敏感信息  
✅ **中文优化**: 专为中文金融市场分析优化  

## 快速开始

### 1. 环境配置

```bash
# 进入项目目录
cd ai_finance_agent_team

# 创建虚拟环境 (推荐)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 获取阿里云 API Key

1. 访问 [DashScope 控制台](https://dashscope.aliyuncs.com/)
2. 注册/登录阿里云账号
3. 进入 **API-KEY 管理** 页面
4. 点击 **创建新的 API Key**
5. 复制 API Key 备用

### 3. 运行应用

```bash
# 启动 Streamlit 应用
streamlit run streamlit_app.py
```

### 4. 使用步骤

1. **配置 API Key**: 在 Web 界面中输入您的阿里云 API Key
2. **输入查询**: 在文本框中输入您的分析需求
3. **开始分析**: 点击"开始分析"或"流式分析"按钮
4. **查看结果**: 等待 AI 团队完成分析并查看结果
5. **下载报告**: 可选择下载 Markdown 格式的分析报告

## 使用代码直接调用

如果您想在代码中直接使用 Agent 团队：

```python
from agent_team import FinanceAgentTeam

# 创建团队实例 (需要提供阿里云 API Key)
api_key = "your_aliyun_api_key_here"
team = FinanceAgentTeam(
    api_key=api_key, 
    model_provider="qwen"
)

# 执行分析
result = team.analyze("分析苹果公司（AAPL）的最新财务表现")
print(result)

# 流式分析
team.analyze("分析特斯拉的最新动态", stream=True)
```

## 示例查询

💡 **单一公司分析**:
- "分析苹果公司（AAPL）的最新新闻和财务表现"
- "微软（MSFT）最近的发展和股票表现总结"

💡 **行业对比**:
- "比较主要云服务提供商（AMZN、MSFT、GOOGL）的财务表现"
- "电动汽车制造商的表现如何？重点关注特斯拉（TSLA）"

💡 **投资建议**:
- "分析科技巨头（AAPL、GOOGL、MSFT）的投资组合配置建议"
- "半导体公司如 AMD 和英特尔的市场前景"

💡 **主题分析**:
- "英伟达（NVDA）的 AI 发展对股价的影响分析"
- "分析最近美联储决策对银行股的影响"

💡 **中文市场分析**:
- "分析阿里巴巴（BABA）在电商和云计算领域的竞争优势"
- "腾讯（0700.HK）的游戏和社交业务发展趋势"

## 报告格式

生成的分析报告包含以下结构：

📋 **执行摘要**: 关键发现概述  
📊 **财务数据**: 股价、基本面指标、评级  
📰 **新闻背景**: 最新动态和市场情绪  
💡 **关键要点**: 核心投资逻辑  
⚠️ **风险因素**: 潜在风险提示  
📈 **投资建议**: 基于分析的建议  

## 技术栈

- **🧠 AI 框架**: Agno Multi-Agent System
- **🌐 Web 界面**: Streamlit
- **📊 数据可视化**: Plotly
- **🔍 搜索工具**: DuckDuckGo
- **💰 财务数据**: YFinance
- **🤖 语言模型**: 阿里云通义千问 (qwen-plus-latest)

## 项目结构

```
ai_finance_agent_team/
├── agent_team.py          # 核心 Agent 团队逻辑
├── streamlit_app.py       # Streamlit Web 界面
├── requirements.txt       # 依赖包列表
└── README.md             # 项目说明文档
```

## 安全说明

🔒 **API Key 安全**:
- API Key 仅在当前会话中使用，不会被存储到本地或服务器
- 建议定期更换 API Key
- 不要在公共场所或屏幕共享时输入 API Key

## 故障排除

### 常见问题

**Q: API Key 输入后提示错误**
A: 请检查：
- API Key 是否正确复制（注意空格）
- 阿里云账户余额是否充足
- 网络是否能正常访问阿里云服务

**Q: 分析过程中出现网络错误**
A: 请检查：
- 网络连接是否正常
- 是否能访问 DashScope API 服务
- 防火墙设置是否阻止了连接

**Q: 分析结果不准确**
A: 请注意：
- 财务数据可能存在延迟
- 新闻信息的时效性
- AI 分析仅供参考，不构成投资建议

## 阿里云通义千问优势

🇨🇳 **中文优化**: 针对中文金融术语和市场特点优化  
⚡ **响应速度**: 国内访问速度快，延迟低  
💰 **成本优势**: 相比国外模型更具价格优势  
🔒 **数据安全**: 数据在国内处理，符合相关法规要求  

## 贡献指南

欢迎提交 Issue 和 Pull Request 来改进项目！

### 贡献方式
1. Fork 本项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 提交 Pull Request

## 许可证

本项目使用 MIT 许可证。详见 LICENSE 文件。

## 免责声明

⚠️ **重要提示**: 
- 本工具生成的分析报告仅供参考，不构成投资建议
- 投资有风险，决策需谨慎
- 请在做出投资决定前咨询专业财务顾问

---

🚀 **开始您的智能金融分析之旅！** 