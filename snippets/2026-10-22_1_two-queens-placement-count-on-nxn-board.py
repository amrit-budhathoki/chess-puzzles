# Title: Two Queens Placement Count on NxN Board

"""
Puzzle: Count the number of ways to place two queens on an N×N chessboard.
We compute both:
1. Total placements (attacking or non-attacking)
2. Non-attacking placements only

Idea: For total placements, use the formula C(N²,2) = N²(N²-1)/2.
For non-attacking placements, subtract attacking pairs using queen attack patterns.
A queen attacks along rows, columns, and diagonals.
We verify formulas against brute force for small boards.
"""

def queens_attack(r1, c1, r2, c2):
    """Check if two queens at (r1,c1) and (r2,c2) attack each other."""
    return (r1 == r2 or c1 == c2 or 
            abs(r1 - r2) == abs(c1 - c2))

def brute_force_count(n):
    """Count placements by checking all pairs."""
    total = 0
    non_attacking = 0
    
    for r1 in range(n):
        for c1 in range(n):
            for r2 in range(n):
                for c2 in range(n):
                    if (r1, c1) < (r2, c2):  # Avoid counting same pair twice
                        total += 1
                        if not queens_attack(r1, c1, r2, c2):
                            non_attacking += 1
    
    return total, non_attacking

def formula_total_placements(n):
    """Total ways to place 2 queens = C(N²,2) = N²(N²-1)/2."""
    squares = n * n
    return squares * (squares - 1) // 2

def formula_attacking_pairs(n):
    """Count attacking pairs using symmetry."""
    attacking = 0
    
    # Same row: choose 2 from n queens per row, n rows
    attacking += n * (n * (n - 1) // 2)
    
    # Same column: choose 2 from n queens per column, n columns
    attacking += n * (n * (n - 1) // 2)
    
    # Diagonals (top-left to bottom-right)
    for length in range(1, n):
        attacking += 2 * (length * (length - 1) // 2)
    
    # Diagonals (top-right to bottom-left)
    for length in range(1, n):
        attacking += 2 * (length * (length - 1) // 2)
    
    return attacking

def formula_non_attacking(n):
    """Non-attacking placements = Total - Attacking."""
    total = formula_total_placements(n)
    attacking = formula_attacking_pairs(n)
    return total - attacking

def print_board_example(n):
    """Display one non-attacking placement example."""
    if n >= 3:
        print(f"\nExample: Two non-attacking queens on {n}×{n}:")
        board = [['.' for _ in range(n)] for _ in range(n)]
        board[0][0] = 'Q'
        board[n-1][n-1] = 'Q'
        for row in board:
            print(' '.join(row))

# Main execution
print("Two Queens Placement Analysis")
print("=" * 50)

test_sizes = [3, 4, 5, 8]

for n in test_sizes:
    print(f"\nBoard size: {n}×{n}")
    
    # Brute force
    bf_total, bf_non_attack = brute_force_count(n)
    
    # Formula
    fm_total = formula_total_placements(n)
    fm_attacking = formula_attacking_pairs(n)
    fm_non_attack = formula_non_attacking(n)
    
    # Verify
    assert bf_total == fm_total, f"Total mismatch at n={n}"
    assert bf_non_attack == fm_non_attack, f"Non-attacking mismatch at n={n}"
    
    print(f"  Total placements:        {fm_total}")
    print(f"  Attacking pairs:         {fm_attacking}")
    print(f"  Non-attacking placements: {fm_non_attack}")
    print(f"  ✓ Formula verified (brute force matches)")

print_board_example(5)
print("\n" + "=" * 50)
print("All formulas verified against brute force!")
