# Title: Knight's Tour with Warnsdorff's Rule on Small Boards

# A knight's tour is a sequence of moves where a knight visits every square on a chessboard exactly once.
# Warnsdorff's rule is a heuristic: always move the knight to the square from which it will have the fewest onward moves.
# This greedy approach succeeds on most board sizes. We solve small boards and visualize the tour.

def knight_moves(r, c, n):
    """Generate all valid knight moves from (r, c) on an n×n board."""
    moves = []
    for dr, dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < n and 0 <= nc < n:
            moves.append((nr, nc))
    return moves

def count_onward_moves(r, c, board, n):
    """Count how many unvisited squares the knight can reach from (r, c)."""
    count = 0
    for nr, nc in knight_moves(r, c, n):
        if board[nr][nc] == -1:
            count += 1
    return count

def warnsdorff_tour(n, start_r=0, start_c=0):
    """Find a knight's tour using Warnsdorff's rule. Returns tour as list of moves, or None if failed."""
    board = [[-1] * n for _ in range(n)]
    board[start_r][start_c] = 0
    tour = [(start_r, start_c)]
    r, c = start_r, start_c
    
    for move_num in range(1, n * n):
        candidates = knight_moves(r, c, n)
        # Filter to unvisited squares only
        candidates = [(nr, nc) for nr, nc in candidates if board[nr][nc] == -1]
        
        if not candidates:
            return None  # Dead end
        
        # Sort by Warnsdorff's rule: fewest onward moves first
        candidates.sort(key=lambda pos: count_onward_moves(pos[0], pos[1], board, n))
        
        r, c = candidates[0]
        board[r][c] = move_num
        tour.append((r, c))
    
    return tour, board

def print_board(board):
    """Print the board with move numbers."""
    n = len(board)
    for row in board:
        print(" ".join(f"{val:3d}" for val in row))
    print()

def visualize_tour(tour, n):
    """Show the tour as a sequence of coordinates."""
    print(f"Tour ({len(tour)} moves):")
    for i, (r, c) in enumerate(tour):
        print(f"  {i:2d}: ({r},{c})", end="")
        if (i + 1) % 4 == 0:
            print()
        else:
            print(" | ", end="")
    print()

# Test on small boards
for board_size in [5, 6]:
    print(f"\n{'='*50}")
    print(f"Knight's Tour on {board_size}×{board_size} board (Warnsdorff's Rule)")
    print(f"{'='*50}")
    
    result = warnsdorff_tour(board_size)
    if result:
        tour, board = result
        print_board(board)
        visualize_tour(tour, board_size)
        print(f"✓ Tour found! Visited all {board_size * board_size} squares.\n")
    else:
        print(f"✗ No tour found from (0, 0).\n")

# Verify on a 6×6: show success rate across different starting positions
print(f"\n{'='*50}")
print("Success rate on 6×6 from various starts (Warnsdorff's rule):")
print(f"{'='*50}")
successes = 0
for start_r in range(6):
    for start_c in range(6):
        result = warnsdorff_tour(6, start_r, start_c)
        if result:
            successes += 1

print(f"Successful tours: {successes} out of 36 starting positions ({100*successes//36}%)")
