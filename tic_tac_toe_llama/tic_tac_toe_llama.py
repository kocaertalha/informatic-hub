from llama_cpp import Llama

# Initialize LLaMA from local model file
llm = Llama(model_path="models/llama-2-7b-chat.Q4_K_M.gguf", n_ctx=2048)


def print_board(board):
    for row in board:
        print("|".join(row))
    print()


def check_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(row[col] == player for row in board):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False


def board_full(board):
    return all(cell != " " for row in board for cell in row)


def llama_move(board):
    board_str = "\n".join(["|".join(row) for row in board])
    prompt = f"""
### Instruction: You are playing Tic Tac Toe as O. The board is shown below. The user (X) has made a move. Write the coordinates of your move (row and column) in the format: row,column.

Current Board:
{board_str}

What is your move?
### Response:
"""
    response = llm(prompt, max_tokens=10, echo=False)
    move_text = response["choices"][0]["text"].strip()
    try:
        row, col = map(int, move_text.split(","))
        return row - 1, col - 1
    except Exception:
        print("Invalid model response, picking first empty cell.")
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    return i, j


board = [[" " for _ in range(3)] for _ in range(3)]

print("Let's play Tic Tac Toe! You are X, LLaMA is O.")
print_board(board)

while True:
    # User move
    while True:
        try:
            move = input("Enter your move (row,col): ")
            row, col = map(int, move.split(","))
            row -= 1
            col -= 1
            if board[row][col] == " ":
                board[row][col] = "X"
                break
            else:
                print("Cell already taken!")
        except Exception:
            print("Invalid input. Please enter row,col (e.g., 1,2)")

    print_board(board)

    if check_winner(board, "X"):
        print("🎉 You win!")
        break
    if board_full(board):
        print("It's a draw!")
        break

    # LLaMA move
    print("LLaMA (O) is thinking...")
    o_row, o_col = llama_move(board)
    board[o_row][o_col] = "O"

    print_board(board)

    if check_winner(board, "O"):
        print("LLaMA (O) wins!")
        break
    if board_full(board):
        print("It's a draw!")
        break
