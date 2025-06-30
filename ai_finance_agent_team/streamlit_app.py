"""
AI Finance Agent Team - Streamlit Web 界面
提供用户友好的 Web 界面来使用多 Agent 财务分析系统
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from agent_team import FinanceAgentTeam
import time
import re

# 页面配置
st.set_page_config(
    page_title="AI 金融分析团队",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义 CSS
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    font-weight: bold;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.sub-header {
    font-size: 1.5rem;
    color: #2e8b57;
    margin: 1rem 0;
}
.agent-card {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 10px;
    margin: 0.5rem 0;
}
.query-example {
    background-color: #e8f4fd;
    padding: 0.8rem;
    border-left: 4px solid #1f77b4;
    margin: 0.5rem 0;
    border-radius: 0 5px 5px 0;
}
.api-key-info {
    background-color: #fff3cd;
    padding: 1rem;
    border-radius: 5px;
    border-left: 4px solid #ffc107;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

def get_agent_team(api_key: str, model_provider: str):
    """创建 Agent 团队实例"""
    try:
        return FinanceAgentTeam(api_key=api_key, model_provider=model_provider)
    except Exception as e:
        st.error(f"初始化 AI 团队失败: {str(e)}")
        return None

def show_api_key_setup():
    """显示 API Key 设置界面"""
    st.markdown('<h2 class="sub-header">🔑 API 配置</h2>', unsafe_allow_html=True)
    
    # API Key 信息说明
    st.markdown("""
    <div class="api-key-info">
    <strong>🔐 关于阿里云通义千问 API Key</strong><br>
    • 访问 <a href="https://dashscope.aliyuncs.com/" target="_blank">DashScope 控制台</a> 获取 API Key<br>
    • API Key 仅在当前会话中使用，不会被保存<br>
    • 通义千问提供强大的中文理解和分析能力
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 显示使用的模型
        st.info("🇨🇳 使用模型：阿里云通义千问 (qwen-plus-latest)")
        
        # API Key 输入
        api_key = st.text_input(
            "请输入您的阿里云 API Key:",
            type="password",
            placeholder="请输入您的阿里云 DashScope API Key...",
            help="您的 API Key 将安全地用于本次会话，不会被存储"
        )
    
    with col2:
        st.markdown("### 📋 获取 API Key 步骤")
        st.markdown("""
        1. 访问 [DashScope 控制台](https://dashscope.aliyuncs.com/)
        2. 注册/登录账号
        3. 进入 **API-KEY 管理** 页面
        4. 点击 **创建新的 API Key**
        5. 复制并粘贴到左侧输入框
        """)
    
    # 固定使用 qwen 作为模型提供商
    model_provider = "qwen"
    
    return api_key, model_provider

