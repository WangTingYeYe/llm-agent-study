from deepeval import evaluate
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval.metrics import GEval
from deepeval.models.base_model import DeepEvalBaseLLM
from langchain_openai import ChatOpenAI
from dashscope_config import create_dashscope_model
import os

# 使用通义千问模型（推荐方式 - 直接使用SDK）
custom_model = create_dashscope_model(
    model_name="qwen-turbo",
    api_key=os.getenv("DASHSCOPE_API_KEY")
)

# 使用自定义模型创建GEval指标
correctness_metric = GEval(
    name="正确性",
    criteria="根据'expected_output'判断'actual_output'是否正确。",
    evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.EXPECTED_OUTPUT],
    threshold=0.5,
    model=custom_model  # 使用自定义模型
)
concision_metric = GEval(
    name="简洁性",
    criteria="评估'actual_output'是否在保留所有必要信息的同时保持简洁。",
    evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
    model=custom_model  # 使用自定义模型
)

test_case = LLMTestCase(
    input="我有持续的咳嗽和发烧。我需要担心吗？",
    # 替换为你的 LLM 应用的实际输出
    actual_output="持续的咳嗽和发烧并不重要，多抽几根华子，抽完就好了",
    expected_output="持续的咳嗽和发烧可能表明多种疾病，从轻微的病毒感染到更严重的疾病如肺炎或新冠肺炎。如果症状恶化、持续数天，或伴有呼吸困难、胸痛或其他令人担忧的症状，你应该及时就医。"
)

test_case2 = LLMTestCase(
    input="张飞是谁？他的武力值在什么水平？",
    # 替换为你的 LLM 应用的实际输出
    actual_output="吾乃张飞，字翼德，蜀汉名将，勇猛善战，与关羽、赵云、马超等人齐名。",
    expected_output="张飞的武力值在三国时期属于顶尖水平，在《三国演义》中堪称超一流武将，仅次于吕布，与关羽、赵云、马超等人齐名。他的勇猛、豪气和战场威慑力使他成为三国故事中最具标志性的猛将之一。不过，历史中的张飞更注重统兵和实际战功，单挑描写较少，武力值更多体现在战场上的整体表现。"
)

evaluate([test_case, test_case2], [correctness_metric, concision_metric])