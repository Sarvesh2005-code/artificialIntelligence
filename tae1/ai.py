import math
import random
from connect4 import ROWS, COLS, EMPTY, PLAYER_PIECE, AI_PIECE

WINDOW_LENGTH = 4

def evaluate_window(window, piece):
    """
    Evaluates a specific window of 4 slots.
    Returns a score based on how advantageous this window is for the given piece.
    """
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4  # Penalize if the opponent is about to win

    return score

def score_position(board_obj, piece):
    """
    Evaluates the entire board and returns a heuristic score for the given piece.
    """
    score = 0
    board = board_obj.board

    # Score center column (prefer center control)
    center_array = [int(i) for i in list(board[:, COLS//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score Horizontal
    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLS - 3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score Vertical
    for c in range(COLS):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROWS - 3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score positive sloped diagonal
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Score negative sloped diagonal
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def is_terminal_node(board_obj):
    """Determines if the game is over."""
    return board_obj.is_win(PLAYER_PIECE) or board_obj.is_win(AI_PIECE) or len(board_obj.get_valid_locations()) == 0


def minimax(board_obj, depth, alpha, beta, maximizingPlayer):
    """
    Minimax algorithm with Alpha-Beta Pruning.
    Returns: (best_column, score)
    """
    valid_locations = board_obj.get_valid_locations()
    is_terminal = is_terminal_node(board_obj)
    
    # Base cases for recursion
    if depth == 0 or is_terminal:
        if is_terminal:
            if board_obj.is_win(AI_PIECE):
                return (None, 100000000000000)
            elif board_obj.is_win(PLAYER_PIECE):
                return (None, -10000000000000)
            else: # Game is a draw
                return (None, 0)
        else: # Depth is zero, return heuristic score
            return (None, score_position(board_obj, AI_PIECE))

    if maximizingPlayer:
        value = -math.inf
        # Randomize column order slightly to avoid repetitive play when scores are equal
        best_col = random.choice(valid_locations)
        
        for col in valid_locations:
            row = board_obj.get_next_open_row(col)
            b_copy = board_obj.copy()
            b_copy.drop_piece(row, col, AI_PIECE)
            
            # Recurse down the tree
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            
            if new_score > value:
                value = new_score
                best_col = col
                
            # Alpha-Beta Pruning
            alpha = max(alpha, value)
            if alpha >= beta:
                break # Prune the branch
                
        return best_col, value

    else: # Minimizing player (Human/Opponent)
        value = math.inf
        best_col = random.choice(valid_locations)
        
        for col in valid_locations:
            row = board_obj.get_next_open_row(col)
            b_copy = board_obj.copy()
            b_copy.drop_piece(row, col, PLAYER_PIECE)
            
            # Recurse down the tree
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            
            if new_score < value:
                value = new_score
                best_col = col
                
            # Alpha-Beta Pruning
            beta = min(beta, value)
            if alpha >= beta:
                break # Prune the branch
                
        return best_col, value
