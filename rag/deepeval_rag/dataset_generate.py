from dashscope_config import create_dashscope_model,create_dashscope_embedding_model
from deepeval.dataset import EvaluationDataset
from deepeval.synthesizer import Synthesizer
from deepeval.synthesizer.config import ContextConstructionConfig

import os

# 使用通义千问模型（推荐方式 - 直接使用SDK）
custom_model = create_dashscope_model(
    model_name="qwen-plus",
    api_key=os.getenv("DASHSCOPE_API_KEY")
)
#  使用百炼的 嵌入式模型
custom_embedder = create_dashscope_embedding_model(
    model_name="text-embedding-v2",
    api_key=os.getenv("DASHSCOPE_API_KEY")
)

prompt_template = """
你是一个乐于助人的QA助手，专门回答用户关于公司产品和服务的问题。
你的目标是根据从公司知识库中检索到的信息，提供准确、相关且结构清晰的回答。
"""

#  1、根据已有的知识库生成 测试数据集
synthesizer = Synthesizer(model=custom_model)
synthesizer.generate_goldens_from_docs(
    document_paths=['./company_information.txt'],
    include_expected_output=True,
    context_construction_config=ContextConstructionConfig(critic_model=custom_model, embedder=custom_embedder)
)
dataset = EvaluationDataset(goldens=synthesizer.synthetic_goldens)
print(dataset.goldens[0])
dataset.push("Company QA Dataset")