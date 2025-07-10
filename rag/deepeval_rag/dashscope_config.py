"""
百炼（DashScope）API配置文件
直接使用通义千问SDK进行配置和模型封装
支持自定义LLM和嵌入模型
"""

import os
import json
from typing import List, Optional, Dict, Any
import logging

from deepeval.models.base_model import DeepEvalBaseLLM
from deepeval.models import DeepEvalBaseEmbeddingModel
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings

logger = logging.getLogger(__name__)

class DashScopeModel(DeepEvalBaseLLM):
    """
    直接使用通义千问SDK的模型类
    避免OpenAI兼容接口的限制
    """
    
    def __init__(self, 
                 model_name: str = "qwen-turbo",
                 api_key: str = None,
                 temperature: float = 0.0,
                 max_tokens: Optional[int] = None,
                 timeout: int = 30):
        """
        初始化通义千问模型
        
        Args:
            model_name: 模型名称，可选值包括：
                - qwen-turbo (推荐，快速响应)
                - qwen-plus (平衡性能)
                - qwen-max (最强性能)
                - qwen-max-longcontext (长文本)
                - qwen2.5-72b-instruct
                - qwen2.5-32b-instruct
                - qwen2.5-14b-instruct
                - qwen2.5-7b-instruct
            api_key: 通义千问API密钥
            temperature: 温度参数
            max_tokens: 最大token数
            timeout: 超时时间
        """
        self.model_name = model_name
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout
        
        if not self.api_key:
            raise ValueError("通义千问API密钥未提供，请设置api_key参数或DASHSCOPE_API_KEY环境变量")
        
        logger.info(f"初始化通义千问模型: {model_name}")
        
    def load_model(self):
        """加载通义千问模型"""
        model_kwargs = {
            "model_name": self.model_name,
            "dashscope_api_key": self.api_key,
            "temperature": self.temperature,
            "streaming": False,  # 确保非流式调用
        }
        
        if self.max_tokens:
            model_kwargs["max_tokens"] = self.max_tokens
            
        return ChatTongyi(**model_kwargs)
    
    def _parse_response_with_schema(self, response_text: str, schema: Optional[Any] = None):
        """解析响应并尝试匹配schema"""
        if not schema:
            return response_text
        
        try:
            # 尝试从响应中提取JSON
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                json_str = response_text[json_start:json_end].strip()
            elif "{" in response_text and "}" in response_text:
                json_start = response_text.find("{")
                json_end = response_text.rfind("}") + 1
                json_str = response_text[json_start:json_end]
            else:
                json_str = response_text
            
            # 尝试解析JSON
            try:
                parsed_json = json.loads(json_str)
                
                # 如果schema有特定的结构，尝试创建相应的对象
                if hasattr(schema, '__annotations__'):
                    # 这是一个dataclass或pydantic模型
                    return schema(**parsed_json)
                else:
                    # 创建一个简单的对象来包装数据
                    class SimpleObject:
                        def __init__(self, **kwargs):
                            for k, v in kwargs.items():
                                setattr(self, k, v)
                    
                    return SimpleObject(**parsed_json)
                    
            except json.JSONDecodeError:
                # 如果JSON解析失败，返回原始文本
                logger.warning(f"无法解析JSON响应: {json_str}")
                return response_text
                
        except Exception as e:
            logger.warning(f"解析schema响应时出错: {e}")
            return response_text
    
    def generate(self, prompt: str, schema: Optional[Any] = None) -> str:
        """生成响应"""
        try:
            chat_model = self.load_model()
            
            # 如果有schema参数，修改prompt以请求JSON格式
            if schema:
                if hasattr(schema, '__annotations__'):
                    # 获取schema的字段信息
                    fields = schema.__annotations__
                    json_format = {field: f"<{field}_value>" for field in fields}
                    prompt = f"{prompt}\n\n请以JSON格式回答，格式如下：\n{json.dumps(json_format, indent=2, ensure_ascii=False)}"
                else:
                    prompt = f"{prompt}\n\n请以JSON格式回答。"
            
            response = chat_model.invoke(prompt)
            
            # 处理schema响应
            if schema:
                return self._parse_response_with_schema(response.content, schema)
            
            return response.content
        except Exception as e:
            logger.error(f"通义千问模型生成失败: {e}")
            raise
    
    async def a_generate(self, prompt: str, schema: Optional[Any] = None) -> str:
        """异步生成响应"""
        try:
            chat_model = self.load_model()
            
            # 如果有schema参数，修改prompt以请求JSON格式
            if schema:
                if hasattr(schema, '__annotations__'):
                    # 获取schema的字段信息
                    fields = schema.__annotations__
                    json_format = {field: f"<{field}_value>" for field in fields}
                    prompt = f"{prompt}\n\n请以JSON格式回答，格式如下：\n{json.dumps(json_format, indent=2, ensure_ascii=False)}"
                else:
                    prompt = f"{prompt}\n\n请以JSON格式回答。"
            
            response = await chat_model.ainvoke(prompt)
            
            # 处理schema响应
            if schema:
                return self._parse_response_with_schema(response.content, schema)
            
            return response.content
        except Exception as e:
            logger.error(f"通义千问模型异步生成失败: {e}")
            raise
    
    def get_model_name(self) -> str:
        """获取模型名称"""
        return self.model_name
    
    def test_connection(self) -> bool:
        """测试通义千问模型连接"""
        try:
            test_response = self.generate("你好")
            logger.info("通义千问模型连接测试成功")
            return True
        except Exception as e:
            logger.error(f"通义千问模型连接测试失败: {e}")
            return False


