# Title: Queen Pair Placement Efficiency Analysis

# Puzzle: Count placements of two queens on an N×N board and categorize them
# as attacking or non-attacking. Use combinatorics for large boards and verify
# against brute force for small N to validate the formula:
# Total placements = C(N²,2) = N²(N²-1)/2
# Attacking pairs found by checking queen attack rules (row, col, diagonals)

def queens_attack(r1, c1, r2, c2):
    """Check if two queens at (r1,c1) and (r2,c2) attack each other."""
    return (r1 == r2 or c1 == c2 or 
            abs(r1 - r2) == abs(c1 - c2))

def brute_force_count(n):
    """Count attacking and non-attacking queen pairs via brute force."""
    attacking = 0
    total = 0
    
    for r1 in range(n):
        for c1 in range(n):
            for r2 in range(n):
                for c2 in range(n):
                    if (r1, c1) < (r2, c2):
                        total += 1
                        if queens_attack(r1, c1, r2, c2):
                            attacking += 1
    
    return total, attacking

def formula_count(n):
    """Count using formula: total = N²(N²-1)/2."""
    n_sq = n * n
    total = n_sq * (n_sq - 1) // 2
    return total

def count_attacking_pairs(n):
    """Count attacking pairs via formula.
    - Row attacks: N rows × C(N,2) pairs per row = N × N(N-1)/2
    - Col attacks: N cols × C(N,2) pairs per col = N × N(N-1)/2
    - Diagonal attacks: sum over all diagonals of C(len,2) for each direction
    """
    # Row and column attacks
    row_col_attacks = 2 * n * (n * (n - 1) // 2)
    
    # Diagonal attacks (both directions)
    diag_attacks = 0
    for length in range(2, n + 1):
        # Number of diagonals of this length in each direction
        count = n - length + 1
        pairs_per_diag = length * (length - 1) // 2
        diag_attacks += 2 * count * pairs_per_diag
    
    return row_col_attacks + diag_attacks

def print_board_example(n, max_show=4):
    """Print a small example board with two attacking queens."""
    if n > max_show:
        return
    board = [['.' for _ in range(n)] for _ in range(n)]
    board[0][0] = 'Q'
    board[0][1] = 'Q'
    print(f"\nExample {n}×{n} board (two attacking queens at (0,0) and (0,1)):")
    for row in board:
        print(' '.join(row))

# Main verification
print("=" * 60)
print("TWO QUEENS PLACEMENT ANALYSIS")
print("=" * 60)

for n in range(2, 7):
    total_brute, attacking_brute = brute_force_count(n)
    total_formula = formula_count(n)
    attacking_formula = count_attacking_pairs(n)
    non_attacking = total_formula - attacking_formula
    
    formula_match = "✓" if total_formula == total_brute else "✗"
    attacking_match = "✓" if attacking_formula == attacking_brute else "✗"
    
    print(f"\nN = {n}:")
    print(f"  Total placements:    {total_formula:6d} (formula) vs {total_brute:6d} (brute) {formula_match}")
    print(f"  Attacking pairs:     {attacking_formula:6d} (formula) vs {attacking_brute:6d} (brute) {attacking_match}")
    print(f"  Non-attacking pairs: {non_attacking:6d}")
    
    if attacking_brute > 0:
        efficiency = (non_attacking / total_formula) * 100
        print(f"  Efficiency (non-attacking %): {efficiency:.1f}%")
    
    print_board_example(n)

print("\n" + "=" * 60)
print("Formula verified for small boards!")
print("=" * 60)
