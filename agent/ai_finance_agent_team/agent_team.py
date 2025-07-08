"""
AI Finance Agent Team - 多 Agent 协作系统
包含 Web Agent（互联网搜索）和 Finance Agent（财务分析）
"""
from agno.agent import Agent
from agno.models.openai.like import OpenAILike
from agno.team.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FinanceAgentTeam:
    """AI 金融分析团队"""
    
    def __init__(self, api_key: str = None, model_provider: str = "qwen"):
        """
        初始化金融分析团队
        
        Args:
            api_key: API 密钥
            model_provider: 模型提供商 ("qwen" 或 "openai")
        """
        self.api_key = api_key
        self.model_provider = model_provider
        
        if not api_key:
            raise ValueError("请提供 API Key")
            
        self.setup_agents()
        self.setup_team()
    
    def _get_model(self):
        """根据提供商获取对应的模型"""
        if self.model_provider == "qwen":
            return OpenAILike(
                id="qwen-plus-latest",
                api_key=self.api_key,
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            )
        else:
            raise ValueError(f"不支持的模型提供商: {self.model_provider}")
    
    def setup_agents(self):
        """初始化各个 Agent"""
        
        
        # Web Agent - 负责互联网搜索和新闻收集
        self.web_agent = Agent(
            name="Web Search Agent",
            role="互联网搜索专家",
            model=self._get_model(),
            tools=[DuckDuckGoTools()],
            instructions=[
                "你是一个专业的互联网搜索专家，负责收集最新的新闻、市场动态和公司信息",
                "搜索时要关注：",
                "- 最新的公司新闻和公告",
                "- 行业趋势和市场动态", 
                "- 监管变化和政策影响",
                "- 竞争对手动态",
                "- 技术发展和创新",
                "始终提供信息来源和发布时间",
                "优先搜索权威财经媒体的报道",
                "用中文回复，但保留重要的英文专业术语",
            ],
            add_datetime_to_instructions=True,
            show_tool_calls=True,
            debug_mode=True,
        )
        
        # Finance Agent - 负责财务数据分析
        self.finance_agent = Agent(
            name="Finance Analysis Agent", 
            role="财务分析专家",
            model=self._get_model(),  # 为每个 Agent 创建独立的模型实例
            tools=[
                YFinanceTools()
            ],
            instructions=[
                "你是一个专业的财务分析师，负责深度财务数据分析",
                "分析内容包括：",
                "- 股价表现和技术指标",
                "- 基本面分析（P/E、市值、收入增长等）",
                "- 分析师评级和目标价",
                "- 财务健康状况",
                "- 行业比较和估值分析",
                "使用表格清晰展示财务数据",
                "明确标注公司名称和股票代码",
                "提供基于数据的投资建议和风险评估",
                "用中文回复，数据用标准格式展示",
            ],
            add_datetime_to_instructions=True,
            show_tool_calls=True,
            debug_mode=True,
        )
    
    def setup_team(self):
        """设置团队协作模式"""
        
        self.agent_team = Team(
            name="AI Finance Analysis Team",
            model= self._get_model(),
            members=[self.web_agent, self.finance_agent],
            instructions=[
                "你们是一个专业的金融分析团队，协作为用户提供全面的投资研究报告",
                "工作流程：",
                "1. Web Agent 搜索最新相关新闻和市场动态",
                "2. Finance Agent 分析财务数据和基本面",
                "3. 综合分析，提供全面的投资建议",
                "",
                "报告格式要求：",
                "- 使用醒目的标题",
                "- 执行摘要突出关键点",
                "- 财务数据优先，配合新闻背景",
                "- 清晰的段落分隔",
                "- 包含相关图表或表格",
                "- 添加'市场情绪'分析",
                "- 结尾包含'关键要点'和'风险因素'",
                "- 署名：AI金融分析团队 + 当前日期",
                "",
                "始终用中文回复用户",
            ],
            add_datetime_to_instructions=True,
            show_tool_calls=True,
            markdown=True,
            debug_mode=True,
        )
    
    def analyze(self, query: str, stream: bool = False):
        """执行分析查询"""
        try:
            if stream:
                return self.agent_team.print_response(query, stream=True)
            else:
                response = self.agent_team.run(query)
                return response.content if response else "分析失败，请重试"
        except Exception as e:
            logger.error(f"分析过程中发生错误: {e}")
            return f"分析过程中发生错误: {str(e)}"
    
    def get_sample_queries(self):
        """获取示例查询"""
        return [
            "分析苹果公司（AAPL）的最新新闻和财务表现",
            "英伟达（NVDA）的 AI 发展对股价的影响分析",
            "电动汽车制造商的表现如何？重点关注特斯拉（TSLA）",
            "半导体公司如 AMD 和英特尔的市场前景",
            "微软（MSFT）最近的发展和股票表现总结",
            "比较主要云服务提供商（AMZN、MSFT、GOOGL）的财务表现",
            "分析科技巨头（AAPL、GOOGL、MSFT）的投资组合配置建议",
        ]

if __name__ == "__main__":
    # 示例用法（需要提供 API Key）
    print("🚀 AI 金融分析团队")
    print("请注意：运行此程序需要提供 API Key")
    
    # 如果要测试，请取消注释下面的代码并提供您的 API Key
    # api_key = "your_api_key_here"
    # team = FinanceAgentTeam(api_key=api_key)
    # 
    # print("\n📝 示例查询：")
    # for i, query in enumerate(team.get_sample_queries(), 1):
    #     print(f"{i}. {query}")
    # 
    # print("\n" + "=" * 50)
    # 
    # # 示例分析
    # sample_query = "分析苹果公司（AAPL）的最新财务表现和市场新闻"
    # print(f"\n🔍 执行示例分析: {sample_query}")
    # print("-" * 50)
    # 
    # team.analyze(sample_query, stream=True)
