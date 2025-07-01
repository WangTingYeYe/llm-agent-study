# 💔 AI分手治愈助手

基于 Agno 和 Streamlit 构建的智能分手治愈助手，使用阿里云通义千问 Qwen Omni 模型提供全方位的分手恢复支持。

## 项目简介

AI分手治愈助手是一个温暖贴心的AI应用，专为经历分手困扰的用户设计。通过四个专业的AI代理协同工作，为用户提供情感支持、恢复计划、结束指导和客观建议，帮助用户以健康的方式走出分手阴霾。

## 主要功能

### 🤗 情感支持代理
- 倾听并验证用户感受
- 提供安慰话语和鼓励
- 分享相关经历
- 使用适当幽默缓解情绪

### ✍️ 结束语代理  
- 创建情感结束消息模板
- 提供情感释放练习
- 设计结束仪式
- 制定向前发展策略

### 📅 恢复计划代理
- 设计7天恢复挑战计划
- 推荐有趣活动和自我护理任务
- 提供社交媒体排毒建议
- 创建激励人心的音乐播放列表

### 💪 客观分析建议代理
- 提供客观、建设性的反馈
- 分析关系失败原因
- 指出成长机会
- 提供实用的向前发展建议

## 技术栈

- **前端框架**: Streamlit
- **AI框架**: Agno
- **大模型**: 阿里云通义千问 Qwen Omni Turbo
- **图像处理**: Agno Media Image
- **搜索工具**: DuckDuckGo
- **Python版本**: 3.10+

## 安装指南

### 1. 环境准备

```bash
# 进入项目目录
cd ai_breakup_recovery_agent

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# macOS/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate
```

### 2. 安装依赖

```bash
# 安装项目依赖
pip install -r requirements.txt
```

### 3. API Key 配置

1. 前往 [阿里云百炼控制台](https://bailian.console.aliyun.com/?tab=home#/homey)
2. 获取你的 Qwen API Key
3. 在应用侧边栏输入 API Key

## 使用说明

### 启动应用

```bash
# 启动 Streamlit 应用
streamlit run ai_breakup_recovery_agent.py
```

应用将在浏览器中打开，通常地址为 `http://localhost:8501`

### 使用步骤

1. **配置API**: 在侧边栏输入你的 Qwen API Key
2. **分享感受**: 在文本框中描述你的情况和感受
3. **上传截图**: （可选）上传聊天截图提供更多背景信息
4. **获取支持**: 点击"获取恢复计划 💝"按钮
5. **查看建议**: 系统将生成四个维度的专业建议

### 功能特色

- **流式响应**: 采用流式渲染，AI回复实时显示，增强互动体验
- **多模态输入**: 支持文本描述和图片上传
- **四重支持**: 情感、实用、指导、客观四个维度全面支持
- **中文优化**: 针对中文用户的情感表达和文化背景优化

## 项目结构

```
ai_breakup_recovery_agent/
├── README.md                    # 项目文档
├── requirements.txt             # 项目依赖
└── ai_breakup_recovery_agent.py # 主程序文件
```

## 依赖说明

主要依赖包括：
- `agno`: AI框架，用于构建AI代理
- `streamlit`: Web应用框架
- `openai`: 用于与通义千问API交互
- `pathlib`: 文件路径处理
- `tempfile`: 临时文件管理
- `logging`: 日志记录

## 使用注意事项

1. **API费用**: 使用通义千问API会产生费用，请注意使用量
2. **网络连接**: 需要稳定的网络连接以访问AI服务
3. **隐私保护**: 应用不会存储用户输入的个人信息
4. **专业建议**: AI建议仅供参考，严重情况请寻求专业心理咨询

## 贡献指南

欢迎提交 Issue 和 Pull Request 来改进这个项目：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/新功能`)
3. 提交更改 (`git commit -am '添加新功能'`)
4. 推送到分支 (`git push origin feature/新功能`)
5. 创建 Pull Request

## 许可证

MIT License

## 免责声明

本应用仅提供AI生成的建议和支持，不能替代专业的心理咨询或医疗服务。如果你正在经历严重的心理困扰，请寻求专业帮助。 