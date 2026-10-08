# Title: Knight's Tour using Warnsdorff's Rule

"""
A knight's tour is a sequence of moves where a knight visits every square
on a chessboard exactly once. Warnsdorff's rule is a heuristic that chooses
the next move to be the square from which the knight will have the fewest
onward moves. This greedy approach is remarkably effective for finding tours.
"""

def get_knight_moves(row, col, board_size):
    """Return all valid knight moves from (row, col)."""
    moves = []
    deltas = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
              (1, -2), (1, 2), (2, -1), (2, 1)]
    for dr, dc in deltas:
        nr, nc = row + dr, col + dc
        if 0 <= nr < board_size and 0 <= nc < board_size:
            moves.append((nr, nc))
    return moves

def count_onward_moves(row, col, board, board_size):
    """Count how many unvisited squares the knight can reach from (row, col)."""
    count = 0
    for nr, nc in get_knight_moves(row, col, board_size):
        if board[nr][nc] == -1:
            count += 1
    return count

def knights_tour_warnsdorff(board_size, start_row, start_col):
    """Find a knight's tour using Warnsdorff's rule."""
    board = [[-1] * board_size for _ in range(board_size)]
    board[start_row][start_col] = 0
    
    row, col = start_row, start_col
    
    for move_count in range(1, board_size * board_size):
        next_moves = get_knight_moves(row, col, board_size)
        # Filter to unvisited squares only
        unvisited = [(nr, nc) for nr, nc in next_moves if board[nr][nc] == -1]
        
        if not unvisited:
            return None  # No valid moves; tour failed
        
        # Choose the square with the fewest onward moves (Warnsdorff's rule)
        next_row, next_col = min(
            unvisited,
            key=lambda pos: count_onward_moves(pos[0], pos[1], board, board_size)
        )
        
        board[next_row][next_col] = move_count
        row, col = next_row, next_col
    
    return board

def print_board(board):
    """Print the tour board."""
    board_size = len(board)
    max_num = board_size * board_size - 1
    width = len(str(max_num))
    
    for row in board:
        print(" ".join(f"{val:{width}}" for val in row))

def solve_and_display(board_size):
    """Solve and display a knight's tour."""
    print(f"Knight's Tour on {board_size}x{board_size} board using Warnsdorff's Rule\n")
    
    board = knights_tour_warnsdorff(board_size, 0, 0)
    
    if board is None:
        print("No tour found!")
    else:
        print("Tour found! (showing move numbers):\n")
        print_board(board)
        print(f"\nTotal moves: {board_size * board_size - 1}")
        print(f"All {board_size * board_size} squares visited: ✓")

# Test on multiple board sizes
print("=" * 50)
solve_and_display(6)
print("\n" + "=" * 50)
solve_and_display(8)
