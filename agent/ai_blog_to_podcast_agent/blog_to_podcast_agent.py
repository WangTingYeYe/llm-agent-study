import os
from uuid import uuid4
from agno.agent import Agent
from agno.models.openai import OpenAILike
from agno.tools.eleven_labs import ElevenLabsTools
from agno.tools.firecrawl import FirecrawlTools
from agno.agent import Agent, RunResponse
from agno.utils.audio import write_audio_to_file
from agno.utils.log import logger
import streamlit as st

# Streamlit Page Setup
st.set_page_config(page_title="📰 ➡️ 🎙️ 播客转录代理", page_icon="🎙️")
st.title("📰 ➡️ 🎙️ 播客转录代理")

# Sidebar: API Keys
st.sidebar.header("🔑 API Keys")

qwen_api_key = st.sidebar.text_input("Qwen API Key", type="password")
elevenlabs_api_key = st.sidebar.text_input("ElevenLabs API Key", type="password")
firecrawl_api_key = st.sidebar.text_input("Firecrawl API Key", type="password")

# Check if all keys are provided
keys_provided = all([qwen_api_key, elevenlabs_api_key, firecrawl_api_key])

# Input: Blog URL
url = st.text_input("输入播客的Blog URL:", "")

# Button: Generate Podcast
generate_button = st.button("🎙️ Generate Podcast", disabled=not keys_provided)

if not keys_provided:
    st.warning("请输入所有必需的API密钥以启用播客生成。")

if generate_button:
    if url.strip() == "":
        st.warning("请先输入一个博客URL。")
    else:
        # Set API keys as environment variables for Agno and Tools
        os.environ["QWEN_API_KEY"] = qwen_api_key
        os.environ["ELEVEN_LABS_API_KEY"] = elevenlabs_api_key
        os.environ["FIRECRAWL_API_KEY"] = firecrawl_api_key

        with st.spinner(
            "处理中... 抓取博客，总结并生成播客 🎶"
        ):
            try:
                blog_to_podcast_agent = Agent(
                    name="播客转录代理",
                    agent_id="blog_to_podcast_agent",
                    model=OpenAILike(
                        id="qwen-plus-latest",
                        api_key=qwen_api_key,
                        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                    ),
                    tools=[
                        ElevenLabsTools(
                            voice_id="JBFqnCBsd6RMkjVDRZzb",
                            model_id="eleven_multilingual_v2",
                            target_directory="audio_generations",
                        ),
                        FirecrawlTools(),
                    ],
                    description="您是一个ai代理，可以使用ElevenLabs API生成音频，使用FirecrawlTools抓取博客内容，并使用Qwen API生成播客",
                    instructions=[
                        "当用户提供一个博客URL时:",
                        "1. 使用FirecrawlTools抓取博客内容",
                        "2. 创建一个简洁的总结，不超过2000个字符",
                        "3. 总结应该捕捉主要观点，同时保持有趣和对话性",
                        "4. 使用ElevenLabsTools将总结转换为音频，确保总结不超过2000个字符，以避免ElevenLabs API限制", 
                    ],
                    markdown=True,
                    debug_mode=True,
                )

                podcast: RunResponse = blog_to_podcast_agent.run(
                    f"将博客内容转换为播客: {url}"
                )

                save_dir = "audio_generations"
                os.makedirs(save_dir, exist_ok=True)

                if podcast.audio and len(podcast.audio) > 0:
                    filename = f"{save_dir}/podcast_{uuid4()}.wav"
                    write_audio_to_file(
                        audio=podcast.audio[0].base64_audio, filename=filename
                    )

                    st.success("播客生成成功! 🎧")
                    audio_bytes = open(filename, "rb").read()
                    st.audio(audio_bytes, format="audio/wav")

                    st.download_button(
                        label="下载播客",
                        data=audio_bytes,
                        file_name="generated_podcast.wav",
                        mime="audio/wav",
                    )
                else:
                    st.error("没有音频生成。请重试。")

            except Exception as e:
                st.error(f"An error occurred: {e}")
                logger.error(f"Streamlit app error: {e}")
