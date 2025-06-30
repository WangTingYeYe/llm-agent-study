import streamlit as st
import pandas as pd
import os
import tempfile
import shutil
from pathlib import Path
from agno.agent import Agent
from agno.tools.duckdb import DuckDbTools
from agno.models.deepseek import DeepSeek


def save_uploaded_file_to_temp(uploaded_file):
    """将上传的文件保存到临时目录"""
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()

    # 构建文件路径
    file_path = os.path.join(temp_dir, uploaded_file.name)

    # 保存文件
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path, temp_dir


def cleanup_temp_dir(temp_dir):
    """清理临时目录"""
    try:
        shutil.rmtree(temp_dir)
    except Exception as e:
        st.warning(f"清理临时文件时出现警告: {e}")


def main():
    st.set_page_config(page_title="AI 数据分析智能体 (DuckDB版)", layout="wide")
    st.title("📈 AI 数据分析智能体 (DuckDB SQL版)")

    st.info("💡 此版本使用 DuckDB 进行数据分析，支持复杂的 SQL 查询操作")

    # Sidebar for API Key
    st.sidebar.header("模型配置")
    deepseek_api_key = st.sidebar.text_input(
        "请输入您的 DEEPSEEK API Key", type="password"
    )

    # Main content
    uploaded_file = st.file_uploader(
        "上传您的 CSV 或 Excel 文件",
        type=["csv", "xlsx", "xls"],
        help="支持 CSV 和 Excel 格式文件",
    )

    if uploaded_file is not None:
        temp_dir = None
        try:
            st.sidebar.info(f"已上传文件: `{uploaded_file.name}`")

            # 保存文件到临时目录
            with st.spinner("正在保存文件到临时目录..."):
                file_path, temp_dir = save_uploaded_file_to_temp(uploaded_file)
                st.sidebar.success(f"文件已保存到: `{file_path}`")

            # 读取并预览数据
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path, engine="openpyxl")

            st.write("数据预览 (前5行):")
            st.dataframe(df.head())

            # 显示数据基本信息
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("总行数", len(df))
            with col2:
                st.metric("总列数", len(df.columns))
            with col3:
                st.metric("文件大小", f"{uploaded_file.size / 1024:.1f} KB")

            # 显示列信息
            with st.expander("📊 查看列信息"):
                st.write("列名和数据类型:")
                column_info = pd.DataFrame(
                    {
                        "列名": df.columns,
                        "数据类型": df.dtypes.astype(str),
                        "非空值数量": df.count(),
                        "缺失值数量": df.isnull().sum(),
                    }
                )
                st.dataframe(column_info)

            # SQL 查询建议
            st.write("### 💡 SQL 查询建议")
            st.code(
                f"""
                    -- 基础查询示例 (表名: '{Path(uploaded_file.name).stem}')
                    SELECT * FROM '{Path(uploaded_file.name).stem}' LIMIT 10;

                    -- 统计分析示例
                    SELECT COUNT(*) as total_rows FROM '{Path(uploaded_file.name).stem}';

                    -- 按列分组统计 (请根据实际列名修改)
                    SELECT column_name, COUNT(*) 
                    FROM '{Path(uploaded_file.name).stem}' 
                    GROUP BY column_name 
                    ORDER BY COUNT(*) DESC; 
                """,
                language="sql",
            )

            question = st.text_area(
                "请输入您的数据分析问题 (支持自然语言或SQL查询):",
                height=150,
                placeholder="例如: 帮我分析这个数据集的基本统计信息\n或者: 查询销售额最高的前10个产品",
            )

            if st.button("🚀 开始分析", type="primary"):
                if not deepseek_api_key:
                    st.error("❌ 请输入您的 DEEPSEEK API Key。")
                elif not question:
                    st.error("❌ 请输入您的问题。")
                else:
                    with st.spinner("🔍 正在使用 DuckDB 分析您的数据，请稍候..."):
                        try:
                            # 为 Agent 设置 API Key
                            os.environ["DEEPSEEK_API_KEY"] = deepseek_api_key

                            # 初始化 DuckDbTools
                            duckdb_tools = DuckDbTools()

                            # 获取表名 (使用文件名作为表名，去除扩展名)
                            table_name = Path(uploaded_file.name).stem

                            agent = Agent(
                                model=DeepSeek(api_key=deepseek_api_key),
                                tools=[duckdb_tools],
                                markdown=True,
                                instructions=f"""你是一个专业的数据分析师，擅长使用 SQL 查询分析数据。

用户上传了一个名为 '{uploaded_file.name}' 的文件，文件路径为: {file_path}
该文件已经可以通过 DuckDB 访问，表名为: '{table_name}'

请根据用户的问题进行数据分析：
1. 如果用户问的是自然语言问题，请先理解用户需求，然后编写合适的SQL查询
2. 如果用户直接提供SQL查询，请执行并分析结果
3. 请提供清晰的分析结果和见解
4. 如果需要，可以提供多个SQL查询来全面分析数据

文件列信息：
{df.columns.tolist()}

数据类型：
{df.dtypes.to_dict()}
""",
                                debug_mode=True,
                            )

                            # 构建完整的 prompt
                            prompt = f"""
请分析位于 '{file_path}' 的数据文件，表名为 '{table_name}'。

用户问题: {question}

请使用 DuckDB SQL 查询来分析数据并回答用户的问题。
"""

                            # 运行 Agent 并获取回复
                            response = agent.run(prompt)

                            st.success("✅ 分析完成!")
                            st.write("### 📋 分析结果:")

                            # 检查 response 的类型并正确显示内容
                            if hasattr(response, "content"):
                                st.markdown(response.content)
                            else:
                                st.markdown(str(response))

                        except Exception as e:
                            st.error(f"❌ 分析过程中出现错误: {e}")
                            st.info(
                                "💡 请检查您的 API Key 是否正确，以及网络连接是否正常。"
                            )
                            # 显示详细错误信息以便调试
                            with st.expander("🔍 查看详细错误信息"):
                                st.code(str(e))

        except Exception as e:
            st.error(f"❌ 读取文件时出错: {e}")

        finally:
            # 清理临时文件
            if temp_dir and os.path.exists(temp_dir):
                cleanup_temp_dir(temp_dir)

    else:
        # 显示使用说明
        st.markdown(
            """
        ### 📖 使用说明
        
        1. **上传文件**: 点击上方的文件上传区域，选择您的 CSV 或 Excel 文件
        2. **输入 API Key**: 在左侧边栏输入您的 DEEPSEEK API Key
        3. **查看数据**: 上传后可以预览数据的基本信息和结构
        4. **提出问题**: 在文本框中输入您的分析需求
        5. **获取结果**: 点击"开始分析"按钮，AI 将使用 SQL 查询分析您的数据
        
        ### 🔧 支持的功能
        
        - ✅ CSV 和 Excel 文件上传
        - ✅ 自动数据类型识别
        - ✅ SQL 查询执行
        - ✅ 自然语言转 SQL
        - ✅ 数据统计分析
        - ✅ 复杂查询支持
        
        ### 💡 查询示例
        
        - "帮我分析这个数据集的基本统计信息"
        - "找出销售额最高的前10个产品"
        - "按月份统计销售趋势"
        - "计算各类别的平均值和总和"
        """
        )


if __name__ == "__main__":
    main()
