# Title: N-Queens Solutions Counter with Verification

# The N-Queens problem asks: in how many ways can N queens be placed on an NxN board
# such that no two queens attack each other? We use backtracking to count all solutions
# for small N, verify against known formulas, and display sample solutions visually.

def count_n_queens(n):
    """Count all valid N-Queens solutions using backtracking."""
    solutions = []
    
    def is_safe(board, row, col):
        # Check column
        for i in range(row):
            if board[i] == col:
                return False
        # Check diagonals
        for i in range(row):
            if abs(board[i] - col) == abs(i - row):
                return False
        return True
    
    def backtrack(board, row):
        if row == n:
            solutions.append(board[:])
            return
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                backtrack(board, row + 1)
    
    backtrack([-1] * n, 0)
    return solutions

def draw_board(solution):
    """Draw an N-Queens solution as text."""
    n = len(solution)
    board = [['.' for _ in range(n)] for _ in range(n)]
    for row, col in enumerate(solution):
        board[row][col] = 'Q'
    for row in board:
        print(' '.join(row))
    print()

def verify_known_values():
    """Verify against known N-Queens solution counts."""
    known = {1: 1, 2: 0, 3: 0, 4: 2, 5: 10, 6: 4, 7: 40, 8: 92}
    print("N-Queens Solution Counts:")
    print("-" * 40)
    all_correct = True
    for n in range(1, 9):
        solutions = count_n_queens(n)
        count = len(solutions)
        expected = known[n]
        status = "✓" if count == expected else "✗"
        print(f"N={n}: {count:3d} solutions {status}")
        if count != expected:
            all_correct = False
    print("-" * 40)
    return all_correct

def main():
    print("N-Queens Puzzle Solver\n")
    
    # Verify correctness
    if verify_known_values():
        print("\nAll values match known solutions!\n")
    else:
        print("\nMismatch detected!\n")
    
    # Show sample solutions for N=4 and N=5
    for n in [4, 5]:
        solutions = count_n_queens(n)
        print(f"Sample solution for {n}-Queens (out of {len(solutions)}):")
        if solutions:
            draw_board(solutions[0])
    
    # Larger computation
    print("Computing larger cases...")
    for n in [6, 7, 8]:
        solutions = count_n_queens(n)
        print(f"N={n}: {len(solutions)} total solutions")

if __name__ == "__main__":
    main()
