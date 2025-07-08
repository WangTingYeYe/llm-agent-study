from agno.agent import Agent
from agno.models.google import Gemini
from agno.media import Image as AgnoImage
from agno.models.openai import OpenAILike
from agno.tools.duckduckgo import DuckDuckGoTools
import streamlit as st
from typing import List, Optional
import logging
from pathlib import Path
import tempfile
import os

# Configure logging for errors only
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def initialize_agents(api_key: str) -> tuple[Agent, Agent, Agent, Agent]:
    try:
        model = OpenAILike(
            id="qwen-omni-turbo",
            api_key=api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )

        therapist_agent = Agent(
            model=model,
            name="治疗师代理",
            instructions=[
                "你是一个有同理心的治疗师，基于：",
                "1. 倾听并验证感受",
                "2. 使用幽默来减轻情绪",
                "3. 分享相关的分手经历",
                "4. 提供安慰的话语和鼓励",
                "5. 分析文本和图像输入的情感上下文",
                "在回应中保持支持和理解",
            ],
            markdown=True,
            structured_outputs=False,  # 流式输出时不支持结构化输出
        )

        closure_agent = Agent(
            model=model,
            name="结束语代理",
            instructions=[
                "你是一个结束语专家，基于：",
                "1. 创建情感消息",
                "2. 帮助表达真实的情感",
                "3. 清晰地格式化消息",
                "4. 确保语气是真诚的",
                "专注于情感释放和结束",
            ],
            markdown=True,
        )

        routine_planner_agent = Agent(
            model=model,
            name="恢复计划代理",
            instructions=[
                "你是一个恢复计划专家，基于：",
                "1. 设计7天的恢复挑战",
                "2. 包括有趣的活动和自我护理任务",
                "3. 建议社交媒体排毒策略",
                "4. 创建激励人心的播放列表",
                "专注于实际的恢复步骤",
            ],
            markdown=True,
        )

        brutal_honesty_agent = Agent(
            model=model,
            name="客观分析建议代理",
            tools=[DuckDuckGoTools()],
            instructions=[
                "你是一个直接反馈专家，基于：",
                "1. 给出关于分手的直接、客观的反馈",
                "2. 清楚地解释关系失败",
                "3. 使用直接、客观的语言",
                "4. 提供向前发展的理由",
                "专注于诚实见解，不加糖衣",
            ],
            markdown=True,
        )

        return (
            therapist_agent,
            closure_agent,
            routine_planner_agent,
            brutal_honesty_agent,
        )
    except Exception as e:
        st.error(f"Error initializing agents: {str(e)}")
        return None, None, None, None


# Set page config and UI elements
st.set_page_config(page_title="分手治愈助手", page_icon="💔", layout="wide")


# Sidebar for API key input
with st.sidebar:
    st.header("🔑 API 配置")

    if "api_key_input" not in st.session_state:
        st.session_state.api_key_input = ""

    api_key = st.text_input(
        "请输入你的 Qwen apikey",
        value=st.session_state.api_key_input,
        type="password",
        help="请输入你的 Qwen apikey",
        key="api_key_widget",
    )

    if api_key != st.session_state.api_key_input:
        st.session_state.api_key_input = api_key

    if api_key:
        st.success("API Key 已提供! ✅")
    else:
        st.warning("请输入你的 API key 以继续")
        st.markdown(
        """ 
        获取你的 API key:
        - 1. 前往 [Qwen](https://bailian.console.aliyun.com/?tab=home#/homey)
        - 2. 在侧边栏输入你的 API key
        - 3. 点击获取 API key
        - 4. 在侧边栏输入你的 API key"""
        )

# Main content
st.title("💔 分手治愈助手")
st.markdown(
    """
    ### 分手治愈助手，帮你走出分手的阴影
    分享你的感受和聊天截图，我们会帮助你度过这个艰难的时刻。
"""
)

# Input section
col1, col2 = st.columns(2)

with col1:
    st.subheader("分享你的感受")
    user_input = st.text_area(
        "你最近怎么样？发生了什么？", height=150, placeholder="告诉我们你的故事..."
    )

with col2:
    st.subheader("上传聊天截图")
    uploaded_files = st.file_uploader(
        "上传聊天截图（可选）",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        key="screenshots",
    )

    if uploaded_files:
        for file in uploaded_files:
            st.image(file, caption=file.name, use_container_width=True)

