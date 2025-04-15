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


def get_mcts_move(board, player_symbol):
    # Placeholder for MCTS agent
    # Currently chooses a random valid move
    valid_moves = [i for i, spot in enumerate(board) if spot == ' ']
    return random.choice(valid_moves)


def main():
    board = [' '] * 9
    player_x_name, player_o_name = generate_player_names()

    print(f"Welcome to Tic-Tac-Toe! Today, {player_x_name} (X) will play against {player_o_name} (O).")

    current_symbol, current_name = 'X', player_x_name

    while ' ' in board:
        display_board(board)
        move = get_mcts_move(board, current_symbol)
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