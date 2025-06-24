import os
import gradio as gr
from textwrap import dedent
from typing import Optional, Tuple

from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.tools.baidusearch import BaiduSearchTools

class TravelPlannerApp:
    """旅行规划助手应用"""
    
    def __init__(self):
        self.travel_agent: Optional[Agent] = None
    
    def create_travel_agent(self, deepseek_api_key: str) -> Agent:
        """创建旅行规划智能体"""
        # 设置环境变量
        os.environ["DEEPSEEK_API_KEY"] = deepseek_api_key
        
        travel_agent = Agent(
            name="智能旅行规划师",
            model=DeepSeek(id="deepseek-chat"),
            tools=[BaiduSearchTools()],
            markdown=True,
            description=dedent("""\
                你是一位专业的智能旅行规划师，拥有丰富的旅行规划经验！🌍

                你的专业领域包括：
                - 豪华和经济旅行规划
                - 文化沉浸式体验设计
                - 冒险旅行协调
                - 当地美食探索
                - 交通物流安排
                - 住宿选择建议
                - 活动策划
                - 预算优化
                - 群体旅行管理"""),
            instructions=dedent("""\
                请按照以下步骤来制定每个旅行计划：

                1. 初步评估 🎯
                   - 了解群体规模和动态
                   - 注意具体日期和时长
                   - 考虑预算限制
                   - 识别特殊需求
                   - 考虑季节因素

                2. 目的地研究 🔍
                   - 使用搜索工具获取最新信息
                   - 验证营业时间和可用性
                   - 查找当地活动和节日
                   - 研究天气模式
                   - 识别潜在挑战

                3. 住宿规划 🏨
                   - 选择靠近主要活动的位置
                   - 考虑群体规模和偏好
                   - 验证设施和服务
                   - 包含备选方案
                   - 检查取消政策

                4. 活动策划 🎨
                   - 平衡各种兴趣
                   - 包含当地体验
                   - 考虑场所间的通行时间
                   - 添加灵活的备选方案
                   - 注明预订要求

                5. 物流规划 🚗
                   - 详细说明交通选择
                   - 包含转换时间
                   - 添加当地交通提示
                   - 考虑无障碍性
                   - 制定应急计划

                6. 预算细分 💰
                   - 逐项列出主要费用
                   - 包含估算成本
                   - 添加省钱提示
                   - 注明潜在隐性成本
                   - 建议省钱替代方案

                呈现风格：
                - 使用清晰的 markdown 格式
                - 按天展示行程
                - 在相关时包含地图
                - 为活动添加时间估算
                - 使用表情符号更好地可视化
                - 突出必做活动
                - 注明提前预订要求
                - 包含当地提示和文化注释"""),
            expected_output=dedent("""\
                # {目的地} 旅行行程 🌎

                ## 概览
                - **日期**: {日期}
                - **群体规模**: {规模}
                - **预算**: {预算}
                - **旅行风格**: {风格}

                ## 住宿 🏨
                {详细的住宿选择，包含优缺点}

                ## 每日行程

                ### 第1天
                {详细的时间表和活动安排}

                ### 第2天
                {详细的时间表和活动安排}

                [继续每一天...]

                ## 预算细分 💰
                - 住宿: {费用}
                - 活动: {费用}
                - 交通: {费用}
                - 餐饮: {费用}
                - 其他: {费用}

                ## 重要提示 ℹ️
                {关键信息和提示}

                ## 预订要求 📋
                {需要提前预订的项目}

                ## 当地贴士 🗺️
                {内部建议和文化注释}

                ---
                由智能旅行规划师创建"""),
            add_datetime_to_instructions=True,
            show_tool_calls=True,
        )
        
        return travel_agent
    
    def validate_api_keys(self, deepseek_key: str) -> Tuple[bool, str]:
        """验证 API 密钥"""
        if not deepseek_key or not deepseek_key.strip():
            return False, "请输入 DeepSeek API Key"
    
        if not deepseek_key.startswith('sk-'):
            return False, "DeepSeek API Key 格式不正确"
        
        return True, "API Keys 验证成功"
    
    def generate_travel_plan(
        self, 
        deepseek_key: str, 
        destination: str, 
        days: int, 
        budget: str = "",
        group_size: str = "",
        travel_style: str = ""
    ) -> str:
        """生成旅行计划"""
        try:
            # 验证 API Keys
            is_valid, message = self.validate_api_keys(deepseek_key)
            if not is_valid:
                return f"❌ {message}"
            
            # 验证输入参数
            if not destination or not destination.strip():
                return "❌ 请输入旅游目的地"
            
            if days <= 0:
                return "❌ 旅游天数必须大于0"
            
            # 创建智能体
            self.travel_agent = self.create_travel_agent(deepseek_key)
            
            # 构建提示信息
            prompt_parts = [
                f"请为我规划一个{days}天的{destination}旅行计划。"
            ]
            
            if group_size:
                prompt_parts.append(f"群体规模：{group_size}")
            
            if budget:
                prompt_parts.append(f"预算：{budget}")
            
            if travel_style:
                prompt_parts.append(f"旅行风格：{travel_style}")
            
            prompt_parts.append("请提供详细的每日行程、住宿建议、活动安排和预算细分。")
            
            prompt = " ".join(prompt_parts)
            
            # 生成旅行计划
            response = self.travel_agent.run(prompt)
            
            return response.content
            
        except Exception as e:
            return f"❌ 生成旅行计划时出错：{str(e)}"

