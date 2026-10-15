# Title: Knight Move Degree Heatmap

# A knight can move in an L-shape: 2 squares in one direction and 1 square perpendicular.
# This program computes how many squares a knight can reach from each square on a chessboard.
# We visualize this as a heatmap showing the degree (number of reachable squares) for each position.
# Corner squares have fewer options (2 moves), edge squares have 3-4 moves, and central squares have 8.

def knight_degree(row, col, board_size=8):
    """Count how many valid knight moves exist from position (row, col)."""
    moves = [
        (2, 1), (2, -1), (-2, 1), (-2, -1),
        (1, 2), (1, -2), (-1, 2), (-1, -2)
    ]
    count = 0
    for dr, dc in moves:
        nr, nc = row + dr, col + dc
        if 0 <= nr < board_size and 0 <= nc < board_size:
            count += 1
    return count

def create_heatmap(board_size=8):
    """Create a heatmap of knight move degrees for all squares."""
    heatmap = []
    for row in range(board_size):
        heatmap_row = []
        for col in range(board_size):
            degree = knight_degree(row, col, board_size)
            heatmap_row.append(degree)
        heatmap.append(heatmap_row)
    return heatmap

def print_heatmap(heatmap):
    """Print heatmap with visual representation."""
    print("\nKnight Move Degree Heatmap (8x8 board):")
    print("(Shows how many squares a knight can reach from each position)\n")
    print("  a b c d e f g h")
    for i, row in enumerate(heatmap):
        print(f"{8-i} ", end="")
        for val in row:
            # Use shading: . for low, o for medium, * for high
            if val <= 2:
                symbol = "·"
            elif val <= 4:
                symbol = "○"
            elif val <= 6:
                symbol = "◐"
            else:
                symbol = "●"
            print(f"{val}{symbol}", end=" ")
        print(f" {8-i}")
    print("  a b c d e f g h\n")

def verify_corners_and_center():
    """Verify knight degrees at specific squares match expectations."""
    # Corner squares should have 2 moves
    assert knight_degree(0, 0) == 2, "Corner a1 should have 2 moves"
    assert knight_degree(0, 7) == 2, "Corner h1 should have 2 moves"
    
    # Center squares should have 8 moves
    assert knight_degree(3, 3) == 8, "Center d5 should have 8 moves"
    assert knight_degree(4, 4) == 8, "Center e4 should have 8 moves"
    
    # Edge but not corner should have 3 or 4 moves
    assert knight_degree(0, 1) == 3, "Edge a2 should have 3 moves"
    assert knight_degree(1, 0) == 3, "Edge b1 should have 3 moves"
    
    print("✓ All verification checks passed!\n")

def print_degree_statistics(heatmap):
    """Print statistics about the degree distribution."""
    from collections import Counter
    all_degrees = [val for row in heatmap for val in row]
    degree_counts = Counter(all_degrees)
    
    print("Degree Distribution:")
    for degree in sorted(degree_counts.keys()):
        count = degree_counts[degree]
        print(f"  Degree {degree}: {count} squares")
    
    avg_degree = sum(all_degrees) / len(all_degrees)
    print(f"\nAverage degree: {avg_degree:.2f}")
    print(f"Min degree: {min(all_degrees)}, Max degree: {max(all_degrees)}\n")

if __name__ == "__main__":
    verify_corners_and_center()
    
    heatmap = create_heatmap(8)
    print_heatmap(heatmap)
    print_degree_statistics(heatmap)
    
    print("Legend:")
    print("  · = 2 moves (corners)")
    print("  ○ = 3-4 moves (edges)")
    print("  ◐ = 5-6 moves (near center)")
    print("  ● = 8 moves (center)")
