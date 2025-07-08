import streamlit as st
import pandas as pd
from agno.agent import Agent
from agno.tools.pandas import PandasTools
from agno.models.deepseek import DeepSeek

import os


def main():
    st.set_page_config(page_title="AI 数据分析智能体", layout="wide")
    st.title("📈 AI 数据分析智能体")

    # Sidebar for API Key
    st.sidebar.header("模型配置")
    deepseek_api_key = st.sidebar.text_input(
        "请输入您的DEEPSEEK API Key", type="password"
    )

    # Main content
    uploaded_file = st.file_uploader("上传您的 CSV 或 Excel 文件", type=["csv", "xlsx"])

    if uploaded_file is not None:
        try:
            st.sidebar.info(f"已上传文件: `{uploaded_file.name}`")
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file, engine="openpyxl")

            st.write("数据预览 (前5行):")
            st.dataframe(df.head())

            question = st.text_area("请输入您关于数据的问题:", height=150)

            if st.button("开始分析"):
                if not deepseek_api_key:
                    st.error("请输入您的DEEPSEEK API Key。")
                elif not question:
                    st.error("请输入您的问题。")
                else:
                    with st.spinner("正在分析您的数据，请稍候..."):
                        try:
                            # 为 Agent 设置 API Key
                            os.environ["DEEPSEEK_API_KEY"] = deepseek_api_key

                            # 初始化 Agent - 使用正确的 PandasTools 初始化方式
                            pandas_tools = PandasTools()
                            # 将数据框添加到工具中
                            pandas_tools.dataframes["uploaded_data"] = df

                            agent = Agent(
                                model=DeepSeek(api_key=deepseek_api_key),
                                tools=[pandas_tools],
                                markdown=True,
                                instructions="你是一个数据分析助手，请帮助用户分析数据。",
                                debug_mode=True,
                            )

                            # 构建完整的 prompt
                            prompt = f"请根据名为 'uploaded_data' 的数据框分析并回答以下问题: {question}"

                            # 运行 Agent 并获取回复
                            response = agent.run(prompt)

                            st.success("分析完成!")
                            st.write("分析结果:")
                            st.markdown(response.content)

                        except Exception as e:
                            st.error(f"分析过程中出现错误: {e}")
                            st.info(
                                "请检查您的 API Key 是否正确，以及网络连接是否正常。"
                            )

        except Exception as e:
            st.error(f"读取文件时出错: {e}")


if __name__ == "__main__":
    main()
