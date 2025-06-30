# AI 数据分析智能体

一个基于 Streamlit 和 Agno 构建的 AI 数据分析智能体，支持 Excel 和 CSV 文件上传，使用 DeepSeek 模型进行数据分析。

## 功能特性

- 📊 支持 Excel (.xlsx) 和 CSV 文件上传
- 🤖 集成 DeepSeek API
- 📈 使用 Pandas 进行数据分析
- 🗃️ 支持 DuckDB SQL 查询分析
- 💬 自然语言问答界面
- 🎨 美观的 Streamlit 用户界面
- 🔍 自动数据预览和统计信息
- 💡 SQL 查询建议和示例

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

**Pandas 版本:**
```bash
streamlit run app.py
```

**DuckDB 版本:**
```bash
streamlit run app_duckdb.py --server.port 8502
```

### 4. 访问应用
- Pandas 版本: `http://localhost:8501`
- DuckDB 版本: `http://localhost:8502`

## 使用方法

1. 在侧边栏输入您的 DeepSeek API Key
2. 上传 CSV 或 Excel 文件
3. 查看数据预览和基本统计信息
4. 在文本框中输入您的问题（支持自然语言或SQL查询）
5. 点击"开始分析"按钮
6. 查看分析结果

## 常见问题

### Q: 如何获取 DeepSeek API Key？
**A:** 访问 [DeepSeek 官网](https://platform.deepseek.com/) 注册账号并获取 API Key。

### Q: 缺少依赖模块
**A:** 运行以下命令安装缺失的依赖：
```bash
pip install -r requirements.txt
```

### Q: 两个版本有什么区别？
**A:** 
- **Pandas 版本**: 适合基础数据分析，使用 Pandas 工具
- **DuckDB 版本**: 支持复杂 SQL 查询，适合大数据集和复杂分析

### Q: 文件上传失败
**A:** 确保文件格式为 CSV 或 Excel (.xlsx, .xls)，文件大小不超过 200MB。

## 技术栈

- **前端**: Streamlit
- **AI 框架**: Agno
- **数据处理**: Pandas, DuckDB
- **模型**: DeepSeek API
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
- 数据直接加载到内存中进行处理
- 支持常见的数据分析操作

### 🗃️ DuckDB 版本 (app_duckdb.py)
- 使用 DuckDbTools 进行 SQL 查询分析
- 支持复杂的 SQL 查询操作 (JOIN, GROUP BY, 窗口函数等)
- 文件保存到临时目录，支持更大的数据集
- 自动清理临时文件，避免磁盘空间浪费
- 提供 SQL 查询建议和数据结构预览
- 支持自然语言转 SQL 查询
- 显示详细的数据统计信息（行数、列数、数据类型等）
- 适合需要复杂查询和数据库操作的场景

### 选择指南

- **选择 Pandas 版本** 如果您需要：
  - 快速的数据探索和基础分析
  - 简单的统计操作
  - 较小的数据集（< 100MB）

- **选择 DuckDB 版本** 如果您需要：
  - 复杂的 SQL 查询
  - 处理大型数据集
  - 高级的数据分析功能
  - 详细的数据结构信息

## 开发者注意事项

- 两个版本都使用 DeepSeek API 进行 AI 分析
- Pandas 版本数据框以 "uploaded_data" 名称存储
- DuckDB 版本使用文件名（去除扩展名）作为表名
- 所有错误都有友好的用户提示
- DuckDB 版本会自动清理临时文件

## 许可证

本项目遵循 MIT 许可证。 