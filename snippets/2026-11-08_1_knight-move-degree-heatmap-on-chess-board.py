# Title: Knight Move Degree Heatmap on Chess Board

# A knight can move in an L-shape: 2 squares in one direction, 1 square perpendicular.
# From any square, a knight can move to at most 8 squares. This program calculates
# how many valid moves a knight has from each square on a standard 8x8 chess board,
# then displays the result as a heatmap using ASCII characters (density increases).

def knight_degree(row, col, board_size=8):
    """Calculate how many valid knight moves from (row, col)."""
    moves = [
        (-2, -1), (-2, 1), (-1, -2), (-1, 2),
        (1, -2), (1, 2), (2, -1), (2, 1)
    ]
    count = 0
    for dr, dc in moves:
        nr, nc = row + dr, col + dc
        if 0 <= nr < board_size and 0 <= nc < board_size:
            count += 1
    return count

def verify_knight_degree_formula():
    """Verify degree formula by brute force on 8x8 board."""
    board_size = 8
    for row in range(board_size):
        for col in range(board_size):
            degree = knight_degree(row, col, board_size)
            # Corner squares should have degree 2
            if (row, col) in [(0, 0), (0, 7), (7, 0), (7, 7)]:
                assert degree == 2, f"Corner {(row, col)} should have degree 2, got {degree}"
            # Edge squares near corners should have degree 3
            if (row, col) in [(0, 1), (1, 0), (0, 6), (1, 7), (6, 0), (7, 1), (6, 7), (7, 6)]:
                assert degree == 3, f"Near-corner {(row, col)} should have degree 3, got {degree}"
            # Center squares should have degree 8
            if 2 <= row <= 5 and 2 <= col <= 5:
                assert degree == 8, f"Center {(row, col)} should have degree 8, got {degree}"

def create_heatmap():
    """Create and display knight degree heatmap."""
    board_size = 8
    degrees = []
    for row in range(board_size):
        degrees.append([knight_degree(row, col, board_size) for col in range(board_size)])
    
    # Verify on small board
    verify_knight_degree_formula()
    
    # Display as heatmap with ASCII art
    symbols = " ▁▂▃▄▅▆▇█"  # Gradient from empty to full
    print("Knight Move Degree Heatmap (8x8 chess board)")
    print("=" * 40)
    print("\nDegree (number of valid knight moves from each square):\n")
    
    print("  a b c d e f g h")
    for row in range(board_size):
        print(f"{8 - row} ", end="")
        for col in range(board_size):
            degree = degrees[row][col]
            symbol = symbols[degree]
            print(f"{symbol} ", end="")
        print(f"{8 - row}")
    print("  a b c d e f g h")
    
    # Print numeric heatmap
    print("\nNumeric values:")
    print("  a b c d e f g h")
    for row in range(board_size):
        print(f"{8 - row} ", end="")
        for col in range(board_size):
            degree = degrees[row][col]
            print(f"{degree} ", end="")
        print(f"{8 - row}")
    print("  a b c d e f g h")
    
    # Statistics
    all_degrees = [d for row in degrees for d in row]
    print(f"\nStatistics:")
    print(f"  Min degree: {min(all_degrees)}")
    print(f"  Max degree: {max(all_degrees)}")
    print(f"  Average degree: {sum(all_degrees) / len(all_degrees):.2f}")
    print(f"  Degree distribution: {dict(sorted(__import__('collections').Counter(all_degrees).items()))}")

create_heatmap()
