import streamlit as st
import random

# Emoji for players
PLAYER_X_EMOJI = "❌"
PLAYER_O_EMOJI = "⭕"

def initialize_game():
    return {
        "dashboard": [" "] * 9,
        "game_on": True,
        "winner": None,
        "current_player": "X",
        "player1": "",
        "player2": "",
        "game_mode": None
    }

def display_dashboard(dashboard):
    board = [PLAYER_X_EMOJI if cell == 'X' else PLAYER_O_EMOJI if cell == 'O' else '&nbsp;' for cell in dashboard]

    board_html = f"""
    <div style="display: flex; justify-content: center; align-items: center; height: 200px;">
        <table style="border-collapse: collapse; font-size: 24px; font-weight: bold;">
            <tr>
                <td style="width: 60px; height: 60px; text-align: center; vertical-align: middle; border: 2px solid #333;">{board[0]}</td>
                <td style="width: 60px; height: 60px; text-align: center; vertical-align: middle; border: 2px solid #333;">{board[1]}</td>
                <td style="width: 60px; height: 60px; text-align: center; vertical-align: middle; border: 2px solid #333;">{board[2]}</td>
            </tr>
            <tr>
                <td style="width: 60px; height: 60px; text-align: center; vertical-align: middle; border: 2px solid #333;">{board[3]}</td>
                <td style="width: 60px; height: 60px; text-align: center; vertical-align: middle; border: 2px solid #333;">{board[4]}</td>
                <td style="width: 60px; height: 60px; text-align: center; vertical-align: middle; border: 2px solid #333;">{board[5]}</td>
            </tr>
            <tr>
                <td style="width: 60px; height: 60px; text-align: center; vertical-align: middle; border: 2px solid #333;">{board[6]}</td>
                <td style="width: 60px; height: 60px; text-align: center; vertical-align: middle; border: 2px solid #333;">{board[7]}</td>
                <td style="width: 60px; height: 60px; text-align: center; vertical-align: middle; border: 2px solid #333;">{board[8]}</td>
            </tr>
        </table>
    </div>
    """
    return board_html

def check_for_winner(dashboard):
    win_conditions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)  # Diagonals
    ]
    for a, b, c in win_conditions:
        if dashboard[a] == dashboard[b] == dashboard[c] != " ":
            return dashboard[a]
    return None

def minimax(board, depth, is_maximizing):
    scores = {'X': -1, 'O': 1, 'tie': 0}
    result = check_for_winner(board)

    if result:
        return scores[result]
    if " " not in board:
        return scores['tie']

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == " ":
                board[i] = 'O'
                score = minimax(board, depth + 1, False)
                board[i] = " "
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == " ":
                board[i] = 'X'
                score = minimax(board, depth + 1, True)
                board[i] = " "
                best_score = min(score, best_score)
        return best_score

def smart_computer_move(dashboard):
    best_score = -float('inf')
    best_move = None
    for i in range(9):
        if dashboard[i] == " ":
            dashboard[i] = 'O'
            score = minimax(dashboard, 0, False)
            dashboard[i] = " "
            if score > best_score:
                best_score = score
                best_move = i
    return best_move

def normal_computer_move(dashboard):
    empty_cells = [i for i, cell in enumerate(dashboard) if cell == " "]
    return random.choice(empty_cells) if empty_cells else None

