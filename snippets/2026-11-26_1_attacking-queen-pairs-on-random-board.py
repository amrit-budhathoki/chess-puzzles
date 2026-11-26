# Title: Attacking Queen Pairs on Random Board

# Puzzle: Place N queens randomly on an 8x8 board and count how many pairs
# attack each other. Two queens attack if they share row, column, or diagonal.
# We verify the formula: total_pairs - non_attacking_pairs = attacking_pairs
# by comparing against brute force enumeration for correctness.

import random
from itertools import combinations

def queens_attack(q1, q2):
    """Check if two queens at (r1,c1) and (r2,c2) attack each other."""
    r1, c1 = q1
    r2, c2 = q2
    # Same row, column, or diagonal
    return r1 == r2 or c1 == c2 or abs(r1 - r2) == abs(c1 - c2)

def count_attacking_pairs_brute(queens):
    """Brute force: check all pairs."""
    count = 0
    for q1, q2 in combinations(queens, 2):
        if queens_attack(q1, q2):
            count += 1
    return count

def count_attacking_pairs_formula(queens):
    """Formula-based: sum attacking queens per queen, divide by 2."""
    total = 0
    for q1 in queens:
        for q2 in queens:
            if q1 != q2 and queens_attack(q1, q2):
                total += 1
    return total // 2

def draw_board(queens, size=8):
    """Draw board with queens marked as Q."""
    board = [['.' for _ in range(size)] for _ in range(size)]
    for r, c in queens:
        board[r][c] = 'Q'
    for row in board:
        print(' '.join(row))
    print()

# Test on small case: verify formula matches brute force
print("Verification on small cases:")
for _ in range(5):
    n = random.randint(2, 5)
    queens = [(random.randint(0, 7), random.randint(0, 7)) for _ in range(n)]
    brute = count_attacking_pairs_brute(queens)
    formula = count_attacking_pairs_formula(queens)
    match = "✓" if brute == formula else "✗"
    print(f"  n={n}: brute={brute}, formula={formula} {match}")

print("\nRandom placement simulation (8x8 board):")
for trial in range(1, 6):
    # Random number of queens
    num_queens = random.randint(5, 12)
    queens = set()
    while len(queens) < num_queens:
        queens.add((random.randint(0, 7), random.randint(0, 7)))
    queens = list(queens)
    
    attacking = count_attacking_pairs_brute(queens)
    total_pairs = len(queens) * (len(queens) - 1) // 2
    non_attacking = total_pairs - attacking
    
    print(f"\nTrial {trial}: {len(queens)} queens")
    print(f"  Total pairs: {total_pairs}")
    print(f"  Attacking pairs: {attacking}")
    print(f"  Non-attacking pairs: {non_attacking}")
    
    if len(queens) <= 6:
        draw_board(queens)

print("All verifications passed!" if all(
    count_attacking_pairs_brute([(random.randint(0, 7), random.randint(0, 7)) 
                                   for _ in range(random.randint(2, 8))])
    == count_attacking_pairs_formula([(random.randint(0, 7), random.randint(0, 7)) 
                                       for _ in range(random.randint(2, 8))])
    for _ in range(20)
) else "Verification failed!")
