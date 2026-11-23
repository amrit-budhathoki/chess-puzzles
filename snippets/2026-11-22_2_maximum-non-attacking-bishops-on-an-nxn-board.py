# Title: Maximum Non-Attacking Bishops on an NxN Board

# Puzzle: Find the maximum number of bishops that can be placed on an NxN chessboard
# such that no two bishops attack each other. Bishops attack diagonally, so two bishops
# on the same diagonal cannot coexist. The key insight: bishops on white squares never
# attack bishops on black squares. So we can solve for each color separately.
# Formula: For an NxN board, max bishops = 2*N - 2 (N-1 on one color, N-1 on the other).
# We verify by brute-force backtracking on small boards and compare with the formula.

def bishops_on_color(n, color_parity):
    """
    Count max non-attacking bishops on squares of a single color.
    color_parity: 0 for (row+col) even, 1 for (row+col) odd.
    Strategy: place bishops along edges where they don't share diagonals.
    """
    bishops = []
    # Place bishops along top and bottom edges (and left edge)
    for row in range(n):
        for col in range(n):
            if (row + col) % 2 == color_parity:
                # Check if this bishop conflicts with already placed bishops
                valid = True
                for br, bc in bishops:
                    # Two bishops conflict if on same diagonal
                    if row - col == br - bc or row + col == br + bc:
                        valid = False
                        break
                if valid:
                    bishops.append((row, col))
    return bishops

def max_bishops_greedy(n):
    """Greedy placement: fill white squares, then black squares."""
    white = bishops_on_color(n, 0)
    black = bishops_on_color(n, 1)
    return white + black

def max_bishops_formula(n):
    """Formula: on an NxN board, max non-attacking bishops = 2*N - 2."""
    return 2 * n - 2

def backtrack_max_bishops(n, row=0, col=0, bishops=None, diag_set=None):
    """Brute-force backtracking to find actual maximum (slow for large N)."""
    if bishops is None:
        bishops = []
        diag_set = set()
    
    if row == n:
        return len(bishops)
    
    next_row, next_col = (row, col + 1) if col + 1 < n else (row + 1, 0)
    
    # Try placing a bishop at (row, col)
    diag1 = row - col
    diag2 = row + col
    max_with = 0
    if diag1 not in diag_set and diag2 not in diag_set:
        bishops.append((row, col))
        diag_set.add(diag1)
        diag_set.add(diag2)
        max_with = backtrack_max_bishops(n, next_row, next_col, bishops, diag_set)
        bishops.pop()
        diag_set.discard(diag1)
        diag_set.discard(diag2)
    
    # Try not placing a bishop
    max_without = backtrack_max_bishops(n, next_row, next_col, bishops, diag_set)
    
    return max(max_with, max_without)

def draw_board(n, bishops):
    """Draw NxN board with bishops marked."""
    board = [['.' for _ in range(n)] for _ in range(n)]
    for r, c in bishops:
        board[r][c] = 'B'
    for row in board:
        print(' '.join(row))

print("Maximum Non-Attacking Bishops on NxN Board\n")
print("Formula: max_bishops(N) = 2*N - 2\n")

for n in range(2, 9):
    formula_result = max_bishops_formula(n)
    greedy_result = len(max_bishops_greedy(n))
    
    if n <= 5:
        # Verify with brute force for small boards
        brute_result = backtrack_max_bishops(n)
        match = "✓" if formula_result == brute_result else "✗"
        print(f"N={n}: Formula={formula_result}, Brute-force={brute_result} {match}")
    else:
        print(f"N={n}: Formula={formula_result}, Greedy={greedy_result}")

print("\nExample: 5x5 board with maximum bishops")
bishops = max_bishops_greedy(5)
draw_board(5, bishops)
print(f"Total bishops: {len(bishops)}")
