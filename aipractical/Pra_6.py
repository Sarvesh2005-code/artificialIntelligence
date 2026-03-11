import math

board = [" "] * 9

def check_win(player):
    wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    return any(all(board[i] == player for i in combo) for combo in wins)

def alpha_beta(alpha, beta, is_ai):
    if check_win("X"): return 1
    if check_win("O"): return -1
    if " " not in board: return 0

    if is_ai:
        best = -math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = alpha_beta(alpha, beta, False)
                board[i] = " "
                best = max(score, best)
                alpha = max(alpha, best)
                if beta <= alpha: break
        return best
    else:
        best = math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = alpha_beta(alpha, beta, True)
                board[i] = " "
                best = min(score, best)
                beta = min(beta, best)
                if beta <= alpha: break
        return best

# Game Loop
while " " in board:
    # AI Logic
    best_move = -1
    best_score = -math.inf
    for i in range(9):
        if board[i] == " ":
            board[i] = "X"
            score = alpha_beta(-math.inf, math.inf, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                best_move = i
    
    board[best_move] = "X"
    print(f"{board[0:3]}\n{board[3:6]}\n{board[6:9]}\n")
    
    if check_win("X"):
        print("AI Wins!")
        break

    if " " not in board:
        print("Game Draw!")
        break

    # Human Move
    move = int(input("Pick a spot (0-8): "))
    board[move] = "O"

    if check_win("O"):
        print(f"{board[0:3]}\n{board[3:6]}\n{board[6:9]}\n")
        print("Human Wins!")
        break

    if " " not in board:
        print("Game Draw!")
        break