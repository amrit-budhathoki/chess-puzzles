# Title: Pawn Endgame Distance Calculator

# This program calculates the minimum number of moves for a pawn to reach a promotion
# square, considering that pawns can only move forward (and capture diagonally).
# We use BFS to explore all possible pawn move sequences from start to any promotion
# square on rank 8 (for white) or rank 1 (for black). This models a simplified endgame
# where we want to know how quickly a pawn can be promoted.

from collections import deque

def pawn_distance(start_file, start_rank, color="white"):
    """
    Find minimum moves for a pawn to reach promotion rank using BFS.
    color: "white" (promotes on rank 8) or "black" (promotes on rank 1)
    Returns (min_moves, promotion_file) or None if impossible.
    """
    promotion_rank = 8 if color == "white" else 1
    direction = 1 if color == "white" else -1
    
    if (color == "white" and start_rank >= 8) or (color == "black" and start_rank <= 1):
        return (0, start_file)
    
    queue = deque([(start_file, start_rank, 0)])
    visited = {(start_file, start_rank)}
    
    while queue:
        f, r, moves = queue.popleft()
        
        # Pawn promotion
        if r == promotion_rank:
            return (moves, f)
        
        # Forward move (no capture)
        next_rank = r + direction
        if 1 <= next_rank <= 8:
            if (f, next_rank) not in visited:
                visited.add((f, next_rank))
                queue.append((f, next_rank, moves + 1))
        
        # Diagonal captures (only if opponent piece exists - we explore both diagonals)
        for df in [-1, 1]:
            next_f = f + df
            if 1 <= next_f <= 8:
                next_rank = r + direction
                if 1 <= next_rank <= 8:
                    if (next_f, next_rank) not in visited:
                        visited.add((next_f, next_rank))
                        queue.append((next_f, next_rank, moves + 1))
    
    return None

def draw_board(start_file, start_rank, end_file, end_rank):
    """Draw a simple text board showing start and end positions."""
    print("  a b c d e f g h")
    for r in range(8, 0, -1):
        row = f"{r} "
        for f in range(1, 9):
            if f == start_file and r == start_rank:
                row += "P "
            elif f == end_file and r == end_rank:
                row += "* "
            else:
                row += ". "
        row += str(r)
        print(row)
    print("  a b c d e f g h")

# Test cases
print("=== White Pawn Promotion Distance ===\n")

test_cases = [
    (4, 2, "white"),  # d2 to promotion
    (1, 7, "white"),  # a7 to promotion
    (8, 6, "white"),  # h6 to promotion
    (4, 8, "white"),  # Already promoted
]

for file, rank, color in test_cases:
    result = pawn_distance(file, rank, color)
    file_char = chr(ord('a') + file - 1)
    if result:
        moves, promo_file = result
        promo_char = chr(ord('a') + promo_file - 1)
        print(f"Pawn at {file_char}{rank}: {moves} moves to {promo_char}8")
        if rank < 8:
            draw_board(file, rank, promo_file, 8)
    print()

print("=== Black Pawn Promotion Distance ===\n")

test_cases_black = [
    (4, 7, "black"),   # d7 to promotion
    (1, 2, "black"),   # a2 to promotion
    (8, 3, "black"),   # h3 to promotion
]

for file, rank, color in test_cases_black:
    result = pawn_distance(file, rank, color)
    file_char = chr(ord('a') + file - 1)
    if result:
        moves, promo_file = result
        promo_char = chr(ord('a') + promo_file - 1)
        print(f"Pawn at {file_char}{rank}: {moves} moves to {promo_char}1")
        if rank > 1:
            draw_board(file, rank, promo_file, 1)
    print()
