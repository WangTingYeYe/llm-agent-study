#!/bin/bash

echo "🔬 启动 AI 深度研究助手..."
echo "================================"

# 检查 Python 版本
python_version=$(python3 --version 2>&1)
echo "Python 版本: $python_version"

# 检查是否安装了 Streamlit
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit 未安装，正在安装依赖..."
    pip install -r requirements.txt
else
    echo "✅ Streamlit 已安装"
fi

echo "================================"
echo "🚀 启动应用..."
echo "应用将在 http://localhost:8501 运行"
echo "按 Ctrl+C 停止应用"
echo "================================"

# 启动 Streamlit 应用
streamlit run streamlit_app.py 