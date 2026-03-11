import numpy as np

# Constants for the game
ROWS = 6
COLS = 7
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

class Connect4Board:
    def __init__(self):
        """Initializes a 6x7 Connect-4 board."""
        self.board = np.zeros((ROWS, COLS), dtype=int)

    def is_valid_location(self, col):
        """
        Checks if a column is available for dropping a piece.
        The top row (index ROWS-1) must be empty.
        """
        return self.board[ROWS - 1][col] == EMPTY

    def get_valid_locations(self):
        """Returns a list of all columns that are not yet full."""
        valid_locations = []
        for col in range(COLS):
            if self.is_valid_location(col):
                valid_locations.append(col)
        return valid_locations

    def get_next_open_row(self, col):
        """Finds the lowest empty row in a given column."""
        for r in range(ROWS):
            if self.board[r][col] == EMPTY:
                return r
        return None  # Should not happen if `is_valid_location` is called first

    def drop_piece(self, row, col, piece):
        """Places a piece at the specified row and column."""
        self.board[row][col] = piece

    def copy(self):
        """Returns a copy of the current board for simulation."""
        new_board = Connect4Board()
        new_board.board = np.copy(self.board)
        return new_board

    def is_win(self, piece):
        """Checks if the specified piece has 4 in a row."""
        # Check horizontal locations
        for c in range(COLS - 3):
            for r in range(ROWS):
                if (self.board[r][c] == piece and 
                    self.board[r][c+1] == piece and 
                    self.board[r][c+2] == piece and 
                    self.board[r][c+3] == piece):
                    return True

        # Check vertical locations
        for c in range(COLS):
            for r in range(ROWS - 3):
                if (self.board[r][c] == piece and 
                    self.board[r+1][c] == piece and 
                    self.board[r+2][c] == piece and 
                    self.board[r+3][c] == piece):
                    return True

        # Check positively sloped diagonals
        for c in range(COLS - 3):
            for r in range(ROWS - 3):
                if (self.board[r][c] == piece and 
                    self.board[r+1][c+1] == piece and 
                    self.board[r+2][c+2] == piece and 
                    self.board[r+3][c+3] == piece):
                    return True

        # Check negatively sloped diagonals
        for c in range(COLS - 3):
            for r in range(3, ROWS):
                if (self.board[r][c] == piece and 
                    self.board[r-1][c+1] == piece and 
                    self.board[r-2][c+2] == piece and 
                    self.board[r-3][c+3] == piece):
                    return True

        return False

    def is_terminal_node(self):
        """Checks if the game has ended (win or draw)."""
        return self.is_win(PLAYER_PIECE) or self.is_win(AI_PIECE) or len(self.get_valid_locations()) == 0

    def print_board(self):
        """Prints the board upside down so row 0 is at the bottom."""
        print(np.flip(self.board, 0))