def main():
    """主应用界面"""
    
    # 标题
    st.markdown('<h1 class="main-header">🤖 AI 金融分析团队</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">基于阿里云通义千问的多 Agent 协作智能财务分析系统</p>', unsafe_allow_html=True)
    
    # API Key 配置
    api_key, model_provider = show_api_key_setup()
    
    # 检查 API Key 是否已提供
    if not api_key:
        st.warning("⚠️ 请先配置您的 API Key 才能使用 AI 分析功能")
        
        # 显示功能预览
        st.markdown("---")
        st.markdown('<h2 class="sub-header">✨ 功能预览</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="agent-card">', unsafe_allow_html=True)
            st.markdown("**🌐 Web Search Agent**")
            st.markdown("- 互联网搜索专家")
            st.markdown("- 收集最新新闻和市场动态") 
            st.markdown("- 监控行业趋势")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="agent-card">', unsafe_allow_html=True)
            st.markdown("**💰 Finance Analysis Agent**")
            st.markdown("- 财务分析专家")
            st.markdown("- 深度财务数据分析")
            st.markdown("- 投资建议和风险评估")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 示例查询展示
        st.markdown('<h3 class="sub-header">💡 示例查询</h3>', unsafe_allow_html=True)
        sample_queries = [
            "分析苹果公司（AAPL）的最新新闻和财务表现",
            "英伟达（NVDA）的 AI 发展对股价的影响分析",
            "电动汽车制造商的表现如何？重点关注特斯拉（TSLA）",
            "半导体公司如 AMD 和英特尔的市场前景",
            "微软（MSFT）最近的发展和股票表现总结"
        ]
        
        for i, query in enumerate(sample_queries, 1):
            st.markdown(f"**{i}.** {query}")
        
        return
    
    # 初始化团队
    if 'agent_team' not in st.session_state or st.session_state.get('api_key') != api_key:
        with st.spinner('🚀 正在启动 AI 团队...'):
            agent_team = get_agent_team(api_key, model_provider)
            if agent_team:
                st.session_state.agent_team = agent_team
                st.session_state.api_key = api_key
                st.session_state.model_provider = model_provider
                st.success('✅ AI 团队已就绪！')
            else:
                return
    
    # 侧边栏
    with st.sidebar:
        st.markdown('<h2 class="sub-header">🛠️ 系统信息</h2>', unsafe_allow_html=True)
        
        # 当前配置
        st.markdown("**🔧 当前配置**")
        st.info("🇨🇳 模型: 阿里云通义千问")
        st.info(f"API Key: {'●' * 8}{api_key[-4:] if len(api_key) > 4 else '●' * len(api_key)}")
        
        st.markdown("---")
        
        # Agent 信息卡片
        st.markdown('<div class="agent-card">', unsafe_allow_html=True)
        st.markdown("**🌐 Web Search Agent**")
        st.markdown("- 互联网搜索专家")
        st.markdown("- 收集最新新闻和市场动态") 
        st.markdown("- 监控行业趋势")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="agent-card">', unsafe_allow_html=True)
        st.markdown("**💰 Finance Analysis Agent**")
        st.markdown("- 财务分析专家")
        st.markdown("- 深度财务数据分析")
        st.markdown("- 投资建议和风险评估")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 分析历史
        st.markdown('<h3 class="sub-header">📊 分析历史</h3>', unsafe_allow_html=True)
        if 'analysis_history' not in st.session_state:
            st.session_state.analysis_history = []
        
        if st.session_state.analysis_history:
            for i, item in enumerate(st.session_state.analysis_history[-5:]):  # 显示最近5次
                with st.expander(f"🔍 {item['time']} - {item['query'][:30]}..."):
                    st.write(item['query'])
        else:
            st.info("暂无分析历史")
        
        # 清空历史
        if st.button("🗑️ 清空历史"):
            st.session_state.analysis_history = []
            st.rerun()
    
    # 主内容区域
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<h2 class="sub-header">💭 智能分析查询</h2>', unsafe_allow_html=True)
        
        # 查询输入
        query = st.text_area(
            "请输入您的分析需求：",
            placeholder="例如：分析苹果公司（AAPL）的最新财务表现和市场新闻",
            height=100
        )
        
        # 分析按钮
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
        
        with col_btn1:
            analyze_btn = st.button("🚀 开始分析", type="primary", use_container_width=True)
        
        with col_btn2:
            stream_btn = st.button("📡 流式分析", use_container_width=True)
        
        # 分析结果区域
        result_container = st.container()
        
    with col2:
        st.markdown('<h2 class="sub-header">💡 示例查询</h2>', unsafe_allow_html=True)
        
        # 获取示例查询
        if 'agent_team' in st.session_state:
            sample_queries = st.session_state.agent_team.get_sample_queries()
        else:
            sample_queries = [
                "分析苹果公司（AAPL）的最新新闻和财务表现",
                "英伟达（NVDA）的 AI 发展对股价的影响分析",
                "电动汽车制造商的表现如何？重点关注特斯拉（TSLA）"
            ]
        
        for i, sample in enumerate(sample_queries):
            if st.button(f"📝 {sample[:40]}...", key=f"sample_{i}", use_container_width=True):
                st.session_state.selected_query = sample
                # 自动填充到查询框
                st.rerun()
        
        # 如果有选中的示例查询，填充到输入框
        if 'selected_query' in st.session_state:
            query = st.session_state.selected_query
            del st.session_state.selected_query
    
    # 执行分析
    if analyze_btn or stream_btn:
        if query.strip():
            with result_container:
                st.markdown('<h2 class="sub-header">📈 分析结果</h2>', unsafe_allow_html=True)
                
                # 记录开始时间
                start_time = time.time()
                
                if stream_btn:
                    # 流式输出
                    with st.spinner('🤖 AI 团队正在协作分析...'):
                        response_container = st.empty()
                        
                        try:
                            # 这里我们模拟流式输出，实际项目中需要适配 Agno 的流式接口
                            response = st.session_state.agent_team.analyze(query, stream=False)
                            
                            # 模拟打字机效果
                            displayed_text = ""
                            for char in response:
                                displayed_text += char
                                response_container.markdown(displayed_text)
                                time.sleep(0.01)  # 控制显示速度
                                
                        except Exception as e:
                            st.error(f"分析过程中发生错误: {str(e)}")
                            response = f"分析失败: {str(e)}"
                else:
                    # 标准输出
                    with st.spinner('🤖 AI 团队正在协作分析...'):
                        try:
                            response = st.session_state.agent_team.analyze(query, stream=False)
                            st.markdown(response)
                        except Exception as e:
                            st.error(f"分析过程中发生错误: {str(e)}")
                            response = f"分析失败: {str(e)}"
                
                # 记录分析时间
                end_time = time.time()
                analysis_time = end_time - start_time
                
                # 显示分析统计
                st.markdown("---")
                col_stat1, col_stat2, col_stat3 = st.columns(3)
                
                with col_stat1:
                    st.metric("⏱️ 分析耗时", f"{analysis_time:.2f} 秒")
                
                with col_stat2:
                    st.metric("📝 响应长度", f"{len(response)} 字符")
                
                with col_stat3:
                    st.metric("🤖 Agent 数量", "2 个")
                
                # 保存到历史记录
                st.session_state.analysis_history.append({
                    'time': datetime.now().strftime("%H:%M"),
                    'query': query,
                    'response': response,
                    'analysis_time': analysis_time
                })
                
                # 下载分析报告
                if st.download_button(
                    label="📥 下载分析报告",
                    data=f"# AI 金融分析报告\n\n**查询时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n**查询内容:** {query}\n\n**分析结果:**\n\n{response}",
                    file_name=f"财务分析报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown"
                ):
                    st.success("📁 报告已下载！")
                    
        else:
            st.warning("⚠️ 请输入分析查询内容")
    
    # 页脚
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #666; font-size: 0.9rem;">'
        '🤖 Powered by Agno Multi-Agent System | 🇨🇳 阿里云通义千问 | 📊 Built with Streamlit | '
        f'⏰ {datetime.now().strftime("%Y-%m-%d %H:%M")}'
        '</p>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 