class DashScopeEmbeddingModel(DeepEvalBaseEmbeddingModel):
    """
    DashScope自定义嵌入模型类
    用于DeepEval的synthetic data generation和RAG评估
    """
    
    def __init__(self, 
                 model_name: str = "text-embedding-v1",
                 api_key: str = None):
        """
        初始化DashScope嵌入模型
        
        Args:
            model_name: 嵌入模型名称，可选值包括：
                - text-embedding-v1 (通用文本嵌入模型)
                - text-embedding-v2 (更新版本)
                - text-embedding-async-v1 (异步版本)
                - text-embedding-async-v2 (异步更新版本)
            api_key: DashScope API密钥
        """
        self.model_name = model_name
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        
        if not self.api_key:
            raise ValueError("DashScope API密钥未提供，请设置api_key参数或DASHSCOPE_API_KEY环境变量")
        
        logger.info(f"初始化DashScope嵌入模型: {model_name}")
    
    def load_model(self):
        """加载DashScope嵌入模型"""
        return DashScopeEmbeddings(
            model=self.model_name,
            dashscope_api_key=self.api_key
        )
    
    def embed_text(self, text: str) -> List[float]:
        """
        嵌入单个文本
        
        Args:
            text: 要嵌入的文本
            
        Returns:
            文本的向量表示
        """
        try:
            embedding_model = self.load_model()
            return embedding_model.embed_query(text)
        except Exception as e:
            logger.error(f"DashScope文本嵌入失败: {e}")
            raise
    
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        嵌入多个文本
        
        Args:
            texts: 要嵌入的文本列表
            
        Returns:
            文本列表的向量表示列表
        """
        try:
            embedding_model = self.load_model()
            return embedding_model.embed_documents(texts)
        except Exception as e:
            logger.error(f"DashScope批量文本嵌入失败: {e}")
            raise
    
    async def a_embed_text(self, text: str) -> List[float]:
        """
        异步嵌入单个文本
        
        Args:
            text: 要嵌入的文本
            
        Returns:
            文本的向量表示
        """
        try:
            embedding_model = self.load_model()
            return await embedding_model.aembed_query(text)
        except Exception as e:
            logger.error(f"DashScope异步文本嵌入失败: {e}")
            # 如果异步版本不可用，回退到同步版本
            return self.embed_text(text)
    
    async def a_embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        异步嵌入多个文本
        
        Args:
            texts: 要嵌入的文本列表
            
        Returns:
            文本列表的向量表示列表
        """
        try:
            embedding_model = self.load_model()
            return await embedding_model.aembed_documents(texts)
        except Exception as e:
            logger.error(f"DashScope异步批量文本嵌入失败: {e}")
            # 如果异步版本不可用，回退到同步版本
            return self.embed_texts(texts)
    
    def get_model_name(self) -> str:
        """获取嵌入模型名称"""
        return f"DashScope {self.model_name}"
    
    def test_connection(self) -> bool:
        """测试DashScope嵌入模型连接"""
        try:
            test_vector = self.embed_text("测试连接")
            logger.info("DashScope嵌入模型连接测试成功")
            return True
        except Exception as e:
            logger.error(f"DashScope嵌入模型连接测试失败: {e}")
            return False


