#!/usr/bin/env python3
"""
基于Streamlit的RAG应用程序
使用阿里百炼 DashScope API 和 LangChain 框架
支持用户上传PDF文档和自定义API密钥
"""

import os
import tempfile
import logging
from typing import List, Optional
from pathlib import Path
import time

# 第三方库导入
try:
    import streamlit as st
    import dashscope
    import re
    import unicodedata
    from langchain_community.chat_models import ChatTongyi
    from langchain_community.embeddings import DashScopeEmbeddings
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_community.vectorstores import Chroma
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.schema import Document
    from langchain.chains import RetrievalQA
    from langchain.prompts import PromptTemplate
    import numpy as np
except ImportError as e:
    st.error(f"请安装所需的依赖包: {e}")
    st.code("pip install streamlit dashscope langchain langchain-community pypdf chromadb")
    st.stop()

# 配置页面
st.set_page_config(
    page_title="RAG智能问答助手",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 配置日志 - 减少第三方库的噪音日志
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 设置特定库的日志级别
logging.getLogger('urllib3').setLevel(logging.ERROR)
logging.getLogger('requests').setLevel(logging.ERROR)
logging.getLogger('backoff').setLevel(logging.ERROR)
logging.getLogger('langchain').setLevel(logging.ERROR)
logging.getLogger('posthog').setLevel(logging.ERROR)
logging.getLogger('httpx').setLevel(logging.ERROR)
logging.getLogger('chromadb').setLevel(logging.ERROR)

# 禁用PostHog遥测数据收集
os.environ['POSTHOG_DISABLED'] = '1'
os.environ['ANONYMIZED_TELEMETRY'] = 'false'
os.environ['CHROMA_TELEMETRY'] = 'false'
os.environ['LANGCHAIN_TRACING_V2'] = 'false'

# 应用日志
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PDFPreprocessor:
    """PDF文档预处理器"""
    
    def __init__(self):
        # 常见的无意义字符和模式
        self.noise_patterns = [
            r'\f',  # 换页符
            r'\x0c',  # 换页符
            r'[\u200b-\u200d\ufeff]',  # 零宽字符
            r'\n\s*\n\s*\n+',  # 多个连续空行
        ]
        
        # 页眉页脚常见模式
        self.header_footer_patterns = [
            r'^\d+\s*$',  # 单独的页码
            r'^第\s*\d+\s*页\s*$',  # 中文页码
            r'^Page\s+\d+.*$',  # 英文页码
            r'^\s*\d+\s*/\s*\d+\s*$',  # 页码格式 "1/10"
        ]
    
    def clean_text(self, text: str) -> str:
        """清理文本内容"""
        if not text or not isinstance(text, str):
            return ""
        
        try:
            # 1. Unicode标准化
            text = unicodedata.normalize('NFKC', text)
            
            # 2. 移除噪声字符
            for pattern in self.noise_patterns:
                text = re.sub(pattern, ' ', text)
            
            # 3. 处理连字符换行
            text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)
            
            # 4. 合并被分割的单词（中文）
            text = re.sub(r'([\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])', r'\1', text)
            
            # 5. 标准化空白字符
            text = re.sub(r'[ \t]+', ' ', text)  # 多个空格/制表符合并为一个空格
            text = re.sub(r'\n[ \t]*\n', '\n\n', text)  # 清理空行中的空格
            
            # 6. 移除行首行尾空格
            lines = text.split('\n')
            lines = [line.strip() for line in lines]
            text = '\n'.join(lines)
            
            # 7. 移除多余的空行
            text = re.sub(r'\n{3,}', '\n\n', text)
            
            return text.strip()
        except Exception as e:
            logger.warning(f"文本清理失败: {e}")
            return text
    
    def remove_headers_footers(self, text: str) -> str:
        """移除页眉页脚"""
        try:
            lines = text.split('\n')
            cleaned_lines = []
            
            for line in lines:
                line = line.strip()
                if not line:
                    cleaned_lines.append(line)
                    continue
                
                # 检查是否为页眉页脚
                is_header_footer = False
                for pattern in self.header_footer_patterns:
                    if re.match(pattern, line, re.IGNORECASE):
                        is_header_footer = True
                        break
                
                if not is_header_footer:
                    cleaned_lines.append(line)
            
            return '\n'.join(cleaned_lines)
        except Exception as e:
            logger.warning(f"页眉页脚移除失败: {e}")
            return text
    
    def enhance_structure(self, text: str) -> str:
        """增强文档结构"""
        try:
            lines = text.split('\n')
            enhanced_lines = []
            
            for line in lines:
                line = line.strip()
                if not line:
                    enhanced_lines.append(line)
                    continue
                
                # 检测标题（全大写、较短、或特定模式）
                if (len(line) < 100 and 
                    (line.isupper() or 
                     re.match(r'^[一二三四五六七八九十\d]+[、\.]\s*', line) or
                     re.match(r'^第[一二三四五六七八九十\d]+[章节部分]\s*', line) or
                     re.match(r'^\d+\.\d*\s+', line))):
                    enhanced_lines.append(f"\n## {line}\n")
                else:
                    enhanced_lines.append(line)
            
            return '\n'.join(enhanced_lines)
        except Exception as e:
            logger.warning(f"结构增强失败: {e}")
            return text
    
    def preprocess_document(self, document: Document) -> Document:
        """预处理单个文档"""
        try:
            content = document.page_content
            
            # 执行预处理步骤
            content = self.clean_text(content)
            content = self.remove_headers_footers(content)
            content = self.enhance_structure(content)
            
            # 如果处理后内容为空或过短，返回原文档
            if not content or len(content.strip()) < 50:
                return document
            
            # 创建新的文档对象
            processed_doc = Document(
                page_content=content,
                metadata={
                    **document.metadata,
                    'preprocessed': True,
                    'original_length': len(document.page_content),
                    'processed_length': len(content)
                }
            )
            
            return processed_doc
        except Exception as e:
            logger.warning(f"文档预处理失败: {e}")
            return document
    
    def preprocess_documents(self, documents: List[Document]) -> List[Document]:
        """预处理文档列表"""
        processed_docs = []
        
        for i, doc in enumerate(documents):
            try:
                processed_doc = self.preprocess_document(doc)
                processed_docs.append(processed_doc)
            except Exception as e:
                logger.warning(f"预处理第{i+1}个文档时出错: {e}")
                # 如果预处理失败，使用原文档
                processed_docs.append(doc)
        
        return processed_docs


