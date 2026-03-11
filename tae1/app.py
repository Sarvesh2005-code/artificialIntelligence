from flask import Flask, render_template, request, jsonify
from connect4 import Connect4Board, PLAYER_PIECE, AI_PIECE
import ai
import math

app = Flask(__name__)

# Global state for simplicity in this demonstration. 
# In production, use session data or a database to handle concurrent users.
game_board = Connect4Board()

@app.route('/')
def index():
    # Reset game on load
    global game_board
    game_board = Connect4Board()
    return render_template('index.html')

@app.route('/api/move', methods=['POST'])
def make_move():
    global game_board
    data = request.json
    col = data.get('col')
    
    # 1. Player Move
    if col is None or not game_board.is_valid_location(col):
        return jsonify({"error": "Invalid move"}), 400
        
    row = game_board.get_next_open_row(col)
    game_board.drop_piece(row, col, PLAYER_PIECE)
    
    # Check if player won
    if game_board.is_win(PLAYER_PIECE):
        return jsonify({
            "board": game_board.board.tolist(), 
            "status": "PLAYER_WIN",
            "message": "You Win! 🎉"
        })
        
    if len(game_board.get_valid_locations()) == 0:
        return jsonify({
            "board": game_board.board.tolist(), 
            "status": "DRAW",
            "message": "It's a Draw!"
        })

    # 2. AI Move
    # We use depth 5 here to ensure the web request doesn't timeout.
    col_ai, score = ai.minimax(game_board, 5, -math.inf, math.inf, True)
    
    if col_ai is not None:
        row_ai = game_board.get_next_open_row(col_ai)
        game_board.drop_piece(row_ai, col_ai, AI_PIECE)

        if game_board.is_win(AI_PIECE):
            return jsonify({
                "board": game_board.board.tolist(), 
                "status": "AI_WIN",
                "message": "AI Wins! 🤖"
            })
            
        if len(game_board.get_valid_locations()) == 0:
            return jsonify({
                "board": game_board.board.tolist(), 
                "status": "DRAW",
                "message": "It's a Draw!"
            })
            
    # Continue game
    return jsonify({
        "board": game_board.board.tolist(),
        "status": "ACTIVE"
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