# Process button and API key check
if st.button("获取恢复计划 💝", type="primary"):
    if not st.session_state.api_key_input:
        st.warning("请先在侧边栏输入你的 API key！")
    else:
        therapist_agent, closure_agent, routine_planner_agent, brutal_honesty_agent = (
            initialize_agents(st.session_state.api_key_input)
        )

        if all(
            [
                therapist_agent,
                closure_agent,
                routine_planner_agent,
                brutal_honesty_agent,
            ]
        ):
            if user_input or uploaded_files:
                try:
                    st.header("你的个性化恢复计划")

                    def process_images(files):
                        processed_images = []
                        for file in files:
                            try:
                                temp_dir = tempfile.gettempdir()
                                temp_path = os.path.join(temp_dir, f"temp_{file.name}")

                                with open(temp_path, "wb") as f:
                                    f.write(file.getvalue())

                                agno_image = AgnoImage(filepath=Path(temp_path))
                                processed_images.append(agno_image)

                            except Exception as e:
                                logger.error(
                                    f"Error processing image {file.name}: {str(e)}"
                                )
                                continue
                        return processed_images

                    all_images = (
                        process_images(uploaded_files) if uploaded_files else []
                    )

                    # Therapist Analysis
                    with st.spinner("🤗 获取同理心支持..."):
                        therapist_prompt = f"""
                        分析情感状态并提供同理心支持，基于：
                        用户消息：{user_input}
                        
                        请提供一个有同情心的回应，包括：
                        1. 感受的验证
                        2. 安慰的话语
                        3. 相关经历
                        4. 鼓励的话语
                        """

                        response = therapist_agent.run(
                            message=therapist_prompt,
                            images=all_images,
                            stream=True,
                            debug_mode=True,
                        )
                        
                        st.subheader("🤗 情感支持")
                        # 流式渲染
                        content_placeholder = st.empty()
                        full_content = ""
                        for chunk in response:
                            if hasattr(chunk, 'content') and chunk.content:
                                full_content += chunk.content
                                content_placeholder.markdown(full_content)
                        
                        # 如果response不是generator，fallback到原来的方式
                        if not full_content and hasattr(response, 'content'):
                            content_placeholder.markdown(response.content)

                    # Closure Messages
                    with st.spinner("✍️ 撰写情感结束语..."):
                        closure_prompt = f"""
                        帮助创建情感结束语，基于：
                        用户感受：{user_input}
                        
                        请提供：
                        1. 未发送消息的模板
                        2. 情感释放练习
                        3. 结束仪式
                        4. 向前发展的策略
                        """

                        response = closure_agent.run(
                            message=closure_prompt,
                            images=all_images,
                            stream=True,
                            debug_mode=True,
                        )

                        st.subheader("✍️ 寻找结束语")
                        # 流式渲染
                        content_placeholder = st.empty()
                        full_content = ""
                        for chunk in response:
                            if hasattr(chunk, 'content') and chunk.content:
                                full_content += chunk.content
                                content_placeholder.markdown(full_content)
                        
                        if not full_content and hasattr(response, 'content'):
                            content_placeholder.markdown(response.content)

                    # Recovery Plan
                    with st.spinner("📅 创建你的恢复计划..."):
                        routine_prompt = f"""
                        设计一个7天的恢复计划，基于：
                        当前状态：{user_input}
                        
                        包括：
                        1. 每日活动和挑战
                        2. 自我护理常规
                        3. 社交媒体指南
                        4. 心情提升音乐建议
                        """

                        response = routine_planner_agent.run(
                            message=routine_prompt, images=all_images, stream=True
                        )

                        st.subheader("📅 你的恢复计划")
                        # 流式渲染
                        content_placeholder = st.empty()
                        full_content = ""
                        for chunk in response:
                            if hasattr(chunk, 'content') and chunk.content:
                                full_content += chunk.content
                                content_placeholder.markdown(full_content)
                        
                        if not full_content and hasattr(response, 'content'):
                            content_placeholder.markdown(response.content)

                    # Honest Feedback
                    with st.spinner("💪 获取客观反馈..."):
                        honesty_prompt = f"""
                        提供诚实、客观、建设性的反馈，基于：
                        情况：{user_input}
                        
                        包括：
                        1. 客观分析
                        2. 成长机会
                        3. 未来展望
                        4. 可操作的步骤
                        """

                        response = brutal_honesty_agent.run(
                            message=honesty_prompt, images=all_images, stream=True
                        )

                        st.subheader("💪 客观大实话视角")
                        # 流式渲染
                        content_placeholder = st.empty()
                        full_content = ""
                        for chunk in response:
                            if hasattr(chunk, 'content') and chunk.content:
                                full_content += chunk.content
                                content_placeholder.markdown(full_content)
                        
                        if not full_content and hasattr(response, 'content'):
                            content_placeholder.markdown(response.content)

                except Exception as e:
                    logger.error(f"Error during analysis: {str(e)}")
                    st.error("分析过程中发生错误。请检查日志以获取详细信息。")
            else:
                st.warning("请分享你的感受或上传聊天截图以获得帮助。")
        else:
            st.error("初始化代理失败。请检查你的 API key。")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Made with ❤️ by the 分手治愈助手</p>
        <p>Share your recovery journey with #分手治愈助手</p>
    </div>
""",
    unsafe_allow_html=True,
)
