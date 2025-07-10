"""
基于 LangChain 的 QA Agent
使用通义千问 LLM 和 DashScope 嵌入模型

功能：
1. 加载本地文档到向量数据库
2. 基于向量数据库进行问答
3. 支持多种向量存储后端（FAISS、Chroma）
"""

import os
import logging
from typing import List, Optional
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS, Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import RetrievalQA
from langchain.chains.question_answering import load_qa_chain

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QAAgent:
    """
    基于 LangChain 的问答智能体
    
    使用通义千问 LLM 和 DashScope 嵌入模型构建的RAG系统
    """
    
    def __init__(self, 
                 api_key: str = None,
                 llm_model: str = "qwen-turbo",
                 embedding_model: str = "text-embedding-v2",
                 vector_store_type: str = "faiss",
                 chunk_size: int = 1000,
                 chunk_overlap: int = 200):
        """
        初始化 QA Agent
        
        Args:
            api_key: DashScope API密钥
            llm_model: 使用的LLM模型名称
            embedding_model: 使用的嵌入模型名称
            vector_store_type: 向量存储类型 ("faiss" 或 "chroma")
            chunk_size: 文档分块大小
            chunk_overlap: 分块重叠大小
        """
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError("请设置 DASHSCOPE_API_KEY 环境变量或提供 api_key 参数")
        
        self.llm_model = llm_model
        self.embedding_model = embedding_model
        self.vector_store_type = vector_store_type.lower()
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # 初始化组件
        self._init_components()
        
        # 向量存储和检索器
        self.vector_store = None
        self.retriever = None
        self.qa_chain = None
        
        logger.info(f"QA Agent 初始化完成 - LLM: {llm_model}, Embedding: {embedding_model}, VectorStore: {vector_store_type}")
    
    def _init_components(self):
        """初始化 LLM、嵌入模型和文本分割器"""
        # 初始化通义千问 LLM
        self.llm = ChatTongyi(
            model_name=self.llm_model,
            dashscope_api_key=self.api_key,
            temperature=0.1,
            streaming=False
        )
        
        # 初始化 DashScope 嵌入模型
        self.embeddings = DashScopeEmbeddings(
            model=self.embedding_model,
            dashscope_api_key=self.api_key
        )
        
        # 初始化文本分割器
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""]
        )
        
        logger.info("LLM、嵌入模型和文本分割器初始化完成")
    
    def load_documents_from_file(self, file_path: str) -> List[Document]:
        """
        从文件加载文档
        
        Args:
            file_path: 文件路径
            
        Returns:
            Document对象列表
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        # 根据文件扩展名选择加载器
        file_extension = Path(file_path).suffix.lower()
        
        if file_extension == '.txt':
            loader = TextLoader(file_path, encoding='utf-8')
        else:
            # 默认使用文本加载器
            loader = TextLoader(file_path, encoding='utf-8')
        
        documents = loader.load()
        logger.info(f"从 {file_path} 加载了 {len(documents)} 个文档")
        
        return documents
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        分割文档为小块
        
        Args:
            documents: 原始文档列表
            
        Returns:
            分割后的文档块列表
        """
        chunks = self.text_splitter.split_documents(documents)
        logger.info(f"文档分割完成，共 {len(chunks)} 个块")
        
        return chunks
    
    def create_vector_store(self, documents: List[Document], persist_directory: str = None) -> None:
        """
        创建向量存储
        
        Args:
            documents: 文档列表
            persist_directory: 持久化目录（仅适用于Chroma）
        """
        if self.vector_store_type == "faiss":
            self.vector_store = FAISS.from_documents(
                documents=documents,
                embedding=self.embeddings
            )
            logger.info("FAISS 向量存储创建完成")
            
        elif self.vector_store_type == "chroma":
            if persist_directory:
                self.vector_store = Chroma.from_documents(
                    documents=documents,
                    embedding=self.embeddings,
                    persist_directory=persist_directory
                )
                self.vector_store.persist()
                logger.info(f"Chroma 向量存储创建完成，持久化到: {persist_directory}")
            else:
                self.vector_store = Chroma.from_documents(
                    documents=documents,
                    embedding=self.embeddings
                )
                logger.info("Chroma 内存向量存储创建完成")
        else:
            raise ValueError(f"不支持的向量存储类型: {self.vector_store_type}")
        
        # 创建检索器
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}
        )
        
        # 创建问答链
        self._create_qa_chain()
    
    def _create_qa_chain(self):
        """创建问答链"""
        # 定义提示模板
        prompt_template = ChatPromptTemplate.from_template("""                                                       
        你是一个乐于助人的QA助手，专门回答用户关于公司产品和服务的问题。
        你的目标是根据从公司知识库中检索到的信息回答。
        上下文信息:
        {context}
        用户问题:
        {question}
        """)
#         prompt_template = ChatPromptTemplate.from_template("""
# 你是一个专业的问答助手。请基于以下提供的上下文信息来回答用户的问题。

# 上下文信息:
# {context}

# 用户问题: {question}

