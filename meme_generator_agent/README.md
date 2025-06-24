# 🎭 AI 表情包生成器

基于 BrowserUse + Streamlit 构建的智能表情包生成器，通过自然语言描述自动生成个性化表情包。

## 📸 项目简介

这是一个使用 AI 驱动的浏览器自动化工具，能够根据用户输入的文字描述，自动访问 [imgflip.com](https://imgflip.com/memetemplates) 网站，搜索合适的表情包模板，并生成带有自定义文字的表情包。

## ✨ 功能特点

- 🤖 **AI 智能理解**：支持中文自然语言输入，理解用户意图
- 🌐 **浏览器自动化**：使用 BrowserUse 自动操作浏览器完成表情包制作
- 🎨 **智能模板选择**：根据主题自动选择合适的表情包模板
- ✏️ **智能文案生成**：自动生成上下文相关的表情包文字
- 🖥️ **友好界面**：基于 Streamlit 的现代化 Web 界面
- 🔧 **多模型支持**：支持 DeepSeek 和 OpenAI 两种 AI 模型

## 🚀 快速开始

### 环境要求

- Python 3.8+
- 稳定的网络连接
- 可访问 imgflip.com

### 安装步骤

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd meme_generator_agent
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **安装浏览器驱动**
   ```bash
   playwright install chromium --with-deps
   ```

4. **启动应用**
   ```bash
   streamlit run ai_meme_generator_agent.py
   ```

### 使用方法

1. **打开浏览器**：访问 http://localhost:8502
2. **配置 API Key**：
   - 选择模型类型（推荐 DeepSeek）
   - 输入对应的 API Key
3. **输入主题**：在文本框中描述你想要的表情包场景
4. **生成表情包**：点击 "Generate Meme 🚀" 按钮
5. **查看结果**：等待 AI 自动完成制作并显示结果

## 🎯 使用示例

### 输入示例
```
如何用英语表达'食人族抓住打工人后又放回来了，因为打工人太苦了'
```

### AI 工作流程
1. 🔍 自动访问 imgflip.com/memetemplates
2. 🎯 搜索相关关键词（如 "sad", "work", "tired"）
3. 🖼️ 选择合适的表情包模板
4. ✏️ 填写上方文字和下方文字
5. 👀 预览并调整内容
6. 🎉 生成并返回表情包链接

## 🔐 API Key 获取

### DeepSeek (推荐)
- 访问：https://platform.deepseek.com/
- 注册账号并获取 API Key
- 新用户通常有免费额度

### OpenAI (备用)
- 访问：https://platform.openai.com/
- 需要 GPT-4 访问权限

## 🛠️ 技术栈

- **前端界面**：Streamlit
- **AI 模型**：DeepSeek / OpenAI GPT-4
- **浏览器自动化**：BrowserUse
- **浏览器驱动**：Playwright
- **编程语言**：Python 3.8+

## 📁 项目结构

```
meme_generator_agent/
├── ai_meme_generator_agent.py  # 主程序
├── requirements.txt           # 依赖列表
└── README.md                 # 项目说明
```

## ⚙️ 配置说明

### 模型选择
- **DeepSeek**：成本低，性能好，推荐使用
- **OpenAI**：质量高，需要付费

### 参数调整
- `max_actions_per_step`: 每步最大动作数 (默认 5)
- `max_failures`: 最大失败重试次数 (默认 25)
- `temperature`: 模型创造性 (默认 0.3)

## 🚨 注意事项

1. **网络要求**：确保能正常访问 imgflip.com
2. **API 额度**：注意 API 调用次数和费用
3. **浏览器环境**：首次运行需要下载浏览器驱动
4. **生成时间**：完整流程需要 30-60 秒，请耐心等待
5. **成功率**：复杂主题可能需要多次尝试

## 🔧 故障排除

### 常见问题

1. **API Key 错误**
   ```
   ERROR: The api_key client option must be set
   ```
   - 检查 API Key 是否正确填写
   - 确认 API Key 有效且有余额

2. **浏览器驱动问题**
   ```
   playwright._impl._api_types.Error
   ```
   - 重新安装：`playwright install chromium --with-deps`

3. **网络连接问题**
   - 检查是否能访问 imgflip.com
   - 尝试使用 VPN 或代理

4. **生成失败**
   - 尝试简化主题描述
   - 增加 `max_failures` 参数值

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支
3. 提交更改
4. 发起 Pull Request

## 📄 许可证

MIT License

## 🔗 相关链接

- [BrowserUse GitHub](https://github.com/browser-use/browser-use)
- [Streamlit 文档](https://docs.streamlit.io/)
- [DeepSeek 平台](https://platform.deepseek.com/)
- [ImgFlip 网站](https://imgflip.com/)

## 💡 灵感来源

这个项目展示了如何将 AI 语言模型与浏览器自动化结合，创造出实用且有趣的应用。通过自然语言交互，用户可以轻松创建个性化的表情包，无需手动操作复杂的图像编辑工具。

---

**Made with ❤️ by AI + BrowserUse** 