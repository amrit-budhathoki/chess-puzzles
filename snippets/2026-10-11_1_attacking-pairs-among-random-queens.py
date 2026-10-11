# Title: Attacking Pairs Among Random Queens

# Puzzle: Place N queens randomly on an NxN chessboard and count how many pairs
# attack each other. Two queens attack if they share a row, column, or diagonal.
# We'll verify our counting formula against brute force for small boards.

import random
from itertools import combinations

def count_attacking_pairs_formula(positions):
    """
    Count attacking pairs using row/column/diagonal analysis.
    positions: list of (row, col) tuples for queen placements
    
    Formula: For each direction (row/col/diag), count queens sharing that line,
    then sum C(count, 2) for each line.
    """
    if len(positions) == 0:
        return 0
    
    rows = {}
    cols = {}
    diag1 = {}  # row - col
    diag2 = {}  # row + col
    
    for r, c in positions:
        rows[r] = rows.get(r, 0) + 1
        cols[c] = cols.get(c, 0) + 1
        diag1[r - c] = diag1.get(r - c, 0) + 1
        diag2[r + c] = diag2.get(r + c, 0) + 1
    
    total = 0
    for count in rows.values():
        if count > 1:
            total += count * (count - 1) // 2
    for count in cols.values():
        if count > 1:
            total += count * (count - 1) // 2
    for count in diag1.values():
        if count > 1:
            total += count * (count - 1) // 2
    for count in diag2.values():
        if count > 1:
            total += count * (count - 1) // 2
    
    return total

def count_attacking_pairs_brute(positions):
    """
    Count attacking pairs by checking all pairs directly.
    """
    total = 0
    for (r1, c1), (r2, c2) in combinations(positions, 2):
        if r1 == r2 or c1 == c2 or abs(r1 - r2) == abs(c1 - c2):
            total += 1
    return total

def draw_board(n, positions):
    """Draw an nxn board with queens marked as Q."""
    board = [['.' for _ in range(n)] for _ in range(n)]
    for r, c in positions:
        board[r][c] = 'Q'
    for row in board:
        print(' '.join(row))
    print()

# Test: Verify formula against brute force for small cases
print("=== Verification: Formula vs Brute Force ===\n")

test_cases = [
    (4, [(0, 0), (1, 2), (2, 1), (3, 3)]),
    (5, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]),
    (5, [(0, 1), (1, 3), (2, 0), (3, 2), (4, 4)]),
]

for n, positions in test_cases:
    formula_result = count_attacking_pairs_formula(positions)
    brute_result = count_attacking_pairs_brute(positions)
    match = "✓" if formula_result == brute_result else "✗"
    print(f"Board {n}x{n}: Formula={formula_result}, Brute={brute_result} {match}")
    draw_board(n, positions)

# Main puzzle: random placement on 8x8 board
print("=== Random Queen Placement on 8x8 Board ===\n")

n = 8
num_queens = 8

random.seed(42)
random_positions = [(random.randint(0, n-1), random.randint(0, n-1)) 
                    for _ in range(num_queens)]

# Remove duplicates
random_positions = list(set(random_positions))

attacking = count_attacking_pairs_formula(random_positions)

print(f"Placed {len(random_positions)} queens randomly")
print(f"Attacking pairs: {attacking}\n")
draw_board(n, random_positions)

# Test with different queen counts
print("=== Statistics for Multiple Random Placements ===\n")
results = []
for num_q in [4, 6, 8, 10]:
    attacks_list = []
    for trial in range(10):
        positions = [(random.randint(0, 7), random.randint(0, 7)) 
                    for _ in range(num_q)]
        positions = list(set(positions))
        if len(positions) == num_q:
            attacks = count_attacking_pairs_formula(positions)
            attacks_list.append(attacks)
    
    if attacks_list:
        avg = sum(attacks_list) / len(attacks_list)
        print(f"{num_q} queens: avg attacking pairs = {avg:.1f}")
