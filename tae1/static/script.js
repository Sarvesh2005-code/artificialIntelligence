const ROWS = 6;
const COLS = 7;
const EMPTY = 0;
const PLAYER_PIECE = 1;
const AI_PIECE = 2;

let gameActive = true;
let isPlayerTurn = true;

// DOM Elements
const boardEl = document.getElementById('game-board');
const turnIndicator = document.getElementById('turn-indicator');
const modal = document.getElementById('game-over-modal');
const winnerText = document.getElementById('winner-text');

// Initialize DOM Board
function renderBoardDOM() {
    boardEl.innerHTML = '';
    for (let c = 0; c < COLS; c++) {
        const colEl = document.createElement('div');
        colEl.className = 'col';
        colEl.dataset.colIndex = c;
        
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

// Update DOM based on Backend array
function updateBoardUI(boardArray) {
    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLS; c++) {
            const colEls = document.querySelectorAll('.col');
            const col = colEls[c];
            const cell = col.children[r]; // children[0] is row 0
            
            cell.className = 'cell';
            if (boardArray[r][c] === PLAYER_PIECE) cell.classList.add('player');
            else if (boardArray[r][c] === AI_PIECE) cell.classList.add('ai');
        }
    }
}

// Click Logic
async function handleColumnClick(col) {
    if (!gameActive || !isPlayerTurn) return;

    // Optimistically lock UI
    isPlayerTurn = false;
    turnIndicator.textContent = 'AI is thinking...';
    turnIndicator.className = 'ai-turn';

    try {
        const response = await fetch('/api/move', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ col: col })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            updateBoardUI(data.board);
            
            if (data.status !== 'ACTIVE') {
                gameActive = false;
                winnerText.textContent = data.message;
                modal.classList.remove('hidden');
            } else {
                // Game continues, unlock UI
                isPlayerTurn = true;
                turnIndicator.textContent = 'Your Turn (Red)';
                turnIndicator.className = 'player-turn';
            }
        } else {
            // Revert state if error (e.g. invalid move full column)
            console.error(data.error);
            isPlayerTurn = true;
            turnIndicator.textContent = 'Your Turn (Red)';
            turnIndicator.className = 'player-turn';
        }
    } catch (error) {
        console.error("Error communicating with Python backend:", error);
    }
}

// Initialize
renderBoardDOM();
