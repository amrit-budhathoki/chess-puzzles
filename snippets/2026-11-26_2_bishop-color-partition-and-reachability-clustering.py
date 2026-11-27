# Title: Bishop Color Partition and Reachability Clustering

# Puzzle: On an 8x8 chessboard, bishops can only reach squares of their own color.
# This creates two disconnected components (light and dark squares).
# Given a set of bishops on random squares, find the size of the largest
# reachable cluster from each bishop using graph traversal, and verify
# the formula: exactly half the squares are reachable from any bishop.

def square_color(row, col):
    """Return 'light' or 'dark' based on square parity."""
    return 'light' if (row + col) % 2 == 0 else 'dark'

def bishop_neighbors(row, col):
    """Generate all squares a bishop can reach from (row, col)."""
    neighbors = []
    for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
        r, c = row + dr, col + dc
        while 0 <= r < 8 and 0 <= c < 8:
            neighbors.append((r, c))
            r += dr
            c += dc
    return neighbors

def bfs_reachable(start_row, start_col):
    """BFS to find all squares reachable by a bishop from a starting square."""
    visited = set()
    queue = [(start_row, start_col)]
    visited.add((start_row, start_col))
    
    while queue:
        row, col = queue.pop(0)
        for nr, nc in bishop_neighbors(row, col):
            if (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc))
    
    return visited

def count_color_squares(color):
    """Count squares of a given color on the board."""
    return sum(1 for r in range(8) for c in range(8) if square_color(r, c) == color)

# Brute force: for each square, find all reachable squares
print("Bishop Reachability on 8x8 Board")
print("=" * 50)

light_count = count_color_squares('light')
dark_count = count_color_squares('dark')
print(f"Light squares: {light_count}, Dark squares: {dark_count}\n")

# Test a few sample bishops
test_positions = [(0, 0), (0, 1), (3, 4), (7, 7)]

for start_row, start_col in test_positions:
    color = square_color(start_row, start_col)
    reachable = bfs_reachable(start_row, start_col)
    expected_count = light_count if color == 'light' else dark_count
    
    print(f"Bishop at ({start_row}, {start_col}) [{color}]:")
    print(f"  Reachable squares: {len(reachable)}")
    print(f"  Expected ({color} squares): {expected_count}")
    print(f"  Match: {len(reachable) == expected_count}\n")

# Verify formula: for any bishop, it can reach exactly half the board
# (all squares of its color)
print("Verification across entire board:")
print("-" * 50)
all_reachable_sizes = {}
for row in range(8):
    for col in range(8):
        color = square_color(row, col)
        reachable_size = len(bfs_reachable(row, col))
        expected_size = light_count if color == 'light' else dark_count
        all_reachable_sizes[(row, col)] = reachable_size
        
        if reachable_size != expected_size:
            print(f"MISMATCH at ({row}, {col}): got {reachable_size}, expected {expected_size}")

light_reachable = [size for (r, c), size in all_reachable_sizes.items() if square_color(r, c) == 'light']
dark_reachable = [size for (r, c), size in all_reachable_sizes.items() if square_color(r, c) == 'dark']

print(f"All light-square bishops reach exactly {light_reachable[0]} squares: {len(set(light_reachable)) == 1}")
print(f"All dark-square bishops reach exactly {dark_reachable[0]} squares: {len(set(dark_reachable)) == 1}")
print(f"Total reachable per bishop: {light_reachable[0]} (32 out of 64)")

# Draw example board with reachable squares from a1 (0,0)
print("\nExample: Squares reachable by bishop at a1 (0,0):")
print("-" * 50)
reachable_a1 = bfs_reachable(0, 0)
for row in range(8):
    line = ""
    for col in range(8):
        if (row, col) == (0, 0):
            line += " B "
        elif (row, col) in reachable_a1:
            line += " x "
        else:
            line += " . "
    print(line)
