# Title: King Shortest Path Count from Corner to Corner

# A king can move one square in any of 8 directions. We count how many
# distinct shortest paths exist from one corner to the diagonally opposite corner.
# A king at (0,0) needs exactly (n-1) moves to reach (n-1,n-1) on an nxn board.
# The number of shortest paths is C(2n-2, n-1) since we need exactly (n-1) moves
# right and (n-1) moves down out of (2n-2) total moves, with diagonals counting as 1 move.
# We verify by dynamic programming against the closed form.

from math import comb

def count_paths_dp(n):
    """Count king shortest paths from (0,0) to (n-1,n-1) using DP."""
    # dp[i][j] = number of shortest paths to reach (i,j)
    dp = [[0] * n for _ in range(n)]
    dp[0][0] = 1
    
    for i in range(n):
        for j in range(n):
            if i == 0 and j == 0:
                continue
            # King can arrive from 8 directions, but only those that are closer to origin
            paths = 0
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    if di == 0 and dj == 0:
                        continue
                    ni, nj = i - di, j - dj
                    if 0 <= ni < n and 0 <= nj < n:
                        # Only count previous positions that are on shortest path
                        # Distance from origin via (ni,nj) should equal distance via (i,j) - 1
                        dist_prev = max(ni, nj)
                        dist_curr = max(i, j)
                        if dist_prev == dist_curr - 1:
                            paths += dp[ni][nj]
            dp[i][j] = paths
    
    return dp[n-1][n-1]

def count_paths_formula(n):
    """
    King needs exactly (n-1) moves to go from (0,0) to (n-1,n-1).
    Each move is diagonal, right, or down (never left or up on shortest path).
    This is equivalent to arranging (n-1) down-moves and (n-1) right-moves
    in (2n-2) total moves, with diagonals used optimally.
    Answer: C(2n-2, n-1)
    """
    return comb(2*n - 2, n - 1)

# Test and verify
print("King Shortest Paths: Corner to Opposite Corner")
print("=" * 50)
print(f"{'Board Size':<12} {'DP Result':<15} {'Formula':<15} {'Match':<8}")
print("-" * 50)

for n in range(1, 10):
    dp_result = count_paths_dp(n)
    formula_result = count_paths_formula(n)
    match = "✓" if dp_result == formula_result else "✗"
    print(f"{n}x{n}         {dp_result:<15} {formula_result:<15} {match:<8}")

# Visualize a small board with example paths
print("\n" + "=" * 50)
print("Example: 4x4 Board - King paths from (0,0) to (3,3)")
print("=" * 50)
n = 4
dp = [[0] * n for _ in range(n)]
dp[0][0] = 1

for i in range(n):
    for j in range(n):
        if i == 0 and j == 0:
            continue
        paths = 0
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                ni, nj = i - di, j - dj
                if 0 <= ni < n and 0 <= nj < n:
                    dist_prev = max(ni, nj)
                    dist_curr = max(i, j)
                    if dist_prev == dist_curr - 1:
                        paths += dp[ni][nj]
        dp[i][j] = paths

print("\nPath count at each square:")
for i in range(n):
    row = " ".join(f"{dp[i][j]:3d}" for j in range(n))
    print(row)

print(f"\nTotal shortest paths on 4x4: {dp[3][3]}")
print(f"Formula C(2*4-2, 4-1) = C(6,3) = {comb(6, 3)}")
