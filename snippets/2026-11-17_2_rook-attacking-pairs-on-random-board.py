# Title: Rook Attacking Pairs on Random Board

# Puzzle: Place n rooks randomly on an n×n chessboard and count how many pairs
# of rooks attack each other. Two rooks attack if they share a row or column.
# Solution: Use combinatorics—for each row/column with k rooks, there are C(k,2)
# attacking pairs. We verify the formula against brute force on small boards.

import random
from itertools import combinations

def count_attacking_pairs_brute(positions):
    """Brute force: check all pairs of rooks."""
    count = 0
    for (r1, c1), (r2, c2) in combinations(positions, 2):
        if r1 == r2 or c1 == c2:
            count += 1
    return count

def count_attacking_pairs_formula(positions):
    """Formula: sum C(k,2) over rows and columns with k rooks."""
    rows = {}
    cols = {}
    for r, c in positions:
        rows[r] = rows.get(r, 0) + 1
        cols[c] = cols.get(c, 0) + 1
    
    pairs = 0
    for count in rows.values():
        pairs += count * (count - 1) // 2
    for count in cols.values():
        pairs += count * (count - 1) // 2
    return pairs

def draw_board(n, positions):
    """Draw an n×n board with rooks marked as 'R'."""
    board = [['.' for _ in range(n)] for _ in range(n)]
    for r, c in positions:
        board[r][c] = 'R'
    for row in board:
        print(' '.join(row))

# Verify formula against brute force on small cases
print("=== Verification: Formula vs Brute Force ===")
for n in range(2, 6):
    # Generate a few random configurations
    for trial in range(3):
        positions = [(random.randint(0, n-1), random.randint(0, n-1)) 
                     for _ in range(n)]
        positions = list(set(positions))  # Remove duplicates
        if len(positions) < n:
            continue
        
        brute = count_attacking_pairs_brute(positions)
        formula = count_attacking_pairs_formula(positions)
        match = "✓" if brute == formula else "✗"
        print(f"n={n}, positions={len(positions)}: brute={brute}, formula={formula} {match}")

# Main puzzle: random placement on 8×8 board
print("\n=== Random Rook Placement on 8×8 Board ===")
n = 8
positions = set()
while len(positions) < n:
    positions.add((random.randint(0, n-1), random.randint(0, n-1)))
positions = list(positions)

print(f"\nBoard with {len(positions)} rooks:")
draw_board(n, positions)

attacking = count_attacking_pairs_formula(positions)
print(f"\nNumber of attacking pairs: {attacking}")
print(f"Maximum possible attacking pairs: {n * (n - 1) // 2}")
print(f"Attack density: {100 * attacking / (n * (n - 1) // 2):.1f}%")
