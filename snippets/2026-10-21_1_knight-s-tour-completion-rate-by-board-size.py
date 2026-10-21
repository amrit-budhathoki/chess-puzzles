# Title: Knight's Tour Completion Rate by Board Size

# This program explores how often Warnsdorff's rule (always move the knight to
# the square from which it will have the fewest onward moves) successfully
# completes a knight's tour on various board sizes. We run multiple random
# starting positions and count successes. The heuristic works remarkably well
# on standard 8x8 boards but degrades on smaller boards.

def knight_moves(r, c, n):
    """Return list of valid knight move destinations from (r,c) on n×n board."""
    moves = []
    for dr, dc in [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < n and 0 <= nc < n:
            moves.append((nr, nc))
    return moves

def count_onward_moves(r, c, visited, n):
    """Count how many unvisited squares are reachable from (r,c)."""
    count = 0
    for nr, nc in knight_moves(r, c, n):
        if (nr, nc) not in visited:
            count += 1
    return count

def warnsdorff_tour(start_r, start_c, n):
    """Attempt knight's tour using Warnsdorff's rule. Return True if complete."""
    visited = set()
    r, c = start_r, start_c
    visited.add((r, c))
    
    while len(visited) < n * n:
        # Find all unvisited neighbors
        neighbors = [(nr, nc) for nr, nc in knight_moves(r, c, n) 
                     if (nr, nc) not in visited]
        
        if not neighbors:
            return False
        
        # Choose neighbor with minimum onward moves (Warnsdorff's rule)
        # Break ties by choosing first in list
        next_move = min(neighbors, 
                       key=lambda pos: count_onward_moves(pos[0], pos[1], visited, n))
        
        r, c = next_move
        visited.add((r, c))
    
    return True

def test_warnsdorff(n, num_trials=100):
    """Test Warnsdorff's rule on n×n board from random starting positions."""
    successes = 0
    for start_r in range(n):
        for start_c in range(n):
            if warnsdorff_tour(start_r, start_c, n):
                successes += 1
    return successes

# Test on various board sizes
print("Knight's Tour Completion Rate using Warnsdorff's Rule")
print("=" * 55)
for size in [4, 5, 6, 7, 8]:
    total_starts = size * size
    successes = test_warnsdorff(size)
    rate = 100.0 * successes / total_starts
    print(f"{size}×{size} board: {successes:3d}/{total_starts:2d} starting positions succeed ({rate:5.1f}%)")

print("\n" + "=" * 55)
print("On 8×8: Warnsdorff's rule succeeds from most positions.")
print("On smaller boards: rule may fail due to limited branching.")
