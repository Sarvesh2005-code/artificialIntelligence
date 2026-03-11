const ROWS = 6;
const COLS = 7;
const EMPTY = 0;
const PLAYER_PIECE = 1;
const AI_PIECE = 2;
const WINDOW_LENGTH = 4;

let board = [];
let gameActive = true;
let isPlayerTurn = true;

// DOM Elements
const boardEl = document.getElementById('game-board');
const turnIndicator = document.getElementById('turn-indicator');
const modal = document.getElementById('game-over-modal');
const winnerText = document.getElementById('winner-text');
const resetBtn = document.getElementById('reset-btn');
const modalResetBtn = document.getElementById('modal-reset-btn');

// Initialize Board Data Structure
function createBoard() {
    board = Array.from({ length: ROWS }, () => Array(COLS).fill(EMPTY));
}

// Generate DOM Board
function renderBoardDOM() {
    boardEl.innerHTML = '';
    // Create columns first (because CSS flex column-reverse stack)
    for (let c = 0; c < COLS; c++) {
        const colEl = document.createElement('div');
        colEl.className = 'col';
        colEl.dataset.colIndex = c;
        
        // Add click listener to columns
        colEl.addEventListener('click', () => handleColumnClick(c));

        for (let r = 0; r < ROWS; r++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.dataset.row = r;
            cell.dataset.col = c;
            colEl.appendChild(cell);
        }
        boardEl.appendChild(colEl);
    }
}

function updateBoardUI() {
    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLS; c++) {
            // Find the cell (remember the col is the wrapper and cells go from row 0 at bottom)
            const colEls = document.querySelectorAll('.col');
            const col = colEls[c];
            const cell = col.children[r]; // children[0] is row 0

            cell.className = 'cell';
            if (board[r][c] === PLAYER_PIECE) cell.classList.add('player');
            else if (board[r][c] === AI_PIECE) cell.classList.add('ai');
        }
    }
}

// Validation & Placement
function isValidLocation(b, col) {
    return b[ROWS - 1][col] === EMPTY;
}

function getValidLocations(b) {
    return Array.from({length: COLS}, (_, c) => c).filter(c => isValidLocation(b, c));
}

function getNextOpenRow(b, col) {
    for (let r = 0; r < ROWS; r++) {
        if (b[r][col] === EMPTY) return r;
    }
    return null;
}

function dropPiece(b, row, col, piece) {
    b[row][col] = piece;
}

// Win Detection
function isWin(b, piece) {
    // Horizontal
    for (let c = 0; c < COLS - 3; c++) {
        for (let r = 0; r < ROWS; r++) {
            if (b[r][c] === piece && b[r][c+1] === piece && b[r][c+2] === piece && b[r][c+3] === piece) return true;
        }
    }
    // Vertical
    for (let c = 0; c < COLS; c++) {
        for (let r = 0; r < ROWS - 3; r++) {
            if (b[r][c] === piece && b[r+1][c] === piece && b[r+2][c] === piece && b[r+3][c] === piece) return true;
        }
    }
    // Positive Diagonal
    for (let c = 0; c < COLS - 3; c++) {
        for (let r = 0; r < ROWS - 3; r++) {
            if (b[r][c] === piece && b[r+1][c+1] === piece && b[r+2][c+2] === piece && b[r+3][c+3] === piece) return true;
        }
    }
    // Negative Diagonal
    for (let c = 0; c < COLS - 3; c++) {
        for (let r = 3; r < ROWS; r++) {
            if (b[r][c] === piece && b[r-1][c+1] === piece && b[r-2][c+2] === piece && b[r-3][c+3] === piece) return true;
        }
    }
    return false;
}

function isTerminalNode(b) {
    return isWin(b, PLAYER_PIECE) || isWin(b, AI_PIECE) || getValidLocations(b).length === 0;
}

// -----------------------------------------------------
// AI Logic (Ported from Python)
// -----------------------------------------------------

function evaluateWindow(window, piece) {
    let score = 0;
    let oppPiece = (piece === PLAYER_PIECE) ? AI_PIECE : PLAYER_PIECE;

    const countPiece = window.filter(x => x === piece).length;
    const countEmpty = window.filter(x => x === EMPTY).length;
    const countOpp = window.filter(x => x === oppPiece).length;

    if (countPiece === 4) score += 100;
    else if (countPiece === 3 && countEmpty === 1) score += 5;
    else if (countPiece === 2 && countEmpty === 2) score += 2;

    if (countOpp === 3 && countEmpty === 1) score -= 4;

    return score;
}

