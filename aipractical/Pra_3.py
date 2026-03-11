board = ["-"] * 9 
 
def show(): 
    print(board[0], board[1], board[2]) 
    print(board[3], board[4], board[5]) 
    print(board[6], board[7], board[8]) 
    print() 
 
def winner(): 
    lines = [ 
        (0,1,2),(3,4,5),(6,7,8), 
        (0,3,6),(1,4,7),(2,5,8), 
        (0,4,8),(2,4,6) 
    ] 
    for a,b,c in lines: 
        if board[a] == board[b] == board[c] != "-": 
            return board[a] 
    if "-" not in board: 
        return "Tie" 
    return None 
 
def minimax(ai): 
    w = winner() 
    if w == "O": return 1 
    if w == "X": return -1 
    if w == "Tie": return 0 
 
    scores = [] 
    for i in range(9): 
        if board[i] == "-": 
            board[i] = "O" if ai else "X" 
            scores.append(minimax(not ai)) 
            board[i] = "-" 
    return max(scores) if ai else min(scores) 
 
def ai_move(): 
    best = -10 
    move = 0 
    for i in range(9): 
        if board[i] == "-": 
            board[i] = "O" 
            score = minimax(False) 
            board[i] = "-" 
            if score > best: 
                best, move = score, i 
    board[move] = "O" 
 
# Game loop 
show() 
while True: 
    p = int(input("Enter 1-9: ")) - 1 
    if board[p] != "-": 
        continue 
    board[p] = "X" 
    show() 
    if winner(): break 
 
    ai_move() 
    print("AI move:") 
    show() 
    if winner(): break 
 
print("Result:", winner())