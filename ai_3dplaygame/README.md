# AI 3D 游戏代码生成器

基于 Streamlit + Qwen API + browser-use 构建的智能 3D 游戏代码生成器，通过自然语言描述自动生成 Pygame 代码并在 Trinket.io 上运行。

## 项目简介

AI 3D 游戏代码生成器是一个创新的工具，结合了大语言模型的代码生成能力和浏览器自动化技术，让用户能够通过简单的自然语言描述就能生成复杂的 Pygame 3D 游戏代码。系统不仅能生成代码，还能自动在 Trinket.io 平台上运行，实现从创意到可视化的完整闭环。

## 技术栈

- **Web 框架**: Streamlit
- **AI 模型**: 阿里云通义千问 (Qwen)
- **浏览器自动化**: browser-use
- **代码生成**: Agno Agent 框架
- **在线运行平台**: Trinket.io
- **游戏开发**: Pygame

## 核心功能

### 🎮 智能代码生成
- 基于自然语言描述生成 Pygame 代码
- 支持 3D 可视化和粒子系统
- 智能理解复杂的游戏逻辑需求

### 🚀 自动化运行
- 集成 browser-use 自动化浏览器操作
- 自动在 Trinket.io 上运行生成的代码
- 无需手动复制粘贴，一键生成并运行

### 📊 实时预览
- 流式显示代码生成过程
- 实时查看生成的 Pygame 代码
- 支持代码语法高亮显示

## 项目结构

```
ai_3dplaygame/
├── README.md                    # 项目文档
├── requirements.txt             # 依赖包列表
├── ai_3dplaygame.py            # 主程序文件
└── agent_history.gif           # 演示动图
```

## 快速开始

### 1. 环境准备

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置 API 密钥

在运行程序前，需要获取阿里云通义千问的 API 密钥：

1. 访问 [阿里云 DashScope 控制台](https://dashscope.console.aliyun.com/)
2. 创建应用并获取 API Key
3. 在程序界面的侧边栏输入 API Key

### 3. 运行应用

```bash
# 启动 Streamlit 应用
streamlit run ai_3dplaygame.py
```

应用将在浏览器中打开，通常地址为 `http://localhost:8501`

## 使用指南

### 基本使用流程

1. **配置 API 密钥**
   - 在左侧边栏输入您的 Qwen API Key

2. **输入游戏描述**
   - 在文本框中描述您想要创建的 3D 游戏或可视化效果
   - 例如："创建一个粒子系统模拟，其中100个粒子从鼠标位置发射，并对键盘控制的风力做出响应"

3. **生成代码**
   - 点击"生成代码"按钮
   - 系统将使用 AI 生成相应的 Pygame 代码
   - 代码将实时显示在界面上

4. **自动运行**
   - 点击"生成可视化"按钮
   - 系统将自动打开浏览器，访问 Trinket.io
   - 自动将代码粘贴到在线编辑器并运行

### 示例查询

- "创建一个3D立方体旋转动画，支持鼠标控制视角"
- "制作一个星空背景的太空飞船游戏"
- "生成一个彩色粒子爆炸效果"
- "创建一个简单的3D迷宫游戏"

## 高级功能

### 自定义参数

程序支持以下自定义参数：

- **温度设置**: 控制代码生成的创造性（0.1-1.0）
- **最大步数**: 控制浏览器自动化的最大操作步数
- **视觉功能**: 启用/禁用浏览器视觉识别功能

### 错误处理

程序内置了完善的错误处理机制：

- **网络连接错误**: 自动重试和友好提示
- **API 调用失败**: 详细的错误信息和解决建议
- **浏览器自动化失败**: 提供手动操作的备选方案

## 注意事项

### 系统要求

- Python 3.10+
- 稳定的网络连接
- 现代浏览器（Chrome/Firefox/Safari）

### 使用限制

- 需要有效的阿里云 API Key
- 依赖 Trinket.io 平台的可用性
- 复杂的 3D 效果可能需要较长生成时间

### 常见问题

**Q: 为什么浏览器自动化失败？**
A: 可能是网络问题或 Trinket.io 页面结构变化，可以尝试手动复制代码到 Trinket.io 运行。

**Q: 生成的代码无法运行？**
A: 可能是 API 返回的代码格式问题，可以尝试重新生成或手动调整代码。

**Q: 如何提高代码生成质量？**
A: 提供更详细和具体的需求描述，使用技术术语会得到更好的结果。

## 贡献指南

我们欢迎社区贡献！如果您想参与项目开发：

1. Fork 本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目基于 MIT 许可证开源。详见 [LICENSE](../LICENSE) 文件。

## 致谢

- [Streamlit](https://streamlit.io/) - 快速构建数据应用
- [阿里云通义千问](https://tongyi.aliyun.com/) - 强大的中文大语言模型
- [browser-use](https://github.com/browser-use/browser-use) - 浏览器自动化框架
- [Trinket.io](https://trinket.io/) - 在线 Python 运行环境
- [Pygame](https://www.pygame.org/) - Python 游戏开发库 