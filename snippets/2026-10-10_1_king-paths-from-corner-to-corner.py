# Title: King Paths from Corner to Corner

# A king can move one square in any direction (including diagonals).
# We count the number of shortest paths from one corner (0,0) to the opposite corner (7,7).
# A shortest path requires exactly 7 moves (moving right or down each time, optimally).
# This is equivalent to counting paths in a grid where we must move 7 steps right and 7 steps down,
# which is C(14,7) = 3432. We verify with dynamic programming for small boards.

def count_king_paths_formula(n):
    """
    On an n×n board, shortest path from (0,0) to (n-1,n-1) requires n-1 moves.
    A king can move diagonally, so we need exactly n-1 moves right/down combined.
    Each move is one of: right, down, or diagonal (right+down).
    This is equivalent to distributing n-1 steps where each step covers 1 unit horizontally,
    vertically, or both. Using combinatorics: C(2*(n-1), n-1)
    """
    from math import comb
    return comb(2 * (n - 1), n - 1)

def count_king_paths_dp(n):
    """
    Dynamic programming: count paths to each square.
    A king can reach (i,j) from (i-1,j), (i,j-1), or (i-1,j-1).
    """
    dp = [[0] * n for _ in range(n)]
    dp[0][0] = 1
    
    for i in range(n):
        for j in range(n):
            if i == 0 and j == 0:
                continue
            paths = 0
            if i > 0:
                paths += dp[i-1][j]
            if j > 0:
                paths += dp[i][j-1]
            if i > 0 and j > 0:
                paths += dp[i-1][j-1]
            dp[i][j] = paths
    
    return dp[n-1][n-1]

def visualize_king_paths(n):
    """Visualize the number of paths to each square on a small board."""
    dp = [[0] * n for _ in range(n)]
    dp[0][0] = 1
    
    for i in range(n):
        for j in range(n):
            if i == 0 and j == 0:
                continue
            paths = 0
            if i > 0:
                paths += dp[i-1][j]
            if j > 0:
                paths += dp[i][j-1]
            if i > 0 and j > 0:
                paths += dp[i-1][j-1]
            dp[i][j] = paths
    
    print(f"King paths on {n}×{n} board:")
    for row in dp:
        print("  " + "  ".join(f"{val:6d}" for val in row))
    return dp[n-1][n-1]

# Test the formula against brute force for small boards
print("Verification (formula vs brute force):")
for size in range(2, 7):
    formula_result = count_king_paths_formula(size)
    dp_result = count_king_paths_dp(size)
    match = "✓" if formula_result == dp_result else "✗"
    print(f"  {size}×{size}: formula={formula_result:6d}, dp={dp_result:6d} {match}")

print()
print("=" * 50)

# Solve for standard 8×8 chessboard
board_size = 8
result_formula = count_king_paths_formula(board_size)
result_dp = count_king_paths_dp(board_size)

print(f"\n8×8 Chessboard - King paths from (0,0) to (7,7):")
print(f"  Formula result:    {result_formula:,}")
print(f"  DP verification:   {result_dp:,}")
print(f"  Match: {'YES' if result_formula == result_dp else 'NO'}")

print(f"\nThe king needs exactly 7 moves minimum (moving diagonally when possible).")
print(f"This equals choosing which 7 of the 14 half-moves are 'diagonal':")
print(f"  C(14, 7) = {result_formula:,}")

# Show a smaller board for visualization
print("\n" + "=" * 50)
print("\nVisualization on 5×5 board:")
visualize_king_paths(5)
