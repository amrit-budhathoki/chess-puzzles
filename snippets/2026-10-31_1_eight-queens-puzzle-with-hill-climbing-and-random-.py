# Title: Eight Queens Puzzle with Hill Climbing and Random Restarts

# The eight queens puzzle asks: place 8 queens on an 8×8 chessboard so that no two queens attack each other.
# Solution approach: use hill climbing with random restarts. Start with a random placement, then iteratively
# move queens to reduce conflicts. If stuck in a local minimum, restart randomly. This is faster than
# backtracking for large N and demonstrates local search heuristics.

import random

def count_conflicts(board):
    """Count number of attacking queen pairs. board[col] = row."""
    conflicts = 0
    for col1 in range(len(board)):
        for col2 in range(col1 + 1, len(board)):
            row1, row2 = board[col1], board[col2]
            # Same row or diagonal
            if row1 == row2 or abs(row1 - row2) == abs(col1 - col2):
                conflicts += 1
    return conflicts

def hill_climb(n, max_iterations=1000):
    """Hill climbing: move queens to reduce conflicts."""
    board = [random.randint(0, n - 1) for _ in range(n)]
    
    for iteration in range(max_iterations):
        current_conflicts = count_conflicts(board)
        if current_conflicts == 0:
            return board, iteration
        
        best_col, best_row, best_conflicts = -1, -1, current_conflicts
        
        # Try moving each queen to each row
        for col in range(n):
            old_row = board[col]
            for row in range(n):
                if row == old_row:
                    continue
                board[col] = row
                new_conflicts = count_conflicts(board)
                if new_conflicts < best_conflicts:
                    best_conflicts = new_conflicts
                    best_col, best_row = col, row
            board[col] = old_row
        
        # Move to best position if improved
        if best_col >= 0:
            board[best_col] = best_row
        else:
            # No improvement: stuck in local minimum
            return None, iteration
    
    return None, max_iterations

def solve_eight_queens(n, max_restarts=100):
    """Solve N-queens with random restarts."""
    for restart in range(max_restarts):
        board, iterations = hill_climb(n, max_iterations=1000)
        if board is not None:
            return board, restart, iterations
    return None, max_restarts, -1

def print_board(board):
    """Display board with queens."""
    n = len(board)
    for row in range(n):
        line = ""
        for col in range(n):
            if board[col] == row:
                line += "♛ "
            else:
                line += "· "
        print(line)
    print()

# Solve 8-queens
print("Solving 8-Queens Problem with Hill Climbing + Random Restarts\n")
board, restart_count, iteration_count = solve_eight_queens(8, max_restarts=100)

if board:
    print(f"Solution found in restart #{restart_count}, iteration {iteration_count}")
    print(f"Final conflict count: {count_conflicts(board)}\n")
    print_board(board)
    print(f"Queen positions (column -> row): {board}")
else:
    print("No solution found within restart limit")

# Verify solution
if board:
    conflicts = count_conflicts(board)
    print(f"Verification: {conflicts} conflicts (should be 0 for valid solution)")
    
    # Also verify no two queens in same row, col, or diagonal
    rows = set(board)
    diagonals1 = set(board[i] - i for i in range(len(board)))
    diagonals2 = set(board[i] + i for i in range(len(board)))
    
    all_valid = (len(rows) == 8 and len(diagonals1) == 8 and len(diagonals2) == 8)
    print(f"All checks passed: {all_valid}")
