import math
from connect4 import Connect4Board, PLAYER_PIECE, AI_PIECE, COLS
from ai import minimax

def play_game(ai_depth=4):
    """
    Starts an interactive Connect-4 game in the terminal.
    Player gets piece 1, AI gets piece 2.
    """
    board = Connect4Board()
    game_over = False
    turn = 0 # 0 for Player, 1 for AI

    print("===============================")
    print("   WELCOME TO CONNECT-4 AI     ")
    print("===============================")
    print(f"Player is '1', AI is '2', Empty is '0'")
    print(f"Columns are numbered 0 through {COLS-1}\n")
    board.print_board()

    while not game_over:
        if turn == 0:
            # --- PLAYER'S TURN ---
            col = -1
            while True:
                try:
                    col_str = input(f"\nPlayer (1), Make your Selection (0-{COLS-1}): ")
                    col = int(col_str)
                    if col < 0 or col >= COLS:
                        print(f"Invalid column. Please enter a number between 0 and {COLS-1}.")
                        continue
                    if not board.is_valid_location(col):
                        print("That column is full! Try another one.")
                        continue
                    break # Valid input
                except ValueError:
                    print("Invalid input. Please enter a number.")
            
            row = board.get_next_open_row(col)
            board.drop_piece(row, col, PLAYER_PIECE)

            if board.is_win(PLAYER_PIECE):
                print("\n===============================")
                print("       PLAYER 1 WINS!!         ")
                print("===============================")
                game_over = True
                
        else:
            # --- AI'S TURN ---
            print("\nAI is thinking...")
            col, minimax_score = minimax(board, ai_depth, -math.inf, math.inf, True)
            
            if col is not None:
                row = board.get_next_open_row(col)
                board.drop_piece(row, col, AI_PIECE)
                print(f"AI drops piece in column {col}")

                if board.is_win(AI_PIECE):
                    print("\n===============================")
                    print("          AI WINS!!            ")
                    print("===============================")
                    game_over = True

        print()
        board.print_board()

        # Check for draw
        if len(board.get_valid_locations()) == 0 and not game_over:
            print("\n===============================")
            print("         IT'S A DRAW!          ")
            print("===============================")
            game_over = True

        turn += 1
        turn = turn % 2

if __name__ == "__main__":
    play_game()