# 请按照以下要求回答:
# 1. 仅基于提供的上下文信息回答问题
# 2. 如果上下文中没有相关信息，请明确说明
# 3. 回答要准确、简洁、有条理
# 4. 如果可能，请引用相关的具体信息

# 回答:
# """)
        
        
        # 创建检索问答链
        self.qa_chain = (
            {
                "context": self.retriever | (lambda docs: "\n\n".join([doc.page_content for doc in docs])),
                "question": RunnablePassthrough()
            }
            | prompt_template
            | self.llm
            | StrOutputParser()
        )
        
        logger.info("问答链创建完成")
    
    def load_and_index_document(self, file_path: str, persist_directory: str = None):
        """
        加载文档并建立索引
        
        Args:
            file_path: 文档文件路径
            persist_directory: 持久化目录（可选）
        """
        logger.info(f"开始处理文档: {file_path}")
        
        # 1. 加载文档
        documents = self.load_documents_from_file(file_path)
        
        # 2. 分割文档
        chunks = self.split_documents(documents)
        
        # 3. 创建向量存储
        self.create_vector_store(chunks, persist_directory)
        
        logger.info("文档加载和索引完成")
    
    def query(self, question: str) -> str:
        """
        基于向量数据库进行问答
        
        Args:
            question: 用户问题
            
        Returns:
            回答结果
        """
        if not self.qa_chain:
            raise ValueError("请先加载文档并建立索引")
        
        try:
            logger.info(f"处理问题: {question}")
            answer = self.qa_chain.invoke(question)
            logger.info("问答完成")
            return answer
        
        except Exception as e:
            logger.error(f"问答过程中出错: {e}")
            return f"抱歉，处理您的问题时出现错误: {str(e)}"
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """
        执行相似性搜索
        
        Args:
            query: 查询文本
            k: 返回的文档数量
            
        Returns:
            相关文档列表
        """
        if not self.vector_store:
            raise ValueError("请先加载文档并建立索引")
        
        docs = self.vector_store.similarity_search(query, k=k)
        logger.info(f"相似性搜索完成，找到 {len(docs)} 个相关文档")
        
        return docs
    
    def get_vector_store_info(self) -> dict:
        """
        获取向量存储信息
        
        Returns:
            向量存储信息字典
        """
        if not self.vector_store:
            return {"status": "未初始化"}
        
        info = {
            "type": self.vector_store_type,
            "embedding_model": self.embedding_model,
            "llm_model": self.llm_model,
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap
        }
        
        # 尝试获取文档数量（如果支持）
        try:
            if hasattr(self.vector_store, 'similarity_search'):
                # 通过搜索测试来估算是否有数据
                test_results = self.vector_store.similarity_search("test", k=1)
                info["has_documents"] = len(test_results) > 0
        except:
            info["has_documents"] = "未知"
        
        return info


def main():
    """
    主函数 - 演示 QA Agent 的使用
    """
    # 检查环境变量
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        logger.error("请设置 DASHSCOPE_API_KEY 环境变量")
        return
    
    # 文档路径
    doc_path = "company_information.txt"
    
    try:
        # 创建 QA Agent
        qa_agent = QAAgent(
            api_key=api_key,
            llm_model="qwen-turbo",
            embedding_model="text-embedding-v2",
            vector_store_type="faiss"  # 可选 "chroma"
        )
        
        # 加载文档并建立索引
        qa_agent.load_and_index_document(doc_path)
        
        # 显示向量存储信息
        info = qa_agent.get_vector_store_info()
        logger.info(f"向量存储信息: {info}")
        
        # 示例问答
        questions = [
            "菜鸟网络是什么？",
            "菜鸟网络的核心价值观是什么？",
            "菜鸟的智慧仓储有什么特点？",
            "菜鸟在绿色物流方面做了哪些工作？",
            "为什么选择菜鸟网络？"
        ]
        
        print("\n" + "="*60)
        print("🤖 菜鸟网络 QA Agent 演示")
        print("="*60)
        
        for i, question in enumerate(questions, 1):
            print(f"\n📋 问题 {i}: {question}")
            print("-" * 50)
            
            answer = qa_agent.query(question)
            print(f"💡 回答: {answer}")
            
            # 显示相关文档片段
            print("\n📄 相关文档片段:")
            docs = qa_agent.similarity_search(question, k=2)
            for j, doc in enumerate(docs, 1):
                content_preview = doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
                print(f"   {j}. {content_preview}")
            
            print("\n" + "="*60)
        
        # 交互式问答
        print("\n🎯 进入交互模式 (输入 'quit' 退出):")
        while True:
            user_question = input("\n请输入您的问题: ").strip()
            
            if user_question.lower() in ['quit', 'exit', '退出', 'q']:
                print("感谢使用！再见！")
                break
            
            if not user_question:
                continue
            
            print(f"\n🤖 回答: {qa_agent.query(user_question)}")
    
    except Exception as e:
        logger.error(f"运行过程中出错: {e}")


if __name__ == "__main__":
    main()
