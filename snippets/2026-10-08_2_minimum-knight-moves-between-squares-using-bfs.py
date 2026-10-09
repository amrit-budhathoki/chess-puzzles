# Title: Minimum Knight Moves Between Squares Using BFS

# A knight on a chessboard can move in an L-shape (2 squares in one direction,
# 1 square perpendicular). This puzzle finds the minimum number of moves needed
# to go from one square to another using breadth-first search (BFS).
# BFS guarantees the shortest path in an unweighted graph.

from collections import deque

def knight_moves(start, end):
    """
    Return minimum number of knight moves from start to end.
    Squares are (row, col) tuples where 0 <= row, col < 8.
    """
    if start == end:
        return 0
    
    # Knight move offsets: 2 in one direction, 1 perpendicular
    moves = [
        (2, 1), (2, -1), (-2, 1), (-2, -1),
        (1, 2), (1, -2), (-1, 2), (-1, -2)
    ]
    
    queue = deque([(start, 0)])
    visited = {start}
    
    while queue:
        (r, c), dist = queue.popleft()
        
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            
            if (nr, nc) == end:
                return dist + 1
            
            if 0 <= nr < 8 and 0 <= nc < 8 and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append(((nr, nc), dist + 1))
    
    return -1  # Should never happen on a valid chessboard

def visualize_path(start, end, path_len):
    """Print a simple visualization of start and end squares."""
    board = [['.' for _ in range(8)] for _ in range(8)]
    board[start[0]][start[1]] = 'S'
    board[end[0]][end[1]] = 'E'
    
    print(f"  0 1 2 3 4 5 6 7")
    for i, row in enumerate(board):
        print(f"{i} {' '.join(row)}")
    print()

# Test cases
test_cases = [
    ((0, 0), (7, 7)),  # Corner to corner
    ((0, 0), (0, 1)),  # Adjacent squares (knight's minimum distance)
    ((0, 0), (1, 0)),  # Should be 3 moves
    ((3, 3), (3, 3)),  # Same square
    ((0, 0), (2, 2)),  # Diagonal neighbor
    ((1, 1), (6, 6)),  # Medium distance
]

print("Knight Minimum Moves Puzzle")
print("=" * 40)

for start, end in test_cases:
    result = knight_moves(start, end)
    print(f"From {start} to {end}: {result} moves")
    visualize_path(start, end, result)

# Verify with brute force for a small case
def brute_force_knight_moves(start, end, memo=None):
    """Recursive brute force with memoization for verification."""
    if memo is None:
        memo = {}
    if start == end:
        return 0
    if start in memo:
        return memo[start]
    
    moves = [
        (2, 1), (2, -1), (-2, 1), (-2, -1),
        (1, 2), (1, -2), (-1, 2), (-1, -2)
    ]
    
    min_moves = float('inf')
    for dr, dc in moves:
        nr, nc = start[0] + dr, start[1] + dc
        if 0 <= nr < 8 and 0 <= nc < 8:
            min_moves = min(min_moves, 1 + brute_force_knight_moves((nr, nc), end, memo))
    
    memo[start] = min_moves
    return min_moves

print("\nVerification against brute force (small cases):")
print("=" * 40)
verify_cases = [((0, 0), (1, 2)), ((0, 0), (2, 2)), ((1, 1), (3, 3))]
for start, end in verify_cases:
    bfs_result = knight_moves(start, end)
    bf_result = brute_force_knight_moves(start, end)
    match = "✓" if bfs_result == bf_result else "✗"
    print(f"{match} {start} → {end}: BFS={bfs_result}, Brute Force={bf_result}")
