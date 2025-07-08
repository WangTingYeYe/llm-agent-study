import chess
import chess.svg
import streamlit as st
from autogen import ConversableAgent, register_function

if "qwen_api_key" not in st.session_state:
    st.session_state.qwen_api_key = None
if "board" not in st.session_state:
    st.session_state.board = chess.Board()
if "made_move" not in st.session_state:
    st.session_state.made_move = False
if "board_svg" not in st.session_state:
    st.session_state.board_svg = None
if "move_history" not in st.session_state:
    st.session_state.move_history = []
if "max_turns" not in st.session_state:
    st.session_state.max_turns = 5

st.sidebar.title("象棋代理配置")
qwen_api_key = st.sidebar.text_input("输入您的Qwen API密钥:", type="password")
if qwen_api_key:
    st.session_state.qwen_api_key = qwen_api_key
    st.sidebar.success("API key saved!")

st.sidebar.info("""
要完成一局可能导致将军的完整象棋对局，大约需要超过200个回合。
但这会消耗大量的API额度和时间。
为了演示目的,建议使用5-10个回合。
""")

max_turns_input = st.sidebar.number_input(
    "输入移动次数 (max_turns):",
    min_value=1,
    max_value=1000,
    value=st.session_state.max_turns,
    step=1
)

if max_turns_input:
    st.session_state.max_turns = max_turns_input
    st.sidebar.success(f"总移动次数设置为 {st.session_state.max_turns}!")

st.title("使用AutoGen代理的象棋游戏")

def available_moves() -> str:
    available_moves = [str(move) for move in st.session_state.board.legal_moves]
    return "可用的移动是: " + ",".join(available_moves)

def execute_move(move: str) -> str:
    try:
        chess_move = chess.Move.from_uci(move)
        if chess_move not in st.session_state.board.legal_moves:
            return f"无效的移动: {move}. 请调用 available_moves() 查看有效的移动。"
        
        # Update board state
        st.session_state.board.push(chess_move)
        st.session_state.made_move = True

        # Generate and store board visualization
        board_svg = chess.svg.board(st.session_state.board,
                                  arrows=[(chess_move.from_square, chess_move.to_square)],
                                  fill={chess_move.from_square: "gray"},
                                  size=400)
        st.session_state.board_svg = board_svg
        st.session_state.move_history.append(board_svg)

        # Get piece information
        moved_piece = st.session_state.board.piece_at(chess_move.to_square)
        piece_unicode = moved_piece.unicode_symbol()
        piece_type_name = chess.piece_name(moved_piece.piece_type)
        piece_name = piece_type_name.capitalize() if piece_unicode.isupper() else piece_type_name
        
        # Generate move description
        from_square = chess.SQUARE_NAMES[chess_move.from_square]
        to_square = chess.SQUARE_NAMES[chess_move.to_square]
        move_desc = f"Moved {piece_name} ({piece_unicode}) from {from_square} to {to_square}."
        if st.session_state.board.is_checkmate():
            winner = 'White' if st.session_state.board.turn == chess.BLACK else 'Black'
            move_desc += f"\n将军! {winner} 获胜!"
        elif st.session_state.board.is_stalemate():
            move_desc += "\n游戏以平局结束!"
        elif st.session_state.board.is_insufficient_material():
            move_desc += "\n游戏以平局结束 - 缺乏材料将军!"
        elif st.session_state.board.is_check():
            move_desc += "\n将军!"

        return move_desc
    except ValueError:
        return f"无效的移动格式: {move}. 请使用UCI格式 (e.g., 'e2e4')."

def check_made_move(msg):
    if st.session_state.made_move:
        st.session_state.made_move = False
        return True
    else:
        return False

