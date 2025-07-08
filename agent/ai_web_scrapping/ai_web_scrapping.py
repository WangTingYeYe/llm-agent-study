import streamlit as st
from scrapegraphai.graphs import SmartScraperGraph



st.title("AI 爬虫")
st.caption("使用 ScrapegraphAI 的智能爬虫")

api_key = st.text_input("DeepSeek API Key", type="password", help="DeepSeek API Key")

if api_key:
    model = st.radio("选择模型", ["deepseek-chat", "deepseek-coder"], index=0)
    
    graph_config = {
        "llm": {
            "model": model,
            "temperature": 0,
            "api_key": api_key,
        }
    }

    url = st.text_input("输入URL", placeholder="https://www.baidu.com")
    
    user_propt = st.text_input("输入用户提示", placeholder="请爬取百度首页的标题")
    
    smartScraperGraph =  SmartScraperGraph(
        prompt=user_propt,
        source = url,
        config = graph_config
    )
    
    if st.button("立即爬取！"):
        result = smartScraperGraph.run()
        st.write(result)