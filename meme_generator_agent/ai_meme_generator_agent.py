import asyncio
import re
import streamlit as st
from browser_use import Agent
from langchain_openai import ChatOpenAI


async def generate_meme(query: str, model_choice: str, api_key: str) -> None:
    if not api_key or not api_key.strip():
        raise ValueError(f"API Key 不能为空")

    if model_choice == "deepseek":
        llm = ChatOpenAI(
            base_url="https://api.deepseek.com/v1",
            model="deepseek-chat",
            api_key=api_key,
            temperature=0.3,
        )
    elif model_choice == "openai":
        llm = ChatOpenAI(model="gpt-4o", api_key=api_key.strip(), temperature=0.3)

    task_desc = (
        "You are a meme generator expert. You are given a query and you need to generate a meme for it.\n"
        "1. Go to https://imgflip.com/memetemplates \n"
        "2. Click on the Search bar in the middle and search for ONLY ONE MAIN ACTION VERB (like 'bully', 'laugh', 'cry') in this query: '{0}'\n"
        "3. Click on the 'Search' button search it\n"
        "4. Choose any meme template that metaphorically fits the meme topic: '{0}'\n"
        "   by clicking on the 'Add Caption' button below it\n"
        "5. Write a Top Text (setup/context) and Bottom Text (punchline/outcome) related to '{0}'.\n"
        "6. Check the preview making sure it is funny and a meaningful meme. Adjust text directly if needed. \n"
        "7. Look at the meme and text on it, if it doesnt make sense, PLEASE retry by filling the text boxes with different text. \n"
        "8. Click on the Generate meme button to generate the meme\n"
        "9. Copy the image link and give it as the output\n"
    ).format(query)

    agent = Agent(
        task=task_desc,
        llm=llm,
        max_actions_per_step=5,
        max_failures=25,
        use_vision=(model_choice != "deepseek"),
    )

    history = await agent.run()

    final_result = history.final_result()
    # 正则提取
    url_match = re.search(r"https://imgflip\.com/i/(\w+)", final_result)
    if url_match:
        meme_id = url_match.group(1)
        return f"https://i.imgflip.com/{meme_id}.jpg"
    return None


def main():
    st.title("AI 梗图生成器，基于 BrowserUse ")
    st.info(
        "这个浏览器代理执行浏览器自动化，根据您使用浏览器的输入生成表情。请输入你的梗图主题并描述你想要生成的表情包。"
    )

    with st.sidebar:
        st.markdown('<p class="sidebar-header">⚙️ 模型配置</p>', unsafe_allow_html=True)
        model_choice = st.selectbox(
            "模型类型",
            ["deepseek", "openai"],
            index=0,
            help="选择一个模型用于生成表情包",
        )
        api_key = ""
        if model_choice == "deepseek":
            api_key = st.text_input(
                "DeepSeek API Key",
                type="password",
                help="DeepSeek API Key from https://platform.deepseek.com",
            )
        elif model_choice == "openai":
            api_key = st.text_input(
                "OpenAI API Key",
                type="password",
                help="OpenAI API Key from https://platform.openai.com",
            )

    st.markdown(
        '<p class="header-text">🎨 描述你的梗图主题</p>', unsafe_allow_html=True
    )
    query = st.text_input(
        "梗图主题",
        placeholder="例如：如何用英语表达‘食人族抓住打工人后又放回来了，因为打工人太苦了’",
        label_visibility="collapsed",
    )

    if st.button("Generate Meme 🚀"):
        if not api_key:
            st.warning(f"请提供 {model_choice} API key")
            st.stop()
        if not query:
            st.warning("请输入表情包升成的想法")
            st.stop()

        with st.spinner(f"🧠 {model_choice} 正在生成你的..."):
            try:
                meme_url = asyncio.run(generate_meme(query, model_choice, api_key))

                if meme_url:
                    st.success("✅ 表情包生成成功!")
                    st.image(
                        meme_url,
                        caption="Generated Meme Preview",
                        use_container_width=True,
                    )
                    st.markdown(
                        f"""
                        **Direct Link:** [Open in ImgFlip]({meme_url})  
                        **Embed URL:** `{meme_url}`
                    """
                    )
                else:
                    st.error("❌ 生成失败。请使用不同的提示符再试一次.")

            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("💡 如果使用openai，请确保您的帐户具有gpt-4o访问权限")


if __name__ == "__main__":
    main()