class StreamlitRAGApp:
    """基于Streamlit的RAG应用程序"""
    
    def __init__(self, 
                 embedding_model: str = "text-embedding-v2",
                 llm_model: str = "qwen-turbo"):
        """
        初始化RAG应用
        
        Args:
            embedding_model: 嵌入模型名称
            llm_model: 大语言模型名称
        """
        self.embedding_model = embedding_model
        self.llm_model = llm_model
        
        # 初始化模型
        self.embeddings = None
        self.llm = None
        self.vectorstore = None
        self.qa_chain = None
        
        # 初始化预处理器
        self.preprocessor = PDFPreprocessor()
        
    def setup_models(self):
        """设置模型"""
        if self.embeddings is None:
            # 使用官方的DashScopeEmbeddings
            self.embeddings = DashScopeEmbeddings(
                model=self.embedding_model
            )
        if self.llm is None:
            # 使用官方的ChatTongyi
            self.llm = ChatTongyi(
                model_name=self.llm_model,
                temperature=0.7,
                max_tokens=1000
            )
    
    def load_and_process_pdf(self, pdf_file, enable_preprocessing: bool = True) -> List[Document]:
        """加载并处理PDF文档"""
        # 创建临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(pdf_file.read())
            tmp_file_path = tmp_file.name
        
        try:
            # 加载PDF
            loader = PyPDFLoader(tmp_file_path)
            documents = loader.load()
            
            st.success(f"✅ 成功加载PDF，共 {len(documents)} 页")
            
            # 根据配置决定是否预处理
            if enable_preprocessing:
                st.info("🔧 正在预处理PDF内容...")
                processed_documents = self.preprocessor.preprocess_documents(documents)
                
                # 显示预处理统计
                original_total = sum(len(doc.page_content) for doc in documents)
                processed_total = sum(len(doc.page_content) for doc in processed_documents)
                reduction_percent = (1 - processed_total / original_total) * 100 if original_total > 0 else 0
                
                st.info(f"📊 预处理完成，内容压缩了 {reduction_percent:.1f}%")
            else:
                processed_documents = documents
                st.info("⚠️ 跳过预处理，使用原始PDF内容")
            
            # 文本分割
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,        # 每个块的大小
                chunk_overlap=100,      # 块之间的重叠
                length_function=len,
                separators=["\n\n", "\n", " ", ""]
            )
            
            splits = text_splitter.split_documents(processed_documents)
            st.info(f"📄 文档分割完成，共 {len(splits)} 个文本块")
            
            return splits
            
        finally:
            # 清理临时文件
            os.unlink(tmp_file_path)
    
    def create_vectorstore(self, documents: List[Document]):
        """创建向量数据库"""
        # 显示进度条
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text("🔄 正在创建向量数据库...")
            progress_bar.progress(0.5)
            
            # 使用内存向量数据库
            self.vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings
            )
            
            progress_bar.progress(1.0)
            status_text.text("✅ 向量数据库创建完成")
            
        finally:
            # 清理进度显示
            progress_bar.empty()
            status_text.empty()
        
        st.success("✅ 向量数据库创建完成")
    
    def setup_qa_chain(self):
        """设置问答链"""
        if self.vectorstore is None:
            raise ValueError("向量数据库未初始化")
        
        # 创建检索器
        retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}  # 返回最相似的3个文档块
        )
        
        # 定义提示模板
        prompt_template = """请基于以下上下文信息回答问题。如果上下文中没有相关信息，请如实说明。

上下文信息:
{context}

问题: {question}

请用中文回答:"""
        
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        # 创建问答链
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs={"prompt": prompt},
            return_source_documents=True
        )
        
        st.success("✅ 问答链设置完成")
    
    def initialize_with_pdf(self, pdf_file, enable_preprocessing: bool = True):
        """使用PDF文件初始化RAG系统"""
        try:
            # 设置模型
            self.setup_models()
            
            # 加载和处理PDF
            documents = self.load_and_process_pdf(pdf_file, enable_preprocessing)
            
            # 创建向量数据库
            self.create_vectorstore(documents)
            
            # 设置问答链
            self.setup_qa_chain()
            
            return True
            
        except Exception as e:
            st.error(f"❌ 初始化失败: {e}")
            return False
    
    def query(self, question: str) -> dict:
        """查询问题"""
        if self.qa_chain is None:
            raise ValueError("问答链未初始化，请先上传PDF文档")
        
        try:
            with st.spinner("🔍 正在搜索相关信息..."):
                # 使用新的invoke方法替代deprecated的__call__
                result = self.qa_chain.invoke({"query": question})
            
            return {
                "question": question,
                "answer": result["result"],
                "source_documents": [doc.page_content for doc in result["source_documents"]]
            }
        except Exception as e:
            logger.error(f"查询时出错: {e}")
            return {
                "question": question,
                "answer": "抱歉，处理您的问题时出现错误。",
                "source_documents": []
            }


