# AI 数据分析智能体

一个基于 Streamlit 和 Agno 构建的 AI 数据分析智能体，支持 Excel 和 CSV 文件上传，使用阿里通义千问模型进行数据分析。

## 功能特性

- 📊 支持 Excel (.xlsx) 和 CSV 文件上传
- 🤖 集成阿里通义千问 API
- 📈 使用 Pandas 进行数据分析
- 💬 自然语言问答界面
- 🎨 美观的 Streamlit 用户界面

## 安装和运行

### 1. 创建虚拟环境
```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或者 .venv\Scripts\activate  # Windows
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 运行应用
```bash
streamlit run app.py
```

### 4. 访问应用
打开浏览器访问 `http://localhost:8501`

## 使用方法

1. 在侧边栏输入您的通义千问 API Key
2. 上传 CSV 或 Excel 文件
3. 查看数据预览
4. 在文本框中输入您的问题
5. 点击"开始分析"按钮
6. 查看分析结果

## 常见问题

### Q: 出现 "developer is not one of ['system', 'assistant', 'user', 'tool', 'function']" 错误
**A:** 这是因为 Agno 内部使用了通义千问不支持的消息角色。已通过以下方式解决：
- 添加明确的 instructions
- 设置 show_tool_calls=False
- 使用正确的 base_url 配置

### Q: 缺少 openai 模块
**A:** 运行以下命令安装：
```bash
pip install openai
```

### Q: API Key 设置问题
**A:** 确保在侧边栏正确输入了通义千问的 API Key，而不是 OpenAI 的 API Key。

## 技术栈

- **前端**: Streamlit
- **AI 框架**: Agno
- **数据处理**: Pandas
- **模型**: 阿里通义千问 (qwen-plus-latest)
- **文件处理**: openpyxl (Excel), pandas (CSV)

## 项目结构

```
data_analysis_agent/
├── app.py              # 主应用文件 (Pandas版本)
├── app_duckdb.py       # DuckDB SQL版本应用文件
├── requirements.txt    # 依赖列表
├── README.md          # 项目文档
└── .venv/             # 虚拟环境目录
```

## 版本说明

### 📊 Pandas 版本 (app.py)
- 使用 PandasTools 进行数据分析
- 适合基础的数据操作和统计分析
- 通过自然语言描述数据分析需求

### 🗃️ DuckDB 版本 (app_duckdb.py)
- 使用 DuckDbTools 进行 SQL 查询分析
- 支持复杂的 SQL 查询操作 (JOIN, GROUP BY, 窗口函数等)
- 文件保存到临时目录，支持更大的数据集
- 自动清理临时文件，避免磁盘空间浪费
- 提供 SQL 查询建议和数据结构预览
- 支持自然语言转 SQL 查询
- 适合需要复杂查询和数据库操作的场景

### 运行不同版本

*直接运行**

Pandas 版本:
```bash
streamlit run app.py
```

DuckDB 版本:
```bash
streamlit run app_duckdb.py --server.port 8502
```

## 开发者注意事项

- 使用了 Agno 的 PandasTools 进行数据操作
- 通过 OpenAIChat 兼容模式连接通义千问 API
- 数据框以 "uploaded_data" 名称存储在 PandasTools 中
- 所有错误都有友好的用户提示

## 许可证

本项目遵循 MIT 许可证。 