function scorePosition(b, piece) {
    let score = 0;

    // Center Column
    let centerArray = [];
    let centerColIndex = Math.floor(COLS/2);
    for(let r=0; r<ROWS; r++) centerArray.push(b[r][centerColIndex]);
    const centerCount = centerArray.filter(x => x === piece).length;
    score += centerCount * 3;

    // Horizontal
    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLS - 3; c++) {
            const window = [b[r][c], b[r][c+1], b[r][c+2], b[r][c+3]];
            score += evaluateWindow(window, piece);
        }
    }

    // Vertical
    for (let c = 0; c < COLS; c++) {
        for (let r = 0; r < ROWS - 3; r++) {
            const window = [b[r][c], b[r+1][c], b[r+2][c], b[r+3][c]];
            score += evaluateWindow(window, piece);
        }
    }

    // Pos Diagonal
    for (let r = 0; r < ROWS - 3; r++) {
        for (let c = 0; c < COLS - 3; c++) {
            const window = [b[r][c], b[r+1][c+1], b[r+2][c+2], b[r+3][c+3]];
            score += evaluateWindow(window, piece);
        }
    }

    // Neg Diagonal
    for (let r = 0; r < ROWS - 3; r++) {
        for (let c = 0; c < COLS - 3; c++) {
            const window = [b[r+3][c], b[r+2][c+1], b[r+1][c+2], b[r][c+3]];
            score += evaluateWindow(window, piece);
        }
    }

    return score;
}

function cloneBoard(b) {
    return b.map(row => [...row]);
}

function minimax(b, depth, alpha, beta, maximizingPlayer) {
    const validLocs = getValidLocations(b);
    const isTerminal = isTerminalNode(b);

    if (depth === 0 || isTerminal) {
        if (isTerminal) {
            if (isWin(b, AI_PIECE)) return [null, 10000000];
            if (isWin(b, PLAYER_PIECE)) return [null, -10000000];
            return [null, 0];
        } else {
            return [null, scorePosition(b, AI_PIECE)];
        }
    }

    if (maximizingPlayer) {
        let value = -Infinity;
        let column = validLocs[Math.floor(Math.random() * validLocs.length)];
        for (let col of validLocs) {
            let row = getNextOpenRow(b, col);
            let bCopy = cloneBoard(b);
            dropPiece(bCopy, row, col, AI_PIECE);
            let newScore = minimax(bCopy, depth - 1, alpha, beta, false)[1];
            if (newScore > value) {
                value = newScore;
                column = col;
            }
            alpha = Math.max(alpha, value);
            if (alpha >= beta) break;
        }
        return [column, value];
    } else {
        let value = Infinity;
        let column = validLocs[Math.floor(Math.random() * validLocs.length)];
        for (let col of validLocs) {
            let row = getNextOpenRow(b, col);
            let bCopy = cloneBoard(b);
            dropPiece(bCopy, row, col, PLAYER_PIECE);
            let newScore = minimax(bCopy, depth - 1, alpha, beta, true)[1];
            if (newScore < value) {
                value = newScore;
                column = col;
            }
            beta = Math.min(beta, value);
            if (alpha >= beta) break;
        }
        return [column, value];
    }
}

// -----------------------------------------------------
// Game Loop
// -----------------------------------------------------

function handleColumnClick(col) {
    if (!gameActive || !isPlayerTurn) return;
    if (!isValidLocation(board, col)) return;

    // Player Move
    const row = getNextOpenRow(board, col);
    dropPiece(board, row, col, PLAYER_PIECE);
    updateBoardUI();

    if (isWin(board, PLAYER_PIECE)) {
        endGame("You Win! 🎉");
        return;
    }
    
    if (getValidLocations(board).length === 0) {
        endGame("It's a Draw!");
        return;
    }

    // Switch turn
    isPlayerTurn = false;
    turnIndicator.textContent = 'AI is thinking...';
    turnIndicator.className = 'ai-turn';

    // Delayed AI Move to allow UI update
    setTimeout(makeAIMove, 50);
}

function makeAIMove() {
    if (!gameActive) return;

    // Depth 6 runs very fast in modern JS engines, depth 7 might stutter a bit. Let's stick to 6 for instant feel.
    const [bestCol, score] = minimax(board, 6, -Infinity, Infinity, true);

    if (bestCol !== null) {
        const row = getNextOpenRow(board, bestCol);
        dropPiece(board, row, bestCol, AI_PIECE);
        updateBoardUI();

        if (isWin(board, AI_PIECE)) {
            endGame("AI Wins! 🤖");
            return;
        }
        
        if (getValidLocations(board).length === 0) {
            endGame("It's a Draw!");
            return;
        }
    }

    isPlayerTurn = true;
    turnIndicator.textContent = 'Your Turn (Red)';
    turnIndicator.className = 'player-turn';
}

function endGame(msg) {
    gameActive = false;
    winnerText.textContent = msg;
    modal.classList.remove('hidden');
}

function startGame() {
    createBoard();
    renderBoardDOM();
    gameActive = true;
    isPlayerTurn = true;
    turnIndicator.textContent = 'Your Turn (Red)';
    turnIndicator.className = 'player-turn';
    modal.classList.add('hidden');
}

resetBtn.addEventListener('click', startGame);
modalResetBtn.addEventListener('click', startGame);

// Initialize
startGame();
