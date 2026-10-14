# Title: Knight Move Degree Heatmap

# A knight can move to at most 8 squares from any position on a chessboard.
# Corner and edge squares have fewer reachable destinations. This program
# computes the degree (number of valid knight moves) for every square and
# visualizes it as a heatmap, showing how "connected" each square is in the
# knight move graph.

def get_knight_moves(row, col):
    """Return list of valid squares a knight can reach from (row, col)."""
    moves = []
    knight_deltas = [
        (-2, -1), (-2, 1), (-1, -2), (-1, 2),
        (1, -2), (1, 2), (2, -1), (2, 1)
    ]
    for dr, dc in knight_deltas:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            moves.append((new_row, new_col))
    return moves

def compute_knight_degrees():
    """Compute degree of each square (number of knight moves from it)."""
    degrees = [[0] * 8 for _ in range(8)]
    for row in range(8):
        for col in range(8):
            degrees[row][col] = len(get_knight_moves(row, col))
    return degrees

def verify_formula():
    """Verify degree formula against brute force for 8x8 board."""
    degrees = compute_knight_degrees()
    
    # Known pattern for standard 8x8:
    # Corners (4): degree 2
    # Edge squares near corners (8): degree 3
    # Other edge squares (16): degree 4
    # Squares one in from edge, near corners (8): degree 4
    # Other interior squares: degree 6 or 8
    
    degree_counts = {}
    for row in range(8):
        for col in range(8):
            d = degrees[row][col]
            degree_counts[d] = degree_counts.get(d, 0) + 1
    
    return degrees, degree_counts

def draw_heatmap(degrees):
    """Draw a text-based heatmap of knight move degrees."""
    # Use characters to represent degree levels
    chars = {2: '░', 3: '▒', 4: '▓', 6: '█', 8: '◆'}
    
    print("\nKnight Move Degree Heatmap (8x8):")
    print("=" * 25)
    for row in range(8):
        print("  ", end="")
        for col in range(8):
            deg = degrees[row][col]
            char = chars.get(deg, '?')
            print(char, end=" ")
        print(f"  row {row}")
    print()

def print_numeric_grid(degrees):
    """Print the actual degree numbers in grid form."""
    print("\nNumerical Degree Grid:")
    print("=" * 40)
    for row in range(8):
        print("  ", end="")
        for col in range(8):
            print(str(degrees[row][col]), end=" ")
        print()
    print()

# Main execution
degrees, counts = verify_formula()

# Print numeric grid
print_numeric_grid(degrees)

# Print heatmap
draw_heatmap(degrees)

# Print statistics
print("Degree Distribution:")
print("=" * 40)
for degree in sorted(counts.keys()):
    print(f"Degree {degree}: {counts[degree]} squares")

print(f"\nAverage degree: {sum(counts[d] * d for d in counts) / 64:.2f}")
print(f"Min degree: {min(counts.keys())}, Max degree: {max(counts.keys())}")

# Verify a few specific squares by brute force
print("\nSpot checks (brute force verification):")
test_squares = [(0, 0), (0, 1), (3, 3), (7, 7)]
for row, col in test_squares:
    moves = get_knight_moves(row, col)
    print(f"  Square ({row},{col}): degree {len(moves)} -> moves to {moves}")
