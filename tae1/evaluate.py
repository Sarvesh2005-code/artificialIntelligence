import time
import random
from connect4 import Connect4Board, PLAYER_PIECE, AI_PIECE
from ai import minimax

def play_random_move(board_obj, piece):
    """Selects a completely random valid move (Baseline opponent)."""
    valid_locations = board_obj.get_valid_locations()
    if not valid_locations:
        return None
    col = random.choice(valid_locations)
    row = board_obj.get_next_open_row(col)
    board_obj.drop_piece(row, col, piece)
    return col

def play_minimax_move(board_obj, piece, depth):
    """Selects a move using the Minimax algorithm."""
    # The AI is looking for AI_PIECE optimally. 
    # If we made it play as PLAYER_PIECE, we would need to pass maximizingPlayer=False.
    # For simplicity, we just assume `piece` is AI_PIECE in this test.
    col, minimax_score = minimax(board_obj, depth, -math.inf, math.inf, True)
    if col is not None:
        row = board_obj.get_next_open_row(col)
        board_obj.drop_piece(row, col, piece)
    return col

import math

def simulate_match(ai_depth=3):
    """
    Simulates a match between the AI (Minimax) and a Random Player.
    AI always plays as AI_PIECE (2). Random plays as PLAYER_PIECE (1).
    Returns the winner (1, 2, or 0 for draw).
    """
    board_obj = Connect4Board()
    turn = random.randint(0, 1) # Randomize who goes first
    
    while not board_obj.is_terminal_node():
        if turn == 0:
            # Random Player's turn
            play_random_move(board_obj, PLAYER_PIECE)
            
            if board_obj.is_win(PLAYER_PIECE):
                return PLAYER_PIECE
            
            turn += 1
            turn = turn % 2
            
        else:
            # AI's turn
            play_minimax_move(board_obj, AI_PIECE, ai_depth)
            
            if board_obj.is_win(AI_PIECE):
                return AI_PIECE
                
            turn += 1
            turn = turn % 2
            
    return 0 # Draw

def evaluate_win_rate(num_games=10, ai_depth=3):
    """
    Runs a batch of games to evaluate the AI's win rate against the baseline.
    """
    print(f"Starting evaluation: {num_games} games. AI (Depth {ai_depth}) vs Random Player.")
    
    ai_wins = 0
    random_wins = 0
    draws = 0
    
    start_time = time.time()
    
    for i in range(num_games):
        winner = simulate_match(ai_depth)
        if winner == AI_PIECE:
            ai_wins += 1
        elif winner == PLAYER_PIECE:
            random_wins += 1
        else:
            draws += 1
            
        # Terminal Progress
        if (i+1) % max(1, num_games//10) == 0:
            print(f"[{i+1}/{num_games}] games completed...")
            
    end_time = time.time()
    avg_time = (end_time - start_time) / num_games
    
    print("\n--- RESULTS ---")
    print(f"AI Wins: {ai_wins} ({(ai_wins/num_games)*100:.1f}%)")
    print(f"Random Wins: {random_wins} ({(random_wins/num_games)*100:.1f}%)")
    print(f"Draws: {draws} ({(draws/num_games)*100:.1f}%)")
    print(f"Average time per game: {avg_time:.3f} seconds\n")

if __name__ == "__main__":
    # We run 20 games to get a quick evaluation (this takes a few seconds)
    evaluate_win_rate(num_games=20, ai_depth=3)
