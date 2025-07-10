# 基于 DeepEval 和通义千问的 RAG 评估项目

本项目是一个完整的示例，展示了如何利用 `deepeval` 框架对一个基于 LangChain 和通义千问大模型的 RAG (Retrieval-Augmented Generation) 应用进行自动化评估。

## 核心特性

- **自定义模型集成**: 演示了如何将阿里云通义千问（DashScope）的 LLM 和 Embedding 模型无缝集成到 `deepeval` 评估框架中。
- **自动化数据集生成**: 使用 `deepeval` 的 `Synthesizer` 功能，根据本地知识库文档（`company_information.txt`）自动生成包含问题、上下文和参考答案的评估数据集。
- **全面的 RAG 评估**: 实现了对 RAG 应用的端到端评估，覆盖了包括答案相关性 (`AnswerRelevancy`) 和忠实度 (`Faithfulness`) 在内的关键指标。
- **模块化代码**: 项目代码结构清晰，将 RAG 智能体、模型配置、数据集生成和评估脚本分离，易于理解和扩展。

## 项目结构

```
.
├── README.md                 # 本说明文件
├── qa_agent.py               # 核心的 RAG 问答 Agent
├── dashscope_config.py       # DeepEval 与通义千问模型集成的封装
├── dataset_generate.py       # 自动生成评估数据集的脚本
├── test_qa_agent.py          # RAG Agent 的完整评估流程脚本
├── test_app.py               # DeepEval 基础用法示例
├── company_information.txt   # 知识库示例文档
└── requirements.txt          # 项目依赖
```

## 模块一：为 DeepEval 自定义模型 (`dashscope_config.py`)

为了在 `deepeval` 中使用通义千问模型，我们需要对其进行封装，使其符合 `deepeval` 的规范。`dashscope_config.py` 文件就是为此目的而创建的。

- **`DashScopeModel`**: 继承自 `deepeval.models.DeepEvalBaseLLM`，将通义千问的聊天模型（如 `qwen-turbo`）封装成 `deepeval` 可用的评估器。
- **`DashScopeEmbeddingModel`**: 继承自 `deepeval.models.DeepEvalBaseEmbeddingModel`，封装了 DashScope 的文本嵌入模型（如 `text-embedding-v2`）。

这个文件是本项目能够在 `deepeval` 中使用非 OpenAI 模型的基础，也为集成其他自定义模型提供了范例。

## 模块二：DeepEval 基础用法 (`test_app.py`)

`test_app.py` 是一个入门级的 `deepeval` 示例，用于展示其最核心的评估流程，不依赖于复杂的 RAG 应用。

- **`LLMTestCase`**: 定义一个基本的测试用例，包含输入（`input`）、模型的实际输出（`actual_output`）和期望的理想输出（`expected_output`）。
- **`GEval`**: `deepeval` 中一个非常灵活的指标，允许你通过自然语言定义评估标准（`criteria`），然后由一个强大的 LLM（这里我们指定为自定义的通义千问模型）来打分。
- **`evaluate()`**: `deepeval` 的核心函数，接收测试用例列表和评估指标列表，执行评估并输出结果。

通过运行此文件，你可以快速理解 `deepeval` 的工作模式：**测试用例 + 评估指标 -> 评估结果**。

## 模块三：端到端的 RAG 应用评估

这是项目的核心部分，完整展示了如何评估一个真实的 RAG 应用。它围绕 `QAAgent` 展开，涉及数据集生成和最终评估。

- **`qa_agent.py`**:
  - 一个基于 LangChain 构建的问答机器人。
  - 使用通义千问作为 LLM，DashScope 作为嵌入模型。
  - 支持 FAISS 和 Chroma 向量数据库，负责文档加载、分割、索引和查询。

- **`dataset_generate.py`**:
  - 展示了 `deepeval` 强大的自动化数据生成能力。
  - 它读取 `company_information.txt` 文档，利用 `Synthesizer` 自动创建一系列的 "golden" 测试用例（包含输入问题、期望输出和上下文）。
  - 生成的数据集可以推送到 DeepEval Cloud，方便团队协作和版本管理。

- **`test_qa_agent.py`**:
  - 这是项目的主评估脚本，它将所有部分串联起来。
  - 从 DeepEval Cloud 拉取数据集，遍历每个用例，调用 `QAAgent` 生成实际回答并获取检索上下文。
  - 使用 `AnswerRelevancyMetric` 和 `FaithfulnessMetric` 等 RAG 专用指标进行评估。
  - 输出最终的评估报告，帮助我们量化 RAG 应用的性能。

## 使用指南

### 1. 环境设置

首先，建议创建一个虚拟环境。

```bash
# 创建并激活虚拟环境 (macOS/Linux)
python -m venv venv
source venv/bin/activate
```

安装所有依赖项：
```bash
pip install -r requirements.txt
```

在运行代码之前，你需要设置你的阿里云 DashScope API 密钥。
```bash
export DASHSCOPE_API_KEY='your-dashscope-api-key'
```

### 2. （可选）理解基础用法

运行 `test_app.py` 来快速了解 `deepeval` 的基本工作方式。
```bash
python test_app.py
```

### 3. 生成评估数据集

运行 `dataset_generate.py` 脚本，根据 `company_information.txt` 的内容自动生成测试用例集，并将其上传到 DeepEval Cloud。

```bash
python dataset_generate.py
```
*注意：该脚本会将生成的数据集命名为 "Company QA Dataset" 并推送到 DeepEval Cloud。*

### 4. 运行 RAG 评估

数据集准备好后，运行 `test_qa_agent.py` 来对你的 `QAAgent` 进行完整的评估。

```bash
python test_qa_agent.py
```
脚本会自动拉取数据集，执行评估，并在控制台打印出详细的评估结果。 