# 预定义的通义千问模型配置
TONGYI_MODELS = {
    "qwen-turbo": "通义千问Turbo模型（推荐，快速响应）",
    "qwen-plus": "通义千问Plus模型（平衡性能）", 
    "qwen-max": "通义千问Max模型（最强性能）",
    "qwen-max-longcontext": "通义千问Max长文本模型",
    "qwen2.5-72b-instruct": "通义千问2.5-72B指令模型",
    "qwen2.5-32b-instruct": "通义千问2.5-32B指令模型",
    "qwen2.5-14b-instruct": "通义千问2.5-14B指令模型",
    "qwen2.5-7b-instruct": "通义千问2.5-7B指令模型",
    "qwen2.5-3b-instruct": "通义千问2.5-3B指令模型",
    "qwen2.5-1.5b-instruct": "通义千问2.5-1.5B指令模型",
    "qwen2.5-0.5b-instruct": "通义千问2.5-0.5B指令模型",
}

# 预定义的DashScope嵌入模型配置
DASHSCOPE_EMBEDDING_MODELS = {
    "text-embedding-v1": "DashScope通用文本嵌入模型v1",
    "text-embedding-v2": "DashScope通用文本嵌入模型v2（推荐）",
    "text-embedding-async-v1": "DashScope异步文本嵌入模型v1",
    "text-embedding-async-v2": "DashScope异步文本嵌入模型v2",
}

def create_dashscope_model(model_name: str = "qwen-turbo", 
                          api_key: str = None,
                          **kwargs) -> DashScopeModel:
    """
    创建通义千问模型实例
    
    Args:
        model_name: 模型名称
        api_key: API密钥
        **kwargs: 其他参数
    
    Returns:
        DashScopeModel实例
    """
    if model_name not in TONGYI_MODELS:
        available_models = ", ".join(TONGYI_MODELS.keys())
        raise ValueError(f"不支持的模型: {model_name}. 可用模型: {available_models}")
    
    return DashScopeModel(
        model_name=model_name,
        api_key=api_key,
        **kwargs
    )

def create_dashscope_embedding_model(model_name: str = "text-embedding-v2",
                                    api_key: str = None) -> DashScopeEmbeddingModel:
    """
    创建DashScope嵌入模型实例
    
    Args:
        model_name: 嵌入模型名称
        api_key: API密钥
    
    Returns:
        DashScopeEmbeddingModel实例
    """
    if model_name not in DASHSCOPE_EMBEDDING_MODELS:
        available_models = ", ".join(DASHSCOPE_EMBEDDING_MODELS.keys())
        raise ValueError(f"不支持的嵌入模型: {model_name}. 可用模型: {available_models}")
    
    return DashScopeEmbeddingModel(
        model_name=model_name,
        api_key=api_key
    )

def list_available_models():
    """列出可用的通义千问模型"""
    print("可用的通义千问模型:")
    for model_name, description in TONGYI_MODELS.items():
        print(f"  - {model_name}: {description}")

def list_available_embedding_models():
    """列出可用的DashScope嵌入模型"""
    print("可用的DashScope嵌入模型:")
    for model_name, description in DASHSCOPE_EMBEDDING_MODELS.items():
        print(f"  - {model_name}: {description}")

# 使用示例
if __name__ == "__main__":
    print("=" * 60)
    print("DashScope模型配置测试")
    print("=" * 60)
    
    # 列出可用模型
    list_available_models()
    print()
    list_available_embedding_models()
    
    print("\n" + "=" * 60)
    print("连接测试")
    print("=" * 60)
    
    # 测试LLM模型连接
    try:
        print("测试通义千问LLM模型...")
        llm_model = create_dashscope_model("qwen-turbo")
        if llm_model.test_connection():
            print("✓ 通义千问LLM模型连接成功")
        else:
            print("✗ 通义千问LLM模型连接失败")
    except Exception as e:
        print(f"✗ 通义千问LLM模型初始化失败: {e}")
    
    # 测试嵌入模型连接
    try:
        print("\n测试DashScope嵌入模型...")
        embedding_model = create_dashscope_embedding_model("text-embedding-v2")
        if embedding_model.test_connection():
            print("✓ DashScope嵌入模型连接成功")
        else:
            print("✗ DashScope嵌入模型连接失败")
    except Exception as e:
        print(f"✗ DashScope嵌入模型初始化失败: {e}")
    
    # 环境变量提示
    if not os.getenv("DASHSCOPE_API_KEY"):
        print("\n" + "⚠️" * 20)
        print("请确保设置了DASHSCOPE_API_KEY环境变量")
        print("export DASHSCOPE_API_KEY='your-dashscope-api-key'")
        print("⚠️" * 20)