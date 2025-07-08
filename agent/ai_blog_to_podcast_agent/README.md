# AI博客转播客代理

🎙️ 基于 Agno + Streamlit 构建的智能播客生成器

## 项目简介

AI博客转播客代理是一个创新的音频内容生成工具，能够将任何博客文章自动转换为高质量的播客音频。该项目结合了先进的网页爬虫技术、大语言模型总结能力和语音合成技术，为内容创作者提供了一种全新的内容再利用方式。

## 核心功能

### 🔍 智能内容抓取
- 使用 **Firecrawl** 技术精准抓取博客内容
- 支持各种网站结构，自动过滤广告和无关信息
- 保持原文核心观点和逻辑结构

### 🧠 AI智能总结
- 基于 **阿里云通义千问** (Qwen-plus-latest) 模型
- 将长篇博客文章总结为 2000 字符以内的精华内容
- 保持总结的对话性和趣味性，适合播客形式

### 🎤 高质量语音合成
- 集成 **ElevenLabs** 先进的多语言语音合成技术
- 支持自然流畅的语音表达
- 可自定义声音模型和语音风格

### 📱 友好的用户界面
- 基于 **Streamlit** 构建的现代化 Web 界面
- 简单易用的操作流程
- 实时处理状态显示和音频播放功能

## 技术架构

### 核心技术栈
- **Agno Framework**: AI代理编排框架
- **Streamlit**: Web应用框架
- **OpenAI Compatible API**: 大语言模型接口
- **Firecrawl**: 网页内容抓取
- **ElevenLabs**: 语音合成服务

### 工作流程
1. **内容抓取**: 通过 Firecrawl 获取博客完整内容
2. **智能总结**: 使用 Qwen 模型生成简洁有趣的总结
3. **语音合成**: 通过 ElevenLabs 将文本转换为自然语音
4. **音频处理**: 生成可下载的 WAV 格式音频文件

## 快速开始

### 环境要求
- Python 3.10+
- uv 或 pip 包管理器

### 安装依赖

```bash
# 进入项目目录
cd ai_blog_to_podcast_agent

# 使用 uv 安装依赖（推荐）
uv pip install -r requirements.txt

# 或使用传统 pip
pip install -r requirements.txt
```

### API 密钥配置

运行应用前，您需要准备以下 API 密钥：

1. **Qwen API Key**: 
   - 访问 [阿里云百炼平台](https://bailian.console.aliyun.com/)
   - 创建应用并获取 API Key

2. **ElevenLabs API Key**:
   - 访问 [ElevenLabs](https://elevenlabs.io/)
   - 注册账户并获取 API Key

3. **Firecrawl API Key**:
   - 访问 [Firecrawl](https://www.firecrawl.dev/)
   - 注册账户并获取 API Key

### 运行应用

```bash
streamlit run blog_to_podcast_agent.py
```

### 使用步骤

1. **配置 API 密钥**: 在侧边栏输入所需的三个 API 密钥
2. **输入博客 URL**: 在主界面输入要转换的博客文章链接
3. **生成播客**: 点击"🎙️ Generate Podcast"按钮开始处理
4. **下载音频**: 处理完成后可以直接播放或下载生成的播客音频

## 应用场景

### 内容创作者
- 将优质博客文章转换为播客内容
- 扩展内容分发渠道，触达更多受众
- 节省音频制作时间和成本

### 学习者
- 将学习资料转换为音频形式
- 支持通勤、运动时的听觉学习
- 提高信息吸收效率

### 企业用户
- 将公司博客、新闻稿转换为播客
- 创建内部培训音频材料
- 增强品牌内容的多样性

## 项目特色

### 🚀 高效自动化
- 全流程自动化处理，无需人工干预
- 从网页抓取到音频生成一键完成

### 🎯 智能优化
- AI 自动优化总结内容的播客适配性
- 保持原文精髓的同时增强听觉体验

### 🔧 易于集成
- 模块化设计，易于扩展和定制
- 支持不同的语音模型和总结策略

### 💡 创新应用
- 开创性的博客转播客解决方案
- 展示多模态 AI 应用的实际价值

## 依赖项

```txt
agno              # AI代理框架
streamlit==1.44.1 # Web应用框架
openai            # OpenAI兼容接口
Requests          # HTTP请求库
firecrawl-py      # 网页抓取工具
elevenlabs        # 语音合成服务
```

## 注意事项

### API 使用限制
- ElevenLabs 对单次请求有 2000 字符限制
- Firecrawl 可能对某些网站有访问限制
- 建议合理使用 API 以控制成本

### 支持的网站
- 大部分标准博客平台（WordPress、Medium等）
- 新闻网站和技术博客
- 静态网站和 CMS 系统

## 许可证

MIT License

## 贡献指南

欢迎提交 Issue 和 Pull Request 来改进这个项目！

### 开发建议
- 遵循项目的代码风格规范
- 添加适当的测试用例
- 更新相关文档

---

**让每一篇优质博客都能成为精彩的播客！** 🎙️✨ 