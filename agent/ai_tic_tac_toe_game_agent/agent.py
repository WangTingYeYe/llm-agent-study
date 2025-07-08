"""
井字棋对战
---------------------------------
这个示例展示了如何构建一个由两个 AI 代理对战的井字棋游戏。
游戏包含一个裁判代理,负责协调使用不同语言模型的两个玩家代理之间的对战。

使用示例:
---------------
1. 使用默认设置快速开始游戏:
   referee_agent = get_tic_tac_toe_referee()
   play_tic_tac_toe()

2. 关闭调试模式的游戏:
   referee_agent = get_tic_tac_toe_referee(debug_mode=False)
   play_tic_tac_toe(debug_mode=False)

游戏集成了:
  - 多种 AI 模型(Claude、GPT-4 等)
  - 回合制游戏协调
  - Move validation and game state management
"""

import os
import sys
from pathlib import Path
from textwrap import dedent
from typing import Tuple

from agno.agent import Agent
from agno.models.openai import OpenAILike
from agno.models.deepseek import DeepSeek

project_root = str(Path(__file__).parent.parent.parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)


def get_model_for_provider(provider: str, model_name: str):
    """
    根据提供者创建并返回适当的模型实例。

    Args:
        provider: The model provider (e.g., 'openai', 'deepseek', 'qwen')
        model_name: The specific model name/ID

    Returns:
        An instance of the appropriate model class

    Raises:
        ValueError: If the provider is not supported
    """
    if provider == "deepseek":
        return DeepSeek(id=model_name, api_key=os.environ["DEEPSEEK_API_KEY"])
    elif provider == "qwen":
        return OpenAILike(
                id=model_name,
                api_key=os.environ["QWEN_API_KEY"],
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            )

    else:
        raise ValueError(f"Unsupported model provider: {provider}")


def get_tic_tac_toe_players(
    model_x: str = "deepseek:deepseek-chat",
    model_o: str = "qwen:qwen-plus-latest",
    debug_mode: bool = True,
) -> Tuple[Agent, Agent]:
    """
    返回一个井字棋裁判代理实例，负责协调游戏。

    Args:
        model_x: 模型配置为玩家 X
        model_o: 模型配置为玩家 O
        debug_mode: 启用日志和调试功能

    Returns:
        一个配置好的裁判代理实例
    """
    # Parse model provider and name
    provider_x, model_name_x = model_x.split(":")
    provider_o, model_name_o = model_o.split(":")

    # Create model instances using the helper function
    model_x = get_model_for_provider(provider_x, model_name_x)
    model_o = get_model_for_provider(provider_o, model_name_o)

    player_x = Agent(
        name="Player X",
        description=dedent("""\
        你是井字棋游戏中的 X 玩家。你的目标是通过在一行(水平、垂直或对角线)放置三个 X 来获胜。

        棋盘布局:
        - 棋盘是一个 3x3 的网格,坐标从 (0,0) 到 (2,2)
        - 左上角是 (0,0), 右下角是 (2,2)

        规则:
        - 你只能在空白格子(显示为" ")放置 X
        - 玩家轮流放置标记
        - 第一个在一行(水平、垂直或对角线)获得3个标记的玩家获胜
        - 如果所有空格都填满但没有获胜者,则游戏平局

        你的回应:
        - 只需提供两个由空格分隔的数字(行 列)
        - 示例: "1 2" 表示在第1行第2列放置 X
        - 只能从提供给你的有效移动列表中选择

        策略提示:
        - 仔细研究棋盘并做出战略性移动
        - 阻止对手可能的获胜路径
        - 创造多个获胜路径的机会
        - 注意有效移动列表,避免非法移动
        """),
        model=model_x,
        debug_mode=debug_mode,
    )

    player_o = Agent(
        name="Player O",
        description=dedent("""\
        你是井字棋游戏中的 O 玩家。你的目标是通过在一行(水平、垂直或对角线)放置三个 O 来获胜。

        棋盘布局:
        - 棋盘是一个 3x3 的网格,坐标从 (0,0) 到 (2,2)
        - 左上角是 (0,0), 右下角是 (2,2)

        规则:
        - 你只能在空白格子(显示为" ")放置 O
        - 玩家轮流放置标记
        - 第一个在一行(水平、垂直或对角线)获得3个标记的玩家获胜
        - 如果所有空格都填满但没有获胜者,则游戏平局

        你的回应:
        - 只需提供两个由空格分隔的数字(行 列)
        - 示例: "1 2" 表示在第1行第2列放置 O
        - 只能从提供给你的有效移动列表中选择

        策略提示:
        - 仔细研究棋盘并做出战略性移动
        - 阻止对手可能的获胜路径
        - 创造多个获胜路径的机会
        - 注意有效移动列表,避免非法移动
        """),
        model=model_o,
        debug_mode=debug_mode,
    )

    return player_x, player_o