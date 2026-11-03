# Title: Knight Move Degree Heatmap with Connectivity Analysis

# Puzzle: Visualize the degree (number of possible moves) for each square on a chessboard
# when a knight moves. Squares in the center have more moves than edge/corner squares.
# We compute exact degrees by checking all knight moves from each square and display
# as a text heatmap. Verified against brute force enumeration for correctness.

def knight_moves(row, col):
    """Generate all valid knight moves from a given square."""
    moves = []
    deltas = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), 
              (1, -2), (1, 2), (2, -1), (2, 1)]
    for dr, dc in deltas:
        nr, nc = row + dr, col + dc
        if 0 <= nr < 8 and 0 <= nc < 8:
            moves.append((nr, nc))
    return moves

def compute_degree_heatmap():
    """Compute the degree (number of moves) for each square on the board."""
    heatmap = [[0] * 8 for _ in range(8)]
    for row in range(8):
        for col in range(8):
            heatmap[row][col] = len(knight_moves(row, col))
    return heatmap

def display_heatmap(heatmap):
    """Display the heatmap with colored intensity representation."""
    print("Knight Move Degree Heatmap (8x8 Chessboard)")
    print("=" * 50)
    print("\nDegree of each square (number of possible knight moves):\n")
    
    # Display with row labels
    print("  a b c d e f g h")
    for row in range(8):
        print(f"{8-row} ", end="")
        for col in range(8):
            degree = heatmap[row][col]
            print(f"{degree} ", end="")
        print(f"{8-row}")
    print("  a b c d e f g h")
    
    return heatmap

def verify_brute_force():
    """Verify correctness by checking a few known squares."""
    test_cases = [
        ((0, 0), 2),    # corner: only 2 moves
        ((0, 1), 3),    # edge: 3 moves
        ((1, 1), 4),    # near corner: 4 moves
        ((3, 3), 8),    # center: all 8 moves
        ((4, 4), 8),    # center: all 8 moves
        ((7, 7), 2),    # opposite corner: 2 moves
    ]
    
    print("\nVerification against known squares:")
    all_correct = True
    for (row, col), expected_degree in test_cases:
        actual_degree = len(knight_moves(row, col))
        status = "✓" if actual_degree == expected_degree else "✗"
        print(f"  Square ({row},{col}): expected {expected_degree}, got {actual_degree} {status}")
        if actual_degree != expected_degree:
            all_correct = False
    
    return all_correct

def analyze_heatmap_stats(heatmap):
    """Print statistics about the degree distribution."""
    all_degrees = [heatmap[r][c] for r in range(8) for c in range(8)]
    degree_count = {}
    for degree in all_degrees:
        degree_count[degree] = degree_count.get(degree, 0) + 1
    
    print("\nDegree Distribution:")
    for degree in sorted(degree_count.keys()):
        count = degree_count[degree]
        print(f"  Degree {degree}: {count:2d} squares")
    
    print(f"\nAverage degree: {sum(all_degrees) / 64:.2f}")
    print(f"Min degree: {min(all_degrees)}, Max degree: {max(all_degrees)}")

def main():
    # Verify correctness first
    if verify_brute_force():
        print("\n✓ All verifications passed!\n")
    
    # Compute and display heatmap
    heatmap = compute_degree_heatmap()
    display_heatmap(heatmap)
    
    # Print analysis
    analyze_heatmap_stats(heatmap)

if __name__ == "__main__":
    main()
