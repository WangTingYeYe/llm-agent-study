#!/bin/bash

# 🎭 AI表情包生成器 - 快速启动脚本

clear
echo "🎭 AI表情包生成器"
echo "===================="

# 检查虚拟环境
if [[ ! -d "venv" ]]; then
    echo "❌ 虚拟环境不存在，正在创建..."
    python3 -m venv venv
    echo "✅ 虚拟环境创建完成"
fi

# 激活虚拟环境
echo "🐍 激活虚拟环境..."
source venv/bin/activate

# 显示环境信息
echo "✅ 环境已激活:"
echo "   Python: $(python --version)"
echo "   虚拟环境: $VIRTUAL_ENV"

# 检查并安装依赖
if [[ -f "requirements.txt" ]]; then
    echo ""
    echo "📦 检查依赖包..."
    
    # 简单检查是否需要安装依赖
    if ! pip show streamlit >/dev/null 2>&1; then
        echo "🔄 安装依赖包..."
        pip install -r requirements.txt
        echo "✅ 依赖包安装完成"
    else
        echo "✅ 依赖包已安装"
    fi
fi

echo ""
echo "🚀 启动选项:"
echo "1. 启动 Streamlit 应用"
echo "2. 运行 Python 脚本"
echo "3. 只激活环境 (保持在当前shell)"
echo "4. 退出"

read -p "请选择 (1-4): " choice

case $choice in
    1)
        echo "🌐 启动 Streamlit 应用..."
        streamlit run ai_meme_generator_agent.py
        ;;
    2)
        echo "🐍 运行 Python 脚本..."
        python ai_meme_generator_agent.py
        ;;
    3)
        echo "💡 虚拟环境已激活，可以使用以下命令:"
        echo "   streamlit run ai_meme_generator_agent.py"
        echo "   python ai_meme_generator_agent.py"
        echo "   deactivate  # 退出虚拟环境"
        echo ""
        exec $SHELL
        ;;
    4)
        echo "👋 再见!"
        ;;
    *)
        echo "❌ 无效选择"
        ;;
esac 