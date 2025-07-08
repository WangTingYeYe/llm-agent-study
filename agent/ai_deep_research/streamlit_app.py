import streamlit as st
from textwrap import dedent
from typing import Dict, Any
import os

from agno.agent import Agent
from agno.models.openai import OpenAILike
from agno.tools import tool
from firecrawl import FirecrawlApp


# 设置页面配置
st.set_page_config(
    page_title="AI 深度研究助手",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化 session state
if 'research_results' not in st.session_state:
    st.session_state.research_results = None
if 'elaboration_results' not in st.session_state:
    st.session_state.elaboration_results = None


@tool
def deep_research(query: str, max_depth: int = 3, time_limit: int = 60, max_urls: int = 10) -> Dict[str, Any]:
    """
    使用 Firecrawl 进行深度网络研究。这是一个强大的工具，可以搜索和分析网络内容。
    
    Args:
        query: 研究查询，描述你想要研究的主题
        max_depth: 最大爬取深度 (1-5)，越高越深入但耗时更长，默认3
        time_limit: 时间限制（秒），搜索的最大时间，默认60秒
        max_urls: 最大URL数量 (5-20)，要爬取的网页数量，默认10
    
    Returns:
        Dict[str, Any]: 包含分析结果和来源的字典
        
    示例调用：
        deep_research("人工智能最新发展", max_depth=4, time_limit=120, max_urls=15)
    """
    try:
        if not st.session_state.get('firecrawl_api_key'):
            return {"error": "请先配置 Firecrawl API Key", "success": False}
            
        firecrawl_app = FirecrawlApp(api_key=st.session_state.firecrawl_api_key)
        
        def on_activity(activity):
            st.write(f"🔍 [{activity['type']}] {activity['message']}")
        
        # 显示实际使用的参数
        st.info(f"🔧 **实际调用参数**: 深度={max_depth}, 时间={time_limit}秒, URL数量={max_urls}")
        
        with st.spinner("正在进行深度研究..."):
            results = firecrawl_app.deep_research(
                query=query,
                max_depth=max_depth,
                time_limit=time_limit,
                max_urls=max_urls,
                on_activity=on_activity
            )
        
        return {
            "success": True,
            "final_analysis": results['data']['finalAnalysis'],
            "sources_count": len(results['data']['sources']),
            "sources": results['data']['sources'][:5]  # 限制显示前5个来源
        }
    except Exception as e:
        st.error(f"深度研究错误: {str(e)}")
        return {"error": str(e), "success": False}


def create_research_agent(api_key: str):
    """创建研究智能体"""
    return Agent(
        model=OpenAILike(
            id="qwen-plus-latest",
            api_key=api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        ),
        tools=[deep_research],
        description=dedent("""\
            你是一名专业的AI研究分析师，具有深度网络研究和信息综合的专业能力。
            你的专长在于创建基于事实的、引人入胜的研究报告，结合学术严谨性和叙事吸引力。

            你的写作风格：
            - 清晰且权威
            - 专业但引人入胜
            - 基于事实，引用适当
            - 对受过教育的非专业人士来说易于理解\
        """),
        instructions=dedent("""\
            1. 使用 deep_research 工具对查询进行全面的网络研究
               - 根据用户要求设置合适的研究参数（max_depth、time_limit、max_urls）
               - 如果用户没有明确指定参数，使用工具的默认值
            2. 分析和交叉引用来源的准确性和相关性
            3. 按照学术标准构建报告，但保持可读性
            4. 只包括可验证的事实和适当的引用
            5. 创建引导读者理解复杂主题的引人入胜的叙述
            6. 以可操作的要点和未来影响作为结尾\
        """),
        expected_output=dedent("""\
        专业研究报告，Markdown格式：

        # {吸引人的标题，体现主题精髓}

        ## 执行摘要
        {关键发现和重要性的简要概述}

        ## 研究背景
        {主题的背景和重要性}
        {研究/讨论的现状}

        ## 主要发现
        {重大发现或发展}
        {支持证据和分析}

        ## 影响分析
        {对领域/社会的影响}
        {未来发展方向}

        ## 关键要点
        - {要点1}
        - {要点2}
        - {要点3}

        ## 参考来源
        - [来源1] - 关键发现/引用
        - [来源2] - 关键发现/引用
        - [来源3] - 关键发现/引用

        ---
        报告生成时间：{current_date}
        由AI研究助手生成\
        """),
        markdown=True,
        show_tool_calls=True,
        add_datetime_to_instructions=True,
    )


def create_elaboration_agent(api_key: str):
    """创建内容阐述智能体"""
    return Agent(
        model=OpenAILike(
            id="qwen-plus-latest",
            api_key=api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        ),
        description=dedent("""\
            你是一名专业的研究阐述专家，专门从事内容增强和深度分析。
            你的专长在于将基础研究转化为更深入、更全面的见解。

            你的能力：
            - 深度分析和批判性思维
            - 多角度视角整合
            - 复杂概念的清晰表达
            - 前瞻性趋势分析\
        """),
        instructions=dedent("""\
            基于提供的研究内容，进行深度阐述和分析：
            1. 对研究内容进行批判性分析
            2. 提供多角度的深入见解
            3. 识别潜在的趋势和模式
            4. 提出前瞻性的观点和建议
            5. 确保内容的逻辑性和连贯性
            6. 增强可读性和实用性\
        """),
        expected_output=dedent("""\
        深度阐述报告，Markdown格式：

        # 深度阐述分析

        ## 核心洞察
        {对原始研究的深入分析和关键洞察}

        ## 多维度分析
        ### 技术视角
        {从技术角度的分析}

        ### 市场视角
        {从市场角度的分析}

        ### 社会影响
        {从社会影响角度的分析}

        ## 趋势预测
        {基于分析的未来趋势预测}

        ## 实用建议
        {针对不同群体的实用建议}

        ## 风险与机遇
        {潜在风险和机遇的分析}

        ---
        深度阐述完成时间：{current_date}
        由AI阐述专家生成\
        """),
        markdown=True,
        add_datetime_to_instructions=True,
    )


def main():
    st.title("🔬 AI 深度研究助手")
    st.markdown("基于 Qwen API 和 Agno 框架的智能研究分析平台")
    
    # 侧边栏配置
    with st.sidebar:
        st.header("⚙️ 配置设置")
        
        # API Key 配置
        st.subheader("API 配置")
        qwen_api_key = st.text_input(
            "Qwen API Key",
            type="password",
            help="请输入您的 Qwen API Key（阿里云百炼平台）"
        )
        
        firecrawl_api_key = st.text_input(
            "Firecrawl API Key",
            type="password",
            help="用于深度网络研究的 Firecrawl API Key"
        )
        
        # 显示固定配置信息
        st.info("🔧 **固定配置**\n- 模型：qwen-plus-latest\n- 端点：阿里云百炼平台")
        
        # 研究参数配置
        st.subheader("研究参数")
        max_depth = st.slider("最大爬取深度", 1, 5, 3)
        time_limit = st.slider("时间限制（秒）", 30, 300, 60)
        max_urls = st.slider("最大URL数量", 5, 20, 10)
        
        # 显示当前参数设置
        st.markdown(f"""
        **当前设置**：
        - 深度：{max_depth} 层
        - 时间：{time_limit} 秒
        - URL：{max_urls} 个
        """)
        
        # 保存配置到 session state
        if qwen_api_key:
            st.session_state.qwen_api_key = qwen_api_key
        if firecrawl_api_key:
            st.session_state.firecrawl_api_key = firecrawl_api_key
        
    
    
    # 主界面
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📝 研究问题")
        research_query = st.text_area(
            "请输入您想要研究的问题",
            height=150,
            placeholder="例如：人工智能在医疗健康领域的最新应用和发展趋势"
        )
        
        # 按钮组
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        
        with col_btn1:
            if st.button("🔍 开始研究", type="primary", use_container_width=True):
                if not research_query.strip():
                    st.error("请输入研究问题")
                elif not st.session_state.get('qwen_api_key'):
                    st.error("请配置 Qwen API Key")
                elif not st.session_state.get('firecrawl_api_key'):
                    st.error("请配置 Firecrawl API Key")
                else:
                    # 执行研究
                    with st.spinner("正在进行深度研究..."):
                        try:
                            research_agent = create_research_agent(
                                st.session_state.qwen_api_key
                            )
                            
                            # 构建包含参数的研究查询
                            research_prompt = f"""
                            请对以下问题进行深度研究：

                            {research_query}

                            请使用以下研究参数：
                            - 最大爬取深度: {max_depth}
                            - 时间限制: {time_limit} 秒
                            - 最大URL数量: {max_urls}

                            请调用 deep_research 工具时使用上述参数。
                            """
                            
                            # 显示当前使用的参数
                            st.info(f"📊 **研究参数**: 深度={max_depth}, 时间={time_limit}秒, URL数量={max_urls}")
                            
                            # 运行研究
                            response = research_agent.run(research_prompt)
                            st.session_state.research_results = response.content
                            st.success("研究完成！")
                            
                        except Exception as e:
                            st.error(f"研究过程中发生错误: {str(e)}")
        
        with col_btn2:
            if st.button("📈 深度阐述", use_container_width=True):
                if not st.session_state.get('research_results'):
                    st.error("请先完成基础研究")
                elif not st.session_state.get('qwen_api_key'):
                    st.error("请配置 Qwen API Key")
                else:
                    # 执行阐述
                    with st.spinner("正在进行深度阐述..."):
                        try:
                            elaboration_agent = create_elaboration_agent(
                                st.session_state.qwen_api_key
                            )
                            
                            elaboration_prompt = f"""
                            请对以下研究内容进行深度阐述和分析：
                            
                            {st.session_state.research_results}
                            """
                            
                            response = elaboration_agent.run(elaboration_prompt)
                            st.session_state.elaboration_results = response.content
                            st.success("深度阐述完成！")
                            
                        except Exception as e:
                            st.error(f"阐述过程中发生错误: {str(e)}")
        
        with col_btn3:
            if st.button("🗑️ 清除结果", use_container_width=True):
                st.session_state.research_results = None
                st.session_state.elaboration_results = None
                st.success("结果已清除")
    
    with col2:
        st.header("ℹ️ 使用说明")
        st.markdown("""
        ### 操作步骤：
        1. **配置API** - 在左侧设置 Qwen 和 Firecrawl API Key
        2. **调整参数** - 设置研究深度、时间限制和URL数量
        3. **输入问题** - 在文本框中输入研究问题
        4. **开始研究** - 点击按钮进行深度网络研究
        5. **深度阐述** - 对研究结果进行进一步分析
        6. **查看结果** - 在下方查看详细报告
        
        ### 功能特点：
        - 🔍 深度网络研究（可调参数）
        - 📊 多维度分析
        - 🎯 智能内容阐述
        - 📈 趋势预测
        - 💡 实用建议
        
        ### 参数说明：
        - **深度**：网页爬取的层级深度 (1-5)
        - **时间**：单次研究的最大时间 (30-300秒)
        - **URL**：最多爬取的网页数量 (5-20个)
        
        ### 参数建议：
        - **快速测试**：深度2, 时间60秒, URL 5个
        - **常规研究**：深度3, 时间120秒, URL 10个  
        - **深度研究**：深度4, 时间300秒, URL 15个
        """)
    
    # 显示结果
    if st.session_state.get('research_results'):
        st.header("📊 研究结果")
        
        # 创建选项卡
        tab1, tab2 = st.tabs(["基础研究", "深度阐述"])
        
        with tab1:
            st.markdown(st.session_state.research_results)
        
        with tab2:
            if st.session_state.get('elaboration_results'):
                st.markdown(st.session_state.elaboration_results)
            else:
                st.info("点击'深度阐述'按钮来获取更深入的分析")


if __name__ == "__main__":
    main() 