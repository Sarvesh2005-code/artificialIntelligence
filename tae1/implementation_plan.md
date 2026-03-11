# AI Game Bot for Connect-4: Implementation Plan

## Problem Definition
Develop an intelligent gameplay bot capable of playing Connect-4 optimally or near-optimally using a game-tree-based heuristic search, evaluated via a win-rate metric against a baseline or human player.

## Phase 1: Core Problem & Environment Setup
- **Objective:** Create the game engine and establish the rules.
- **Tasks:**
  - Define the board state representation (e.g., 6x7 2D numpy array or integer representations).
  - Implement move generation (identifying open columns to validly drop a piece).
  - Implement the "drop piece" transition function to generate child states.
  - Create win/draw condition checkers (horizontal, vertical, diagonal checks).
  - Build a simple Command Line Interface (CLI) to visualize the board and allow interactive play.

## Phase 2: Heuristic Evaluation Function Design
- **Objective:** Teach the AI how to score non-terminal, intermediate board states.
- **Tasks:**
  - Create scoring mechanisms for individual lines (e.g., arrays of 4 slots).
  - Assign higher scores to the center column (as it offers structurally more connection possibilities).
  - Implement pattern matching/scoring loops for counting 2, 3, and 4 tokens in a row.
  - Heavily penalize the scenario where the opponent is one move away from winning (threat mitigation).
  - Fine-tune heuristic scoring weights (e.g., +100 for a 4-in-a-row, -80 for opponent's 3-in-a-row).

## Phase 3: Minimax Algorithm Implementation
- **Objective:** Develop the core recursive game-tree search.
- **Tasks:**
  - Write the `minimax(board, depth, maximizingPlayer)` recursive function.
  - Define the base case: Terminal state (win/lose/draw) or maximum tree depth reached.
  - For the AI player (maximizing component): Iterate over valid moves, recursively call Minimax on child states, and track the maximum evaluation score.
  - For the Opponent (minimizing component): Iterate over valid moves, call Minimax, and track the minimum evaluation score to simulate optimal counterplay.

## Phase 4: Optimization via Alpha-Beta Pruning
- **Objective:** Reduce search space by pruning branches, significantly boosting execution speed and effective search depth constraint.
- **Tasks:**
  - Modify the Minimax algorithm to accept `alpha` and `beta` parameters.
  - Implement the cutoff/pruning logic: `if alpha >= beta: break` to exit evaluation loops tracking guaranteed suboptimal paths.
  - Implement "move ordering" (evaluating center columns before outer columns) to maximize the likelihood of early cutoffs, radically improving pruning efficiency.
  - *(Optional)* Implement iterative deepening to ensure the best possible move is returned prior to a time-limit expiration.

## Phase 5: Win-rate Evaluation & Outcome Reporting
- **Objective:** Measure AI performance and satisfy the outcome requirements.
- **Tasks:**
  - Develop an automated test bench to simulate batches of matches.
  - Pit variants against each other (e.g., Minimax Depth 5 vs. Minimax Depth 3 vs. Pure Random Mover).
  - Run simulations spanning >100 games asynchronously or sequentially.
  - Log, calculate, and visualize:
    - Overall Win-Rate Evaluation (e.g., AI won 95% of matches vs baseline).
    - Average move latency in milliseconds.
    - Prune efficiency (Total Nodes Evaluated vs Total Pruned).
