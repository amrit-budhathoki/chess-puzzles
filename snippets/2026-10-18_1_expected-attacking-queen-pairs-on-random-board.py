# Title: Expected Attacking Queen Pairs on Random Board

# Puzzle: Given N queens randomly placed on an NxN chessboard,
# calculate the expected number of attacking pairs.
# Solution: Two queens attack each other if they share a row, column, or diagonal.
# For random placement, we sum probabilities: P(same row) + P(same col) + P(same diag).
# For each pair of queens, probability they're on same row = (N-1)/(N²-1),
# same for columns. Diagonals are trickier: count available diagonal pairs.
# We verify with brute force enumeration on small boards.

import random
from itertools import combinations

def queens_attack(pos1, pos2):
    """Check if two queen positions attack each other."""
    r1, c1 = pos1
    r2, c2 = pos2
    return (r1 == r2 or c1 == c2 or 
            abs(r1 - r2) == abs(c1 - c2))

def count_attacking_pairs_brute(positions):
    """Brute force: count attacking pairs in given position list."""
    count = 0
    for pos1, pos2 in combinations(positions, 2):
        if queens_attack(pos1, pos2):
            count += 1
    return count

def expected_attacking_pairs(n, num_queens):
    """
    Calculate expected attacking pairs analytically.
    For random placement of num_queens on nxn board.
    """
    if num_queens > n * n:
        return 0
    
    total_squares = n * n
    pair_count = num_queens * (num_queens - 1) // 2
    
    # Probability two random queens share a row
    p_row = (n - 1) / (total_squares - 1)
    
    # Probability two random queens share a column
    p_col = (n - 1) / (total_squares - 1)
    
    # For diagonals: count pairs on same diagonal
    diag_pairs = 0
    for d in range(-(n-1), n):
        length = n - abs(d)
        if length > 1:
            diag_pairs += length * (length - 1) // 2
    
    # Two diagonals (main and anti)
    total_diag_pairs = 2 * diag_pairs
    p_diag = total_diag_pairs / (total_squares * (total_squares - 1) // 2)
    
    expected = pair_count * (p_row + p_col + p_diag)
    return expected

def simulate_attacking_pairs(n, num_queens, trials=10000):
    """Monte Carlo simulation of attacking pairs."""
    total = 0
    for _ in range(trials):
        squares = list(range(n * n))
        random.shuffle(squares)
        positions = [(s // n, s % n) for s in squares[:num_queens]]
        total += count_attacking_pairs_brute(positions)
    return total / trials

def draw_board(positions, n):
    """Draw board with queens marked as Q."""
    board = [['.' for _ in range(n)] for _ in range(n)]
    for r, c in positions:
        board[r][c] = 'Q'
    for row in board:
        print(' '.join(row))
    print()

# Test on small boards
print("=== Verification on Small Boards ===\n")

for n in [4, 5, 6]:
    for num_q in [2, 3, 4]:
        if num_q > n:
            continue
        
        expected = expected_attacking_pairs(n, num_q)
        simulated = simulate_attacking_pairs(n, num_q, trials=5000)
        
        print(f"Board {n}x{n}, {num_q} queens:")
        print(f"  Expected (formula):  {expected:.4f}")
        print(f"  Simulated (5k runs): {simulated:.4f}")
        print(f"  Difference:          {abs(expected - simulated):.4f}\n")

# Large board example
print("=== Large Board Example ===\n")
n, num_q = 8, 8
expected = expected_attacking_pairs(n, num_q)
simulated = simulate_attacking_pairs(n, num_q, trials=10000)

print(f"Standard chessboard: {n}x{n}, {num_q} queens")
print(f"Expected attacking pairs: {expected:.2f}")
print(f"Simulated (10k runs):      {simulated:.2f}\n")

# Show one random configuration
print("Random 8x8 board with 8 queens:")
squares = list(range(64))
random.shuffle(squares)
positions = [(s // 8, s % 8) for s in squares[:8]]
draw_board(positions, 8)
print(f"Attacking pairs in this configuration: {count_attacking_pairs_brute(positions)}")
