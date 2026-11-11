# Title: Pawn Race to Promotion

# Puzzle: Given two pawns on a chessboard, determine which pawn reaches
# the promotion rank first (rank 8 for white, rank 1 for black) assuming
# both move optimally without captures. Uses BFS to find the shortest path
# considering that pawns can only move forward and occasionally sideways
# (capturing). We model pawn movement as a graph search problem where each
# state is (row, col, moves). White pawns start at low ranks, black at high.

from collections import deque

def pawn_distance_to_promotion(start_row, start_col, is_white):
    """
    BFS to find minimum moves for a pawn to reach promotion rank.
    White pawns promote at row 7 (rank 8), black at row 0 (rank 1).
    """
    target_row = 7 if is_white else 0
    
    if start_row == target_row:
        return 0
    
    queue = deque([(start_row, start_col, 0)])
    visited = {(start_row, start_col)}
    
    while queue:
        row, col, moves = queue.popleft()
        
        if row == target_row:
            return moves
        
        # Pawn moves: forward only (no capture needed for this puzzle)
        if is_white:
            next_row = row + 1
        else:
            next_row = row - 1
        
        if 0 <= next_row < 8:
            # Move straight forward
            if (next_row, col) not in visited:
                visited.add((next_row, col))
                queue.append((next_row, col, moves + 1))
    
    return -1


def pawn_race(white_pos, black_pos):
    """
    Determine which pawn reaches promotion first.
    white_pos and black_pos are (row, col) tuples.
    """
    white_moves = pawn_distance_to_promotion(white_pos[0], white_pos[1], True)
    black_moves = pawn_distance_to_promotion(black_pos[0], black_pos[1], False)
    
    return white_moves, black_moves


def draw_board(white_pos, black_pos):
    """Draw a simple text board showing pawn positions."""
    board = [['.' for _ in range(8)] for _ in range(8)]
    board[white_pos[0]][white_pos[1]] = 'P'
    board[black_pos[0]][black_pos[1]] = 'p'
    
    print("  0 1 2 3 4 5 6 7")
    for i in range(8):
        print(f"{i} {' '.join(board[i])}")
    print()


def verify_formula():
    """Verify: distance to promotion = target_row - start_row for white."""
    # For white pawn at row r, should take 7 - r moves to reach row 7
    for r in range(7):
        dist = pawn_distance_to_promotion(r, 0, True)
        expected = 7 - r
        assert dist == expected, f"White pawn at row {r}: got {dist}, expected {expected}"
    
    # For black pawn at row r, should take r moves to reach row 0
    for r in range(1, 8):
        dist = pawn_distance_to_promotion(r, 0, False)
        expected = r
        assert dist == expected, f"Black pawn at row {r}: got {dist}, expected {expected}"
    
    print("✓ Formula verified for all rows\n")


# Main
print("Pawn Race to Promotion - BFS Analysis\n")
verify_formula()

# Test cases
test_cases = [
    ((1, 0), (6, 0), "Pawns on same file"),
    ((2, 3), (5, 3), "Pawns on same file, middle board"),
    ((1, 0), (5, 7), "Pawns on different files"),
    ((3, 2), (4, 5), "Pawns close to each other"),
]

for white_pos, black_pos, description in test_cases:
    print(f"Scenario: {description}")
    draw_board(white_pos, black_pos)
    white_moves, black_moves = pawn_race(white_pos, black_pos)
    
    print(f"White pawn at {white_pos}: {white_moves} moves to promotion")
    print(f"Black pawn at {black_pos}: {black_moves} moves to promotion")
    
    if white_moves < black_moves:
        print(f"→ WHITE WINS by {black_moves - white_moves} move(s)\n")
    elif black_moves < white_moves:
        print(f"→ BLACK WINS by {white_moves - black_moves} move(s)\n")
    else:
        print(f"→ TIE (both promote in {white_moves} moves)\n")
