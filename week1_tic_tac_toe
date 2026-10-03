import random

# Initialize the board with 9 empty spaces
board = [" " for _ in range(9)]

def print_board():
    print()
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("-----------")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("-----------")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print()

def check_win(b, player):
    win_combos = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]             # Diagonals
    ]
    return any(all(b[i] == player for i in combo) for combo in win_combos)

def is_full(b):
    return " " not in b

def get_computer_move(b):
    # Beginner AI picks a random empty spot
    empty_spots = [i for i, spot in enumerate(b) if spot == " "]
    return random.choice(empty_spots)

def play_game():
    print("WELCOME TO TIC TAC TOE!")
    print("Choose game mode:")
    print("1. Human vs Human")
    print("2. Human vs Computer")
    
    choice = input("Enter 1 or 2: ").strip()
    vs_computer = (choice == "2")
    
    current_player = "X"
    
    while True:
        print_board()
        
        if vs_computer and current_player == "O":
            print("Computer's turn (O)...")
            move = get_computer_move(board)
        else:
            try:
                move = int(input(f"Player {current_player}, choose position (1-9): ")) - 1
                if move < 0 or move > 8 or board[move] != " ":
                    print("Invalid move. Choose an empty spot between 1 and 9.")
                    continue
            except ValueError:
                print("Please enter a valid number from 1 to 9.")
                continue
                
        board[move] = current_player
        
        if check_win(board, current_player):
            print_board()
            print(f"Player {current_player} wins!")
            break
            
        if is_full(board):
            print_board()
            print("It's a tie!")
            break
            
        current_player = "O" if current_player == "X" else "X"

if __name__ == "__main__":
    play_game()