def main():
    st.set_page_config(page_title="Tic Tac Toe", page_icon="🎮")
    st.title("🎮 Tic Tac Toe")

    # Sidebar information
    st.sidebar.info(
        "Welcome to Tic Tac Toe! This application allows you to play Tic Tac Toe against another player or a computer.\n\n"
        "How to use:\n"
        "1. Choose your game mode from the options provided.\n"
        "2. Enter player names if you're playing Player vs Player.\n"
        "3. Make your moves by entering a number from 1 to 9 corresponding to the grid positions.\n\n"
        "Enjoy the game!"
    )

    st.sidebar.divider()
    st.sidebar.write(
        "Developed🚀 by **Rakesh Kumar**\n"
        "\n Feel free to connect and share your feedback(✨)"
        "\n on LinkedIn: [LinkedIn Profile](https://www.linkedin.com/in/tech-rakesh-ai)"
    )
    st.sidebar.divider()
    st.sidebar.text('© 2024 Tic Tac Toe Game.')

    if 'game_state' not in st.session_state:
        st.session_state.game_state = initialize_game()

    game_state = st.session_state.game_state

    if st.button("Return to Main Menu"):
        st.session_state.game_state = initialize_game()
        st.rerun()

    if not game_state['game_mode']:
        st.subheader("Choose Game Mode")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Player vs Player"):
                game_state['game_mode'] = 'PvP'
                st.rerun()
        with col2:
            if st.button("Player vs Normal Computer"):
                game_state['game_mode'] = 'PvNC'
                st.rerun()
        with col3:
            if st.button("Player vs Smart Computer(AI)"):
                game_state['game_mode'] = 'PvSC'
                st.rerun()

        # Instructions for game modes
        st.subheader("Instructions")
        instructions = """
        **Player vs Player (PvP):** Play against another player.

        **Player vs Normal Computer (PvNC):** This is a simple mechanism; the computer will move randomly into any unfilled position.

        **Player vs Smart Computer (PvSC):** This Smart Computer AI will never lose the game from the player; either the game will win for the Smart Computer or it will end in a draw! If you don't trust this, please try it.
        """
        st.markdown(instructions)

    elif not game_state['player1'] or not game_state['player2']:
        st.subheader("Enter Player Names")
        game_state['player1'] = st.text_input("Player 1 Name (X)", key="player1")
        if game_state['game_mode'] == 'PvP':
            game_state['player2'] = st.text_input("Player 2 Name (O)", key="player2")
        else:
            game_state['player2'] = "Computer"
        if st.button("Start Game") and game_state['player1'] and game_state['player2']:
            st.rerun()

    else:
        st.subheader(f"{game_state['player1']} (X) vs {game_state['player2']} (O)")
        st.markdown(display_dashboard(game_state['dashboard']), unsafe_allow_html=True)

        if game_state['game_on']:
            current_player = game_state['player1'] if game_state['current_player'] == 'X' else game_state['player2']
            st.write(f"Current turn: {current_player} ({game_state['current_player']})")

            if (game_state['game_mode'] == 'PvP' or
                    (game_state['game_mode'] in ['PvNC', 'PvSC'] and game_state['current_player'] == 'X')):
                move = st.number_input("Enter your move (1-9):", min_value=1, max_value=9, step=1)
                if st.button("Make Move"):
                    if game_state['dashboard'][move - 1] == " ":
                        game_state['dashboard'][move - 1] = game_state['current_player']
                        game_state['winner'] = check_for_winner(game_state['dashboard'])

                        # Check if the game is over after player's move
                        if game_state['winner'] or " " not in game_state['dashboard']:
                            game_state['game_on'] = False  # Set the game to over
                        else:
                            game_state['current_player'] = 'O' if game_state['current_player'] == 'X' else 'X'
                            st.rerun()
                    else:
                        st.error("That position is already taken. Try another one.")

            elif game_state['game_mode'] == 'PvNC' and game_state['current_player'] == 'O':
                move = normal_computer_move(game_state['dashboard'])
                if move is not None:
                    game_state['dashboard'][move] = 'O'
                    game_state['winner'] = check_for_winner(game_state['dashboard'])

                    # Check if the game is over after computer's move
                    if game_state['winner'] or " " not in game_state['dashboard']:
                        game_state['game_on'] = False  # Set the game to over
                    else:
                        game_state['current_player'] = 'X'
                    st.rerun()

            elif game_state['game_mode'] == 'PvSC' and game_state['current_player'] == 'O':
                move = smart_computer_move(game_state['dashboard'])
                if move is not None:
                    game_state['dashboard'][move] = 'O'
                    game_state['winner'] = check_for_winner(game_state['dashboard'])

                    # Check if the game is over after computer's move
                    if game_state['winner'] or " " not in game_state['dashboard']:
                        game_state['game_on'] = False  # Set the game to over
                    else:
                        game_state['current_player'] = 'X'
                    st.rerun()

            # Check for a winner after each move
            game_state['winner'] = check_for_winner(game_state['dashboard'])

            # Check if the game is over
            if game_state['winner'] or " " not in game_state['dashboard']:
                game_state['game_on'] = False  # Set the game to over
                st.rerun()

        # This will display the result when the game is over
        if not game_state['game_on']:  # Check if the game is over
            if game_state['winner']:
                winner_name = game_state['player1'] if game_state['winner'] == 'X' else game_state['player2']
                st.success(f"{winner_name} wins!")
            else:
                st.success("It's a tie! 😉")
            if st.button("Play Again"):
                game_state = initialize_game()
                st.session_state.game_state = game_state
                st.rerun()

if __name__ == "__main__":
    main()
