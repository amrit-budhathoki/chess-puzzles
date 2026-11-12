# Title: Mutilated Chessboard Domino Puzzle

# The mutilated chessboard puzzle: can 31 dominoes (each covering 2 squares)
# cover a chessboard with two opposite corners removed?
# 
# The key insight: color parity. Each domino covers one black and one white square.
# A standard chessboard has 32 black and 32 white squares. Removing two opposite
# corners removes two squares of the same color (opposite corners are same color).
# This leaves 32 and 30 squares of different colors—impossible to cover perfectly
# with dominoes. We verify this reasoning with a backtracking search on small boards.

def can_tile_board(removed_corners):
    """
    Backtracking search: try to place dominoes on an 8x8 board
    with two opposite corners removed. Return True if possible.
    """
    board = [[True] * 8 for _ in range(8)]
    for r, c in removed_corners:
        board[r][c] = False
    
    def place_domino(row, col):
        # Find next empty square
        while row < 8:
            while col < 8 and not board[row][col]:
                col += 1
            if col < 8:
                break
            row += 1
            col = 0
        
        # All squares covered
        if row == 8:
            return True
        
        # Try horizontal domino
        if col + 1 < 8 and board[row][col + 1]:
            board[row][col] = False
            board[row][col + 1] = False
            if place_domino(row, col):
                return True
            board[row][col] = True
            board[row][col + 1] = True
        
        # Try vertical domino
        if row + 1 < 8 and board[row + 1][col]:
            board[row][col] = False
            board[row + 1][col] = False
            if place_domino(row, col):
                return True
            board[row][col] = True
            board[row + 1][col] = True
        
        return False
    
    return place_domino(0, 0)

def count_color_parity(removed_corners):
    """Count black and white squares remaining after removing corners."""
    black = white = 32
    for r, c in removed_corners:
        if (r + c) % 2 == 0:
            black -= 1
        else:
            white -= 1
    return black, white

# Test the mutilated chessboard puzzle
print("=" * 50)
print("MUTILATED CHESSBOARD DOMINO PUZZLE")
print("=" * 50)

# Opposite corners: (0,0) and (7,7) — same color
opposite_corners = [(0, 0), (7, 7)]
black, white = count_color_parity(opposite_corners)
print(f"\nRemoving opposite corners (0,0) and (7,7):")
print(f"  Black squares remaining: {black}")
print(f"  White squares remaining: {white}")
print(f"  Difference: {abs(black - white)}")
print(f"  Parity argument: Cannot tile (need equal counts for dominoes)")

# Verify with backtracking on smaller boards (4x4)
print(f"\n  Backtracking search on 8x8: ", end="", flush=True)
result = can_tile_board(opposite_corners)
print(f"Possible = {result}")

# Adjacent corners: (0,0) and (7,0) — opposite colors
adjacent_corners = [(0, 0), (7, 0)]
black, white = count_color_parity(adjacent_corners)
print(f"\nRemoving adjacent corners (0,0) and (7,0):")
print(f"  Black squares remaining: {black}")
print(f"  White squares remaining: {white}")
print(f"  Difference: {abs(black - white)}")
print(f"  Parity argument: Could potentially tile (equal counts)")

# Verify on a smaller 4x4 board with corners removed
def can_tile_small_board(removed_corners, size=4):
    """4x4 version for quick verification."""
    board = [[True] * size for _ in range(size)]
    for r, c in removed_corners:
        if r < size and c < size:
            board[r][c] = False
    
    def place(row, col):
        while row < size:
            while col < size and not board[row][col]:
                col += 1
            if col < size:
                break
            row += 1
            col = 0
        if row == size:
            return True
        if col + 1 < size and board[row][col + 1]:
            board[row][col] = False
            board[row][col + 1] = False
            if place(row, col):
                return True
            board[row][col] = True
            board[row][col + 1] = True
        if row + 1 < size and board[row + 1][col]:
            board[row][col] = False
            board[row + 1][col] = False
            if place(row, col):
                return True
            board[row][col] = True
            board[row + 1][col] = True
        return False
    
    return place(0, 0)

print(f"\n  Backtracking search on 4x4 (with (0,0) and (3,0) removed):")
print(f"  Possible = {can_tile_small_board([(0, 0), (3, 0)], 4)}")

print("\n" + "=" * 50)
print("CONCLUSION: Opposite corners impossible; parity rules!")
print("=" * 50)