def create_gradio_interface():
    """创建 Gradio 界面"""
    app = TravelPlannerApp()
    
    with gr.Blocks(
        title="🌍 智能旅行规划助手",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1200px !important;
        }
        """
    ) as interface:
        
        gr.HTML("""
        <div style="text-align: center; margin-bottom: 20px;">
            <h1>🌍 智能旅行规划助手</h1>
            <p style="font-size: 18px; color: #666;">
                基于 Agno + Gradio 构建的AI旅行规划助手，为您定制完美的旅行计划！
            </p>
        </div>
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.HTML("<h3>🔑 API 配置</h3>")
                
                deepseek_api_key = gr.Textbox(
                    label="deepseek API Key",
                    placeholder="sk-...",
                    type="password",
                    info="用于调用 deepseek-chat 模型"
                )
                
    
                
                gr.HTML("<h3>🗺️ 旅行信息</h3>")
                
                destination = gr.Textbox(
                    label="旅游目的地",
                    placeholder="例如：日本京都、法国巴黎、新西兰...",
                    info="您想去的地方"
                )
                
                days = gr.Slider(
                    minimum=1,
                    maximum=30,
                    value=5,
                    step=1,
                    label="旅游天数",
                    info="计划旅行的天数"
                )
                
                with gr.Row():
                    group_size = gr.Textbox(
                        label="群体规模（可选）",
                        placeholder="例如：4人家庭、2人情侣、单人旅行...",
                    )
                    
                    budget = gr.Textbox(
                        label="预算（可选）",
                        placeholder="例如：5000元、$2000、豪华/经济...",
                    )
                
                travel_style = gr.Textbox(
                    label="旅行风格（可选）",
                    placeholder="例如：文化探索、冒险旅行、休闲度假、美食之旅...",
                )
                
                generate_btn = gr.Button(
                    "🚀 生成旅行计划",
                    variant="primary",
                    size="lg"
                )
            
            with gr.Column(scale=2):
                gr.HTML("<h3>📋 旅行计划</h3>")
                
                output = gr.Markdown(
                    value="点击左侧的「生成旅行计划」按钮开始规划您的完美旅行！✈️",
                    elem_classes=["travel-plan-output"]
                )
        
        # 事件处理
        generate_btn.click(
            fn=app.generate_travel_plan,
            inputs=[
                deepseek_api_key,
                destination,
                days,
                budget,
                group_size,
                travel_style
            ],
            outputs=[output],
            show_progress=True
        )
        
        # 示例
        gr.HTML("""
        <div style="margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 10px;">
            <h4>💡 使用示例</h4>
            <ul style="margin: 10px 0;">
                <li>🏛️ "规划一个5天的京都文化探索之旅，4人家庭"</li>
                <li>💕 "创建一个浪漫的巴黎周末度假，预算2000美元"</li>
                <li>🏔️ "组织一个7天的新西兰冒险之旅，单人旅行"</li>
                <li>🏢 "设计一个20人的巴塞罗那公司团建活动"</li>
            </ul>
        </div>
        """)
    
    return interface

if __name__ == "__main__":
    # 创建并启动界面
    interface = create_gradio_interface()
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        show_error=True
    ) 