# Title: King Move Generation and Distance Metric Validation

# This puzzle generates all legal king moves from any position on a chessboard,
# then validates Chebyshev distance (max of absolute differences) against actual moves.
# A king can move one square in any of 8 directions. We verify that the minimum number
# of king moves to reach any square equals the Chebyshev distance formula.

def king_moves(row, col):
    """Generate all legal king moves from (row, col) on an 8x8 board."""
    moves = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = row + dr, col + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                moves.append((nr, nc))
    return moves

def chebyshev_distance(r1, c1, r2, c2):
    """Calculate Chebyshev distance: max(|r1-r2|, |c1-c2|)."""
    return max(abs(r1 - r2), abs(c1 - c2))

def min_king_moves_bfs(start_row, start_col, end_row, end_col):
    """Find minimum king moves using BFS (brute force verification)."""
    if start_row == end_row and start_col == end_col:
        return 0
    
    from collections import deque
    queue = deque([(start_row, start_col, 0)])
    visited = {(start_row, start_col)}
    
    while queue:
        r, c, dist = queue.popleft()
        for nr, nc in king_moves(r, c):
            if nr == end_row and nc == end_col:
                return dist + 1
            if (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc, dist + 1))
    
    return -1

def draw_board_with_moves(row, col):
    """Draw board showing king position and its legal moves."""
    board = [['.' for _ in range(8)] for _ in range(8)]
    board[row][col] = 'K'
    for nr, nc in king_moves(row, col):
        board[nr][nc] = '*'
    
    print(f"King at ({row}, {col}):")
    for i, r in enumerate(board):
        print(f"  {' '.join(r)}")
    print()

# Test cases
print("=== King Move Generation ===\n")

test_positions = [(0, 0), (3, 3), (7, 7), (4, 4)]

for start_r, start_c in test_positions:
    moves = king_moves(start_r, start_c)
    draw_board_with_moves(start_r, start_c)
    print(f"Legal moves from ({start_r}, {start_c}): {len(moves)} moves")
    print(f"Moves: {moves}\n")

print("=== Chebyshev Distance Verification ===\n")
print("Verifying that Chebyshev distance equals minimum king moves:")
print()

all_match = True
for start_r in range(8):
    for start_c in range(8):
        for end_r in range(8):
            for end_c in range(8):
                chebyshev = chebyshev_distance(start_r, start_c, end_r, end_c)
                bfs_dist = min_king_moves_bfs(start_r, start_c, end_r, end_c)
                if chebyshev != bfs_dist:
                    all_match = False
                    print(f"MISMATCH: ({start_r},{start_c}) to ({end_r},{end_c}): "
                          f"Chebyshev={chebyshev}, BFS={bfs_dist}")

if all_match:
    print("✓ All 64×64 position pairs verified: Chebyshev distance formula is correct!")
    print()

# Show some example distances
print("Sample distances from (0, 0):")
for target_r, target_c in [(0, 0), (1, 1), (3, 2), (7, 7)]:
    dist = chebyshev_distance(0, 0, target_r, target_c)
    print(f"  (0, 0) → ({target_r}, {target_c}): {dist} moves")
