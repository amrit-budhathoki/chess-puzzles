# Title: N-Queens Problem with Backtracking

# The N-Queens problem asks: place N queens on an NxN chessboard such that no two queens
# attack each other (no two queens share a row, column, or diagonal).
# We use backtracking: place queens row by row, and prune branches where conflicts occur.
# For each row, we try each column and check if it's safe before recursing.

def is_safe(board, row, col):
    """Check if placing a queen at (row, col) is safe."""
    # Check column (all previous rows)
    for i in range(row):
        if board[i] == col:
            return False
    
    # Check diagonals
    for i in range(row):
        if abs(board[i] - col) == abs(i - row):
            return False
    
    return True

def solve_n_queens(n, board=None, row=0, solutions=None):
    """Backtracking solver for N-Queens. board[i] = column of queen in row i."""
    if board is None:
        board = [-1] * n
        solutions = []
    
    if row == n:
        solutions.append(board[:])
        return solutions
    
    for col in range(n):
        if is_safe(board, row, col):
            board[row] = col
            solve_n_queens(n, board, row + 1, solutions)
            board[row] = -1
    
    return solutions

def print_board(solution):
    """Print a single solution as a chessboard."""
    n = len(solution)
    for row in range(n):
        line = ""
        for col in range(n):
            if solution[row] == col:
                line += "Q "
            else:
                line += ". "
        print(line)
    print()

def count_n_queens(n):
    """Count total solutions for N-Queens (brute force)."""
    solutions = solve_n_queens(n)
    return len(solutions)

# Test and verify
print("N-Queens Problem Solutions\n")
print("=" * 40)

test_cases = [4, 5, 6, 8]
known_counts = {4: 2, 5: 10, 6: 4, 8: 92}

for n in test_cases:
    count = count_n_queens(n)
    expected = known_counts[n]
    status = "✓" if count == expected else "✗"
    print(f"N={n}: {count} solutions (expected {expected}) {status}")

print("\n" + "=" * 40)
print("First 3 solutions for N=4:\n")

solutions_4 = solve_n_queens(4)
for i, sol in enumerate(solutions_4[:3]):
    print(f"Solution {i+1}:")
    print_board(sol)

print(f"Total solutions for N=4: {len(solutions_4)}")
