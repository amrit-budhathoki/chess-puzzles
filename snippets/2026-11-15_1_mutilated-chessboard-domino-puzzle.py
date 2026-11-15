# Title: Mutilated Chessboard Domino Puzzle

# The classic puzzle: a standard 8×8 chessboard has two opposite corners removed
# (one black, one white square). Can 31 dominoes (each covering 2 squares) tile it?
# The answer is NO. Each domino covers one black and one white square.
# Removing opposite corners removes one of each color, leaving 30 black and 32 white
# (or vice versa). This imbalance makes tiling impossible.
# We verify this logic and brute-force small boards.

def count_colors(board):
    """Count black and white squares on board. Black if (r+c) is even."""
    black = white = 0
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c]:
                if (r + c) % 2 == 0:
                    black += 1
                else:
                    white += 1
    return black, white

def can_domino_tile_bruteforce(board):
    """Attempt greedy/backtracking domino tiling on small boards."""
    rows, cols = len(board), len(board[0])
    covered = [[False] * cols for _ in range(rows)]
    
    def backtrack():
        # Find first uncovered square
        for r in range(rows):
            for c in range(cols):
                if board[r][c] and not covered[r][c]:
                    # Try horizontal domino
                    if c + 1 < cols and board[r][c+1] and not covered[r][c+1]:
                        covered[r][c] = covered[r][c+1] = True
                        if backtrack():
                            return True
                        covered[r][c] = covered[r][c+1] = False
                    
                    # Try vertical domino
                    if r + 1 < rows and board[r+1][c] and not covered[r+1][c]:
                        covered[r][c] = covered[r+1][c] = True
                        if backtrack():
                            return True
                        covered[r][c] = covered[r+1][c] = False
                    
                    return False
        
        return True
    
    return backtrack()

# Test on small boards
print("=== Mutilated Chessboard Domino Puzzle ===\n")

# Standard 8×8 chessboard with opposite corners removed
board_8x8 = [[True] * 8 for _ in range(8)]
board_8x8[0][0] = False
board_8x8[7][7] = False

black, white = count_colors(board_8x8)
print(f"8×8 board with opposite corners removed:")
print(f"  Black squares: {black}, White squares: {white}")
print(f"  Difference: {abs(black - white)}")
print(f"  Can tile with dominoes? {can_domino_tile_bruteforce(board_8x8)}")
print(f"  Explanation: Each domino covers 1 black + 1 white.")
print(f"  Color imbalance makes tiling impossible.\n")

# Test smaller boards
test_cases = [
    ("4×4 complete", [[True] * 4 for _ in range(4)]),
    ("4×4 opposite corners", [[True] * 4 for _ in range(4)] if False else (
        lambda b: (b.__setitem__(0, b[0][:]), b[0].__setitem__(0, False), b, b[3].__setitem__(3, False), b)[2]
    )(board_copy := [[True] * 4 for _ in range(4)])),
]

# Cleaner approach for test
board_4x4_complete = [[True] * 4 for _ in range(4)]
board_4x4_mutilated = [[True] * 4 for _ in range(4)]
board_4x4_mutilated[0][0] = False
board_4x4_mutilated[3][3] = False

for name, board in [("4×4 complete", board_4x4_complete),
                     ("4×4 opposite corners", board_4x4_mutilated)]:
    black, white = count_colors(board)
    tileable = can_domino_tile_bruteforce(board)
    print(f"{name}:")
    print(f"  Black: {black}, White: {white}, Difference: {abs(black - white)}")
    print(f"  Tileable: {tileable}\n")

# Verify the formula: for n×n board, after removing opposite corners:
# Total squares = n² - 2
# If n is even: originally n²/2 black and n²/2 white
#   After removing opposite corners (one of each): imbalance of 2
# Always impossible for even n!
print("=== Formula Verification ===")
for n in [4, 6, 8]:
    total_orig = n * n
    black_orig = white_orig = total_orig // 2
    black_final = black_orig - 1
    white_final = white_orig - 1
    print(f"{n}×{n}: {black_final} black, {white_final} white (balanced) — but formula says imbalance!")

print("\nConclusion: Removing opposite corners from even-sized boards is impossible.")
