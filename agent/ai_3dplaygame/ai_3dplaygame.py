import streamlit as st
from agno.agent import Agent as AgnoAgent
from agno.models.openai import OpenAILike
from langchain_openai import ChatOpenAI
from langchain_community.chat_models.tongyi import ChatTongyi
import asyncio



st.set_page_config(page_title="Pygame代码生成器", layout="wide")

# Initialize session state
if "api_keys" not in st.session_state:
    st.session_state.api_keys = {"qwen": ""}

# Streamlit sidebar for API keys
with st.sidebar:
    st.title("API密钥配置")
    st.session_state.api_keys["qwen"] = st.text_input(
        "Qwen API Key", type="password", value=st.session_state.api_keys["qwen"]
    )

    st.markdown("---")
    st.info(
        """
    📝 如何使用:
    1. 在上面输入您的API密钥
    2. 编写您的Pygame可视化查询
    3. 点击 '生成代码' 获取代码
    4. 点击 '生成可视化' 来:
       - 打开Trinket.io Pygame编辑器
       - 复制并粘贴生成的代码
       - 观看它自动运行
    """
    )

# Main UI
st.title("🎮 使用Qwen的AI 3D可视化")
example_query = (
    "创建一个粒子系统模拟,其中100个粒子从鼠标位置发射,并对键盘控制的风力做出响应"
)
query = st.text_area(
    "Enter your PyGame query:", height=70, placeholder=f"e.g.: {example_query}"
)

# Split the buttons into columns
col1, col2 = st.columns(2)
generate_code_btn = col1.button("生成代码")
generate_vis_btn = col2.button("生成可视化")

if generate_code_btn and query:
    if not st.session_state.api_keys["qwen"]:
        st.error("请在侧边栏提供API密钥")
        st.stop()

    tongyi_client = ChatTongyi(
        model="qwen-plus-latest",
        api_key=st.session_state.api_keys["qwen"],
        streaming=True,
    )

    system_prompt = """您是一位专门从事 Pygame 和 Python 游戏开发与可视化编程的专家。
    在您的推理和思考过程中，请在推理中包含清晰、简洁且格式良好的 Python 代码。
    对于您提供的每段代码，都要包含相应的解释说明。"""

    try:
        # Get reasoning from Deepseek
        with st.spinner("正在生成解决方案，请稍等..."):
            message_placeholder = st.empty()
            full_response = ""

            # 创建流式响应
            res = tongyi_client.stream(
               [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query},
                ]
            )
            # 逐步获取并显示响应
            for r in res:
                full_response += r.content
                message_placeholder.markdown(full_response + "▌")

            # 完成后显示最终结果
            message_placeholder.markdown(full_response)

        # Initialize
        qwen_agent = AgnoAgent(
            model=OpenAILike(
                id="qwen-plus-latest",
                api_key=st.session_state.api_keys["qwen"],
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            ),
            show_tool_calls=True,
            markdown=True,
        )

        # Extract code
        extraction_prompt = f"""提取以下内容中与特定查询相关的 Python 代码，该查询旨在制作一个 Pygame 脚本。
        返回的代码中不要包含任何解释，或 markdown 反引号:
        {full_response}"""

        with st.spinner("正在提取代码，请稍等..."):
            code_response = qwen_agent.run(extraction_prompt)
            extracted_code = code_response.content

        # Store the generated code in session state
        st.session_state.generated_code = extracted_code

        # Display the code
        with st.expander("生成的Pygame代码", expanded=True):
            st.code(extracted_code, language="python")

        st.success("代码生成成功! 点击 '生成可视化' 运行它")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

elif generate_vis_btn:
    if "generated_code" not in st.session_state:
        st.warning("请先生成代码，然后再进行可视化。")
    else:

        async def run_pygame_on_trinket(code: str) -> None:
            import os
            from browser_use import Agent
               # 检查环境变量
            api_key = os.getenv("QWEN_API_KEY") or "sk-c0a70534d2b44fef9d413665db8f8e5e"
            
            # 禁用遥测数据收集，避免PostHog连接错误
            os.environ["BROWSER_USE_DISABLE_TELEMETRY"] = "true"

            llm = ChatOpenAI(
                        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                        model="qwen-plus-latest",
                        api_key=api_key,
                    )

            # 使用更明确的任务描述和系统提示
            task_description = f"""
            Navigate to https://trinket.io/features/pygame and run Python code in the online editor.
            
            Steps to follow:
            1. Go to https://trinket.io/features/pygame .
            2. Wait for the page to fully load (wait at least 5 seconds)
            3. Locate the code editor area on the left side
            4. Clear any existing code in the editor
            5. Input the provided Python code into the editor
            6. Find and click the "Run" button 
            7. Wait for the pygame window to appear
            8. Take a screenshot if successful
            
            code :
            ```python
            {code}
            ```
            """

            # 使用单个Agent完成整个流程，采用最简单的初始化方式
            agent = Agent(
                task=task_description,
                llm=llm,
                use_vision=False,  # 启用vision帮助识别页面元素
            )

           

            with st.spinner("在Trinket上运行代码..."):
                try:
                    # 添加更详细的进度提示
                    progress_placeholder = st.empty()
                    progress_placeholder.info("🚀 正在启动浏览器...")
                    
                    # 首先发送代码内容给 Agent
                    st.info(f"📝 准备运行的代码:\n```python\n{code[:200]}...\n```")
                    
                    # 运行 Agent，传入代码内容
                    result = await agent.run()
                    
                    # 检查任务是否成功完成
                    if result.is_done():
                        st.success("🎉 代码已在Trinket上成功运行!")
                        progress_placeholder.empty()
                    else:
                        st.warning("⚠️ 代码执行可能未完全完成，但已尽力运行")
                        progress_placeholder.empty()
                    
                    # 显示执行历史（可选，用于调试）
                    if st.checkbox("显示执行详情", key="show_details"):
                        st.write("📍 访问的URL:", result.urls() if hasattr(result, 'urls') else "N/A")
                        st.write("🔧 执行的操作:", result.action_names() if hasattr(result, 'action_names') else "N/A")
                        
                        # 显示错误信息（如果有）
                        if hasattr(result, 'errors') and result.errors():
                            st.write("❌ 遇到的错误:", result.errors())
                        
                except Exception as e:
                    st.error(f"❌ 在Trinket上运行代码时出错: {str(e)}")
                    st.info("💡 您仍然可以复制上面的代码并在Trinket上手动运行它")

        # Run the async function with the stored code
        try:
            asyncio.run(run_pygame_on_trinket(st.session_state.generated_code))
        except Exception as e:
            st.error(f"❌ 启动自动化流程时出错: {str(e)}")
            st.write("**可能的原因：**")
            st.write("- browser-use 库版本不兼容")
            st.write("- 缺少必要的依赖包")
            st.write("- 网络连接问题")
            st.write("**建议手动操作：**")
            st.write("1. 打开 https://trinket.io/features/pygame")
            st.write("2. 复制上面生成的代码")
            st.write("3. 粘贴到 Trinket 编辑器中")
            st.write("4. 点击运行按钮")

elif generate_code_btn and not query:
    st.warning("请在生成代码前输入查询内容")

