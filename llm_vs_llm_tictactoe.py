from llama_cpp import Llama
import random


def display_board(board):
    print("\nCurrent board:")
    print(f" {board[0]} | {board[1]} | {board[2]}")
    print("---|---|---")
    print(f" {board[3]} | {board[4]} | {board[5]}")
    print("---|---|---")
    print(f" {board[6]} | {board[7]} | {board[8]}")


def check_winner(board, player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for condition in win_conditions:
        if all(board[pos] == player for pos in condition):
            return True
    return False


def generate_player_names():
    possible_names = [
        "Captain Lightning", "Commander Star", "Admiral Spark", "General Nova",
        "Pilot Blaze", "Agent Eclipse", "Warrior Frost", "Captain Thunder",
        "Guardian Bolt", "Explorer Phoenix", "Commander Vortex", "Strategist Comet"
    ]
    return random.sample(possible_names, 2)


def get_llm_move(llm, board, player_name, player_symbol):
    prompt = (f"The board is: {board}. {player_name} plays as {player_symbol}. Provide the best move as a single "
              f"number between 0 and 8 (empty spots only). Respond with the number only.")
    response = llm(prompt, max_tokens=10)
    text = response['choices'][0]['text'].strip()
    try:
        move = int(text)
        if move in range(9) and board[move] == ' ':
            return move
    except ValueError:
        pass
    return random.choice([i for i, spot in enumerate(board) if spot == ' '])


def main():
    llm = Llama(model_path="models/llama-2-7b-chat.Q4_K_M.gguf")
    board = [' '] * 9
    player_x_name, player_o_name = generate_player_names()

    print(f"Welcome to Tic-Tac-Toe! Today, {player_x_name} (X) will play against {player_o_name} (O).")

    current_player, current_symbol, current_name = 'X', 'X', player_x_name

    while ' ' in board:
        display_board(board)
        move = get_llm_move(llm, board, current_name, current_symbol)
        print(f"\n{current_name} ({current_symbol}) chose: {move}")
        board[move] = current_symbol

        if check_winner(board, current_symbol):
            display_board(board)
            print(f"{current_name} ({current_symbol}) wins!")
            break

        current_symbol, current_name = ('O', player_o_name) if current_symbol == 'X' else ('X', player_x_name)
    else:
        display_board(board)
        print("It's a draw!")


if __name__ == "__main__":
    main()
