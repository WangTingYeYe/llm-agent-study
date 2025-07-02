import os
import nest_asyncio
import streamlit as st
from agent import get_tic_tac_toe_players
from agno.utils.log import logger
from utils import (
    CUSTOM_CSS,
    TicTacToeBoard,
    display_board,
    display_move_history,
    show_agent_status,
)

nest_asyncio.apply()

# Page configuration
st.set_page_config(
    page_title="代理玩井字棋",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load custom CSS with dark mode support
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def main():
    ####################################################################
    # App header
    ####################################################################
    st.markdown(
        "<h1 class='main-title'>观看代理玩井字棋</h1>",
        unsafe_allow_html=True,
    )

    ####################################################################
    # Initialize session state
    ####################################################################
    if "game_started" not in st.session_state:
        st.session_state.game_started = False
        st.session_state.game_paused = False
        st.session_state.move_history = []

    with st.sidebar:
        st.markdown("### 游戏控制")
        model_options = {
            "deepseek-chat": "deepseek:deepseek-chat",
            "qwen-plus-latest": "qwen:qwen-plus-latest",
        }
        ################################################################
        # Model selection
        ################################################################
        selected_p_x = st.selectbox(
            "选择玩家 X",
            list(model_options.keys()),
            index=list(model_options.keys()).index("deepseek-chat"),
            key="model_p1",
        )
        selected_p_o = st.selectbox(
            "选择玩家 O",
            list(model_options.keys()),
            index=list(model_options.keys()).index("qwen-plus-latest"),
            key="model_p2",
        )

        # API Key 输入
        deepseek_api_key = st.text_input(
            "Deepseek API Key",
            type="password",
            help="请输入 Deepseek API Key",
            key="deepseek_api_key"
        )
        qwen_api_key = st.text_input(
            "Qwen API Key", 
            type="password",
            help="请输入通义千问 API Key",
            key="qwen_api_key"
        )

        if deepseek_api_key:
            os.environ["DEEPSEEK_API_KEY"] = deepseek_api_key
        if qwen_api_key:
            os.environ["QWEN_API_KEY"] = qwen_api_key

        ################################################################
        # Game controls
        ################################################################
        col1, col2 = st.columns(2)
        with col1:
            if not st.session_state.game_started:
                if st.button("▶️ 开始游戏"):
                    st.session_state.player_x, st.session_state.player_o = (
                        get_tic_tac_toe_players(
                            model_x=model_options[selected_p_x],
                            model_o=model_options[selected_p_o],
                            debug_mode=True,
                        )
                    )
                    st.session_state.game_board = TicTacToeBoard()
                    st.session_state.game_started = True
                    st.session_state.game_paused = False
                    st.session_state.move_history = []
                    st.rerun()
            else:
                game_over, _ = st.session_state.game_board.get_game_state()
                if not game_over:
                    if st.button(
                        "⏸️ 暂停" if not st.session_state.game_paused else "▶️ 继续"
                    ):
                        st.session_state.game_paused = not st.session_state.game_paused
                        st.rerun()
        with col2:
            if st.session_state.game_started:
                if st.button("🔄 新游戏"):
                    st.session_state.player_x, st.session_state.player_o = (
                        get_tic_tac_toe_players(
                            model_x=model_options[selected_p_x],
                            model_o=model_options[selected_p_o],
                            debug_mode=True,
                        )
                    )
                    st.session_state.game_board = TicTacToeBoard()
                    st.session_state.game_paused = False
                    st.session_state.move_history = []
                    st.rerun()

    ####################################################################
    # Header showing current models
    ####################################################################
    if st.session_state.game_started:
        st.markdown(
            f"<h3 style='color:#87CEEB; text-align:center;'>{selected_p_x} 对战 {selected_p_o}</h3>",
            unsafe_allow_html=True,
        )

    ####################################################################
    # Main game area
    ####################################################################
    if st.session_state.game_started:
        game_over, status = st.session_state.game_board.get_game_state()

        display_board(st.session_state.game_board)

        # Show game status (winner/draw/current player)
        if game_over:
            winner_player = (
                "X" if "X wins" in status else "O" if "O wins" in status else None
            )
            if winner_player:
                winner_num = "1" if winner_player == "X" else "2"
                winner_model = selected_p_x if winner_player == "X" else selected_p_o
                st.success(f"🏆 游戏结束! 玩家 {winner_num} ({winner_model}) 获胜!")
            else:
                st.info("🤝 游戏结束! 平局!")
        else:
            # Show current player status
            current_player = st.session_state.game_board.current_player
            player_num = "1" if current_player == "X" else "2"
            current_model_name = selected_p_x if current_player == "X" else selected_p_o

            show_agent_status(
                f"Player {player_num} ({current_model_name})",
                "轮到你了",
            )

        display_move_history()

        if not st.session_state.game_paused and not game_over:
            # Thinking indicator
            st.markdown(
                f"""<div class="thinking-container">
                    <div class="agent-thinking">
                        <div style="margin-right: 10px; display: inline-block;">🔄</div>
                        {player_num} ({current_model_name}) 正在思考...
                    </div>
                </div>""",
                unsafe_allow_html=True,
            )

            valid_moves = st.session_state.game_board.get_valid_moves()

            current_agent = (
                st.session_state.player_x
                if current_player == "X"
                else st.session_state.player_o
            )
            response = current_agent.run(
                f"""\
当前棋盘状态:\n{st.session_state.game_board.get_board_state()}\n
有效移动 (行, 列): {valid_moves}\n
选择你下一步的移动，从上面的有效移动中选择。
只用两个数字表示行和列，例如 "1 2"。""",
                stream=False,
            )

            try:
                import re

                numbers = re.findall(r"\d+", response.content if response else "")
                row, col = map(int, numbers[:2])
                success, message = st.session_state.game_board.make_move(row, col)

                if success:
                    move_number = len(st.session_state.move_history) + 1
                    st.session_state.move_history.append(
                        {
                            "number": move_number,
                            "player": f"Player {player_num} ({current_model_name})",
                            "move": f"{row},{col}",
                        }
                    )

                    logger.info(
                        f"移动 {move_number}: 玩家 {player_num} ({current_model_name}) 在位置 ({row}, {col})"
                    )
                    logger.info(
                        f"棋盘状态:\n{st.session_state.game_board.get_board_state()}"
                    )

                    # Check game state after move
                    game_over, status = st.session_state.game_board.get_game_state()
                    if game_over:
                        logger.info(f"游戏结束 - {status}")
                        if "wins" in status:
                            st.success(f"🏆 游戏结束! {status}")
                        else:
                            st.info(f"🤝 游戏结束! {status}")
                        st.session_state.game_paused = True
                    st.rerun()
                else:
                    logger.error(f"无效移动尝试: {message}")
                    response = current_agent.run(
                        f"""\
无效移动: {message}

当前棋盘状态:\n{st.session_state.game_board.get_board_state()}\n
有效移动 (行, 列): {valid_moves}\n
请从上面的有效移动列表中选择一个有效的移动。
只用两个数字表示行和列，例如 "1 2"。""",
                        stream=False,
                    )
                    st.rerun()

            except Exception as e:
                logger.error(f"Error processing move: {str(e)}")
                st.error(f"Error processing move: {str(e)}")
                st.rerun()
    else:
        st.info("👈 点击 '开始游戏' 开始游戏!")

    ####################################################################
    # About section
    ####################################################################
    st.sidebar.markdown(
        f"""
    ### 🎮 井字棋对战
    观看两个代理实时对战!

    **当前玩家:**
    * 🔵 玩家 X: `{selected_p_x}`
    * 🔴 玩家 O: `{selected_p_o}`

    **工作原理:**
    每个代理分析棋盘并采用战略思考来:
    * 🏆 找到获胜的移动
    * 🛡️ 阻止对手获胜
    * ⭐ 控制战略位置
    * 🤔 计划多个移动

    使用 Streamlit 和 Agno 构建
    """
    )


if __name__ == "__main__":
    main()
