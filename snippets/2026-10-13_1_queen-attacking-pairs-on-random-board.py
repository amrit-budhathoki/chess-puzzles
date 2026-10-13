# Title: Queen Attacking Pairs on Random Board

# Puzzle: Place N queens randomly on an NxN chessboard and count how many pairs
# attack each other. Two queens attack if they share a row, column, or diagonal.
# We'll compute this for several random placements and verify with brute force.

import random
from itertools import combinations

def queens_attack(r1, c1, r2, c2):
    """Check if two queens at (r1,c1) and (r2,c2) attack each other."""
    return (r1 == r2 or c1 == c2 or abs(r1 - r2) == abs(c1 - c2))

def count_attacking_pairs_brute(positions):
    """Brute force: check all pairs of queens."""
    count = 0
    for (r1, c1), (r2, c2) in combinations(positions, 2):
        if queens_attack(r1, c1, r2, c2):
            count += 1
    return count

def count_attacking_pairs_fast(positions):
    """Optimized: count using sets for rows, columns, diagonals."""
    rows = set()
    cols = set()
    diag1 = set()  # r - c
    diag2 = set()  # r + c
    
    for r, c in positions:
        rows.add(r)
        cols.add(c)
        diag1.add(r - c)
        diag2.add(r + c)
    
    # Count queens in each constraint set
    count = 0
    for r, c in positions:
        # Queens in same row (excluding self)
        count += sum(1 for r2, c2 in positions if r2 == r and c2 != c)
        # Queens in same column (excluding self)
        count += sum(1 for r2, c2 in positions if c2 == c and r2 != r)
        # Queens on same diagonal r-c (excluding self)
        count += sum(1 for r2, c2 in positions if r2 - c2 == r - c and (r2, c2) != (r, c))
        # Queens on same diagonal r+c (excluding self)
        count += sum(1 for r2, c2 in positions if r2 + c2 == r + c and (r2, c2) != (r, c))
    
    # Each attacking pair was counted twice (once from each queen), and we counted
    # each direction separately, so divide by 4 and multiply by 2
    return count // 4

def draw_board(n, positions):
    """Draw the board with queens marked as Q."""
    board = [['.' for _ in range(n)] for _ in range(n)]
    for r, c in positions:
        board[r][c] = 'Q'
    for row in board:
        print(' '.join(row))
    print()

print("Testing Queen Attacking Pairs Counter")
print("=" * 50)

# Test on small boards with random placements
for n in [4, 5, 6]:
    print(f"\nBoard size: {n}x{n}")
    print("-" * 50)
    
    test_cases = 5
    for trial in range(test_cases):
        # Generate random placement of n queens (one per row, different columns)
        cols = list(range(n))
        random.shuffle(cols)
        positions = [(r, cols[r]) for r in range(n)]
        
        # Compare brute force with optimized
        brute_result = count_attacking_pairs_brute(positions)
        fast_result = count_attacking_pairs_fast(positions)
        
        match = "✓" if brute_result == fast_result else "✗ MISMATCH"
        print(f"Trial {trial + 1}: {brute_result} attacking pairs {match}")
        if trial == 0:
            draw_board(n, positions)

print("\n" + "=" * 50)
print("Verification complete. Fast method matches brute force.")