def setup_sidebar():
    """设置侧边栏"""
    st.sidebar.title("🛠️ 配置设置")
    
    # API密钥配置
    st.sidebar.header("🔑 API密钥设置")
    
    # 从环境变量获取默认值
    default_api_key = os.getenv("DASHSCOPE_API_KEY", "")
    
    api_key = st.sidebar.text_input(
        "DashScope API密钥",
        value=default_api_key,
        type="password",
        help="请在阿里云百炼控制台获取您的API密钥"
    )
    
    if api_key:
        # 设置环境变量，ChatTongyi会自动读取
        os.environ["DASHSCOPE_API_KEY"] = api_key
        dashscope.api_key = api_key
        st.sidebar.success("✅ API密钥已设置")
    else:
        st.sidebar.warning("⚠️ 请设置API密钥")
    
    # 模型配置
    st.sidebar.header("🤖 模型配置")
    
    embedding_model = st.sidebar.selectbox(
        "Embedding模型",
        ["text-embedding-v1", "text-embedding-v2"],
        index=1,
        help="选择用于文档向量化的模型"
    )
    
    llm_model = st.sidebar.selectbox(
        "LLM模型",
        ["qwen-turbo", "qwen-plus", "qwen-max", "qwen-max-longcontext"],
        index=0,
        help="选择用于文本生成的模型"
    )
    
    # 高级设置
    st.sidebar.header("⚙️ 高级设置")
    
    # 预处理选项
    st.sidebar.subheader("📝 文档预处理")
    enable_preprocessing = st.sidebar.checkbox(
        "启用PDF预处理",
        value=True,
        help="自动清理文本、移除页眉页脚、增强文档结构"
    )
    
    if enable_preprocessing:
        st.sidebar.caption("✅ 将自动执行：文本清理、页眉页脚移除、结构优化")
    else:
        st.sidebar.caption("⚠️ 原始PDF内容可能包含噪音")
    
    # 分割参数
    st.sidebar.subheader("✂️ 文档分割")
    chunk_size = st.sidebar.slider(
        "文本分割块大小",
        min_value=500,
        max_value=2000,
        value=1000,
        step=100,
        help="控制文档分割的块大小"
    )
    
    chunk_overlap = st.sidebar.slider(
        "文本块重叠大小",
        min_value=0,
        max_value=200,
        value=100,
        step=20,
        help="控制文档块之间的重叠"
    )
    
    # 检索参数
    st.sidebar.subheader("🔍 检索设置")
    k_docs = st.sidebar.slider(
        "检索文档数量",
        min_value=1,
        max_value=10,
        value=3,
        help="检索时返回的相关文档数量"
    )
    
    # 帮助信息
    st.sidebar.header("ℹ️ 帮助信息")
    
    with st.sidebar.expander("如何获取API密钥"):
        st.markdown("""
        1. 访问 [阿里云百炼控制台](https://dashscope.console.aliyun.com/)
        2. 注册/登录阿里云账号
        3. 开通百炼服务
        4. 创建API密钥
        5. 将密钥粘贴到左侧输入框
        """)
    
    with st.sidebar.expander("支持的文件格式"):
        st.markdown("""
        - PDF文档 (.pdf)
        - 最大文件大小: 200MB
        - 支持中英文文档
        """)
    
    return {
        "api_key": api_key,
        "embedding_model": embedding_model,
        "llm_model": llm_model,
        "enable_preprocessing": enable_preprocessing,
        "chunk_size": chunk_size,
        "chunk_overlap": chunk_overlap,
        "k_docs": k_docs
    }


