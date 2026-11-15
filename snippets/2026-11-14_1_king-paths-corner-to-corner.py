# Title: King Paths Corner to Corner

# Puzzle: Count the number of ways a king can move from one corner of an 8x8 board
# to the opposite corner, where each move is one square (including diagonals).
# Solution: Use dynamic programming where dp[r][c] = number of ways to reach (r,c)
# from (0,0). A king can move in 8 directions, so we build paths incrementally.
# Verify with brute force recursion on small boards.

def count_king_paths_dp(n):
    """DP approach: build up paths from top-left to bottom-right."""
    dp = [[0] * n for _ in range(n)]
    dp[0][0] = 1
    
    for r in range(n):
        for c in range(n):
            if r == 0 and c == 0:
                continue
            ways = 0
            # Check all 8 king moves leading to (r, c)
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    prev_r, prev_c = r - dr, c - dc
                    if 0 <= prev_r < n and 0 <= prev_c < n:
                        ways += dp[prev_r][prev_c]
            dp[r][c] = ways
    
    return dp[n-1][n-1]

def count_king_paths_brute(n, r=0, c=0, target_r=None, target_c=None):
    """Brute force recursion: explore all paths."""
    if target_r is None:
        target_r = n - 1
        target_c = n - 1
    
    if r == target_r and c == target_c:
        return 1
    
    if r < 0 or r >= n or c < 0 or c >= n:
        return 0
    
    if r > target_r or c > target_c:
        return 0
    
    count = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            count += count_king_paths_brute(n, r + dr, c + dc, target_r, target_c)
    
    return count

# Verify on small boards
print("=== King Paths: Corner to Corner ===\n")
print("Board Size | DP Result | Brute Force | Match")
print("-" * 50)

for size in range(2, 6):
    dp_result = count_king_paths_dp(size)
    brute_result = count_king_paths_brute(size)
    match = "✓" if dp_result == brute_result else "✗"
    print(f"{size:^10} | {dp_result:^9} | {brute_result:^11} | {match}")

print("\n=== Results for Standard 8x8 Board ===")
result_8x8 = count_king_paths_dp(8)
print(f"Number of king paths from (0,0) to (7,7): {result_8x8:,}")

# Show a smaller board visualization
print("\n=== Visualization on 4x4 Board ===")
n = 4
dp = [[0] * n for _ in range(n)]
dp[0][0] = 1

for r in range(n):
    for c in range(n):
        if r == 0 and c == 0:
            continue
        ways = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                prev_r, prev_c = r - dr, c - dc
                if 0 <= prev_r < n and 0 <= prev_c < n:
                    ways += dp[prev_r][prev_c]
        dp[r][c] = ways

for r in range(n):
    for c in range(n):
        print(f"{dp[r][c]:7}", end="")
    print()

print(f"\nPaths on 4x4: {dp[n-1][n-1]}")