if st.session_state.qwen_api_key:
    try:
        agent_white_config_list = [
            {
                "model": "qwen-plus-latest",
                "api_key": st.session_state.qwen_api_key,
                "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1"
            },
        ]
        


        agent_black_config_list = [
            {
                "model": "qwen-plus-latest",
                "api_key": st.session_state.qwen_api_key,
                "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1"
            },
        ]

        agent_white = ConversableAgent(
            name="Agent_White",  
            system_message="你是一个专业的象棋玩家，你扮演白棋。 "
            "首先调用 available_moves() 获取合法的移动列表。 "
            "然后调用 execute_move(move) 来执行移动。",
            llm_config={"config_list": agent_white_config_list, "cache_seed": None},
        )

        agent_black = ConversableAgent(
            name="Agent_Black",  
            system_message="你是一个专业的象棋玩家，你扮演黑棋。 "
            "首先调用 available_moves() 获取合法的移动列表。 "
            "然后调用 execute_move(move) 来执行移动。",
            llm_config={"config_list": agent_black_config_list, "cache_seed": None},
        )

        game_master = ConversableAgent(
            name="Game_Master",  
            llm_config=False,
            is_termination_msg=check_made_move,
            default_auto_reply="请做出移动",
            human_input_mode="NEVER",
        )

        register_function(
            execute_move,
            caller=agent_white,
            executor=game_master,
            name="execute_move",
            description="调用此工具来做出移动",
        )

        register_function(
            available_moves,
            caller=agent_white,
            executor=game_master,
            name="available_moves",
            description="获取合法的移动列表",
        )

        register_function(
            execute_move,
            caller=agent_black,
            executor=game_master,
            name="execute_move",
            description="调用此工具来做出移动",
        )

        register_function(
            available_moves,
            caller=agent_black,
            executor=game_master,
            name="available_moves",
            description="获取合法的移动列表",
        )

        agent_white.register_nested_chats(
            trigger=agent_black,
            chat_queue=[
                {
                    "sender": game_master,
                    "recipient": agent_white,
                    "summary_method": "last_msg",
                }
            ],
        )

        agent_black.register_nested_chats(
            trigger=agent_white,
            chat_queue=[
                {
                    "sender": game_master,
                    "recipient": agent_black,
                    "summary_method": "last_msg",
                }
            ],
        )

        st.info("""
这个象棋游戏是由两个AG2 AI代理进行的:
- **Agent White**: 一个由Qwen-plus-latest驱动的象棋玩家，控制白棋
- **Agent Black**: 一个由Qwen-plus-latest驱动的象棋玩家，控制黑棋

游戏由一个**Game Master**管理，它:
- 验证所有移动
- 更新棋盘
- 管理玩家轮流
- 提供合法的移动信息
""")

        initial_board_svg = chess.svg.board(st.session_state.board, size=300)
        st.subheader("初始棋盘")
        st.image(initial_board_svg)

        if st.button("Start Game"):
            st.session_state.board.reset()
            st.session_state.made_move = False
            st.session_state.move_history = []
            st.session_state.board_svg = chess.svg.board(st.session_state.board, size=300)
            st.info("AI代理现在将相互对战。每个代理将分析棋盘，" 
                   "从Game Master(代理)请求合法的移动，并做出战略决策。")
            st.success("您可以在终端输出中查看代理之间的交互，在代理之间的轮次结束后，您可以查看所有棋盘移动显示在下面!")
            st.write("游戏开始! 白棋的回合。")

            chat_result = agent_black.initiate_chat(
                recipient=agent_white, 
                message="让我们下棋! 你先走, 轮到你了。",
                max_turns=st.session_state.max_turns,
                summary_method="reflection_with_llm"
            )
            st.markdown(chat_result.summary)

            # Display the move history (boards for each move)
            st.subheader("移动历史")
            for i, move_svg in enumerate(st.session_state.move_history):
                # Determine which agent made the move
                if i % 2 == 0:
                    move_by = "白棋代理"  # Even-indexed moves are by White
                else:
                    move_by = "黑棋代理"  # Odd-indexed moves are by Black
                
                st.write(f"移动 {i + 1} 由 {move_by}")
                st.image(move_svg)

        if st.button("Reset Game"):
            st.session_state.board.reset()
            st.session_state.made_move = False
            st.session_state.move_history = []
            st.session_state.board_svg = None
            st.write("游戏重置! 点击 '开始游戏' 开始新游戏。")

    except Exception as e:
        st.error(f"发生错误: {e}. 请检查您的API密钥并重试。")

else:
    st.warning("请在侧边栏输入您的OpenAI API密钥以开始游戏。")