def main():
    """主函数"""
    st.title("🤖 RAG智能问答助手")
    st.markdown("基于阿里百炼和LangChain的文档问答系统")
    
    # 设置侧边栏
    config = setup_sidebar()
    
    # 检查API密钥
    if not config["api_key"]:
        st.warning("⚠️ 请在左侧设置您的DashScope API密钥")
        st.info("💡 您可以在 [阿里云百炼控制台](https://dashscope.console.aliyun.com/) 获取API密钥")
        return
    
    # 初始化RAG应用
    if "rag_app" not in st.session_state:
        st.session_state.rag_app = StreamlitRAGApp(
            embedding_model=config["embedding_model"],
            llm_model=config["llm_model"]
        )
    
    # 文件上传区域
    st.header("📁 文档上传")
    
    uploaded_file = st.file_uploader(
        "选择PDF文档",
        type=["pdf"],
        help="请上传您要分析的PDF文档"
    )
    
    if uploaded_file is not None:
        # 显示文件信息
        st.info(f"📄 已选择文件: {uploaded_file.name} ({uploaded_file.size / 1024 / 1024:.2f} MB)")
        
        # 处理文档按钮
        if st.button("🚀 处理文档", type="primary"):
            success = st.session_state.rag_app.initialize_with_pdf(
                uploaded_file, 
                enable_preprocessing=config["enable_preprocessing"]
            )
            if success:
                st.session_state.document_processed = True
                st.balloons()
    
    # 问答区域
    if "document_processed" in st.session_state and st.session_state.document_processed:
        st.header("💬 智能问答")
        
        # 预设问题
        st.subheader("🔍 快速开始")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📋 文档摘要"):
                st.session_state.current_question = "请总结这个文档的主要内容"
        
        with col2:
            if st.button("🔑 关键信息"):
                st.session_state.current_question = "这个文档中最重要的信息是什么？"
        
        with col3:
            if st.button("📊 主要观点"):
                st.session_state.current_question = "文档中提到了哪些主要观点？"
        
        # 问题输入
        question = st.text_input(
            "请输入您的问题:",
            value=st.session_state.get("current_question", ""),
            placeholder="例如：这个文档讲了什么？"
        )
        
        if st.button("🔍 提问", type="primary") and question:
            # 执行查询
            result = st.session_state.rag_app.query(question)
            
            # 添加到聊天历史
            st.session_state.chat_history.append((question, result["answer"]))
            
            # 显示结果
            st.subheader("💡 回答")
            st.write(result["answer"])
            
            # 显示相关文档片段
            if result["source_documents"]:
                st.subheader("📚 相关文档片段")
                for i, doc in enumerate(result["source_documents"], 1):
                    with st.expander(f"文档片段 {i}"):
                        st.text(doc)
            
            # 清空当前问题
            if "current_question" in st.session_state:
                del st.session_state.current_question
    
    else:
        st.info("👆 请先上传PDF文档并点击'处理文档'按钮")
    
    # 聊天历史
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # 显示聊天历史
    if st.session_state.chat_history:
        st.header("💭 聊天历史")
        for i, (q, a) in enumerate(st.session_state.chat_history):
            with st.expander(f"问题 {i+1}: {q[:50]}..."):
                st.write(f"**问题:** {q}")
                st.write(f"**回答:** {a}")
    
    # 页脚
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p>🚀 由阿里百炼 + LangChain + Streamlit 驱动</p>
            <p>📧 如有问题，请联系技术支持</p>
        </div>
        """, 
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main() 