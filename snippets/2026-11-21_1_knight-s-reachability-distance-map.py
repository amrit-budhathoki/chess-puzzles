# Title: Knight's Reachability Distance Map

# This program computes the minimum number of moves required for a knight
# to reach every square on a chessboard from a given starting position.
# It uses BFS to find shortest paths and visualizes the result as a heatmap.
# The idea is useful for endgame analysis and understanding knight mobility.

from collections import deque

def knight_distances(start_row, start_col):
    """
    Compute minimum knight moves from start position to all squares.
    Returns an 8x8 grid where each cell contains the distance, or -1 if unreachable.
    """
    distances = [[-1] * 8 for _ in range(8)]
    distances[start_row][start_col] = 0
    
    queue = deque([(start_row, start_col, 0)])
    knight_moves = [
        (-2, -1), (-2, 1), (-1, -2), (-1, 2),
        (1, -2), (1, 2), (2, -1), (2, 1)
    ]
    
    while queue:
        row, col, dist = queue.popleft()
        
        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8 and distances[new_row][new_col] == -1:
                distances[new_row][new_col] = dist + 1
                queue.append((new_row, new_col, dist + 1))
    
    return distances

def print_distance_map(distances, start_row, start_col):
    """Pretty-print the distance map with the starting position marked."""
    print(f"\nKnight distance map from ({start_row}, {start_col}):\n")
    print("  0 1 2 3 4 5 6 7")
    for row in range(8):
        print(f"{row} ", end="")
        for col in range(8):
            if row == start_row and col == start_col:
                print("S ", end="")
            else:
                print(f"{distances[row][col]} ", end="")
        print()

def verify_symmetry(distances):
    """Check that all squares are reachable (distance != -1)."""
    all_reachable = all(distances[r][c] != -1 for r in range(8) for c in range(8))
    return all_reachable

def compute_average_distance(distances):
    """Compute average distance to reach all squares."""
    valid_distances = [distances[r][c] for r in range(8) for c in range(8) if distances[r][c] != -1]
    return sum(valid_distances) / len(valid_distances) if valid_distances else 0

# Test from corner (0, 0)
print("=" * 40)
print("Test 1: Knight starting at corner (0, 0)")
print("=" * 40)
distances_corner = knight_distances(0, 0)
print_distance_map(distances_corner, 0, 0)
print(f"All squares reachable: {verify_symmetry(distances_corner)}")
print(f"Average distance: {compute_average_distance(distances_corner):.2f}")

# Test from center (3, 3)
print("\n" + "=" * 40)
print("Test 2: Knight starting at center (3, 3)")
print("=" * 40)
distances_center = knight_distances(3, 3)
print_distance_map(distances_center, 3, 3)
print(f"All squares reachable: {verify_symmetry(distances_center)}")
print(f"Average distance: {compute_average_distance(distances_center):.2f}")

# Test from edge (0, 3)
print("\n" + "=" * 40)
print("Test 3: Knight starting at edge (0, 3)")
print("=" * 40)
distances_edge = knight_distances(0, 3)
print_distance_map(distances_edge, 0, 3)
print(f"All squares reachable: {verify_symmetry(distances_edge)}")
print(f"Average distance: {compute_average_distance(distances_edge):.2f}")

# Observation: center positions have lower average distances
print("\n" + "=" * 40)
print("Summary: Center positions offer better knight mobility")
print("=" * 40)
