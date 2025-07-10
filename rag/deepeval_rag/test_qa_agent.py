from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric
from deepeval.dataset import EvaluationDataset
from deepeval.test_case import LLMTestCase
from deepeval import evaluate
from dashscope_config import create_dashscope_model

from qa_agent import QAAgent
import os

model = create_dashscope_model(
    model_name="qwen-plus",
    api_key=os.getenv("DASHSCOPE_API_KEY")
)
#  定义评估指标
answer_relevancy_metric = AnswerRelevancyMetric(model=model)
faithfulness_metric = FaithfulnessMetric(model=model)


dataset = EvaluationDataset()
dataset.pull("Company QA Dataset", auto_convert_goldens_to_test_cases=False)



# 创建 QA Agent
qa_agent = QAAgent(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    llm_model="qwen-turbo",
    embedding_model="text-embedding-v2",
    vector_store_type="faiss"  # 可选 "chroma"
)

# 加载文档并建立索引
qa_agent.load_and_index_document("company_information.txt")


for golden in dataset.goldens:
    # 获取实际输出
    actual_output = qa_agent.query(golden.input)  
    # 获取检索上下文
    retrieval_context = [doc.page_content for doc in qa_agent.similarity_search(golden.input)]

    dataset.add_test_case(
        LLMTestCase(
            input=golden.input,
            actual_output=actual_output,
            retrieval_context=retrieval_context
        )
    )

prompt_template = """
你是一个专业的问答助手。请基于以下提供的上下文信息来回答用户的问题。

上下文信息:
{context}

用户问题: {question}

请按照以下要求回答:
1. 仅基于提供的上下文信息回答问题
2. 如果上下文中没有相关信息，请明确说明
3. 回答要准确、简洁、有条理
4. 如果可能，请引用相关的具体信息

回答:
"""
evaluate(
  dataset,
  metrics=[answer_relevancy_metric, faithfulness_metric],
  hyperparameters={"prompt template": prompt_template, "top-k": 4}
)