# Title: Two Queens Placement Count on NxN Board

# Puzzle: Count the number of ways to place two queens on an NxN chessboard.
# We compute both the total placements and attacking placements.
# Idea: Use combinatorics and brute force verification. Two queens attack each other
# if they share a row, column, or diagonal. Total ways = C(N²,2).
# Attacking pairs = count via geometry. Non-attacking = Total - Attacking.
# We verify the formula against brute force for small boards.

def queens_attack(r1, c1, r2, c2):
    """Check if two queens at (r1,c1) and (r2,c2) attack each other."""
    if r1 == r2 or c1 == c2:
        return True
    if abs(r1 - r2) == abs(c1 - c2):
        return True
    return False

def brute_force_count(n):
    """Count attacking and non-attacking pairs by brute force."""
    total = 0
    attacking = 0
    squares = [(r, c) for r in range(n) for c in range(n)]
    
    for i in range(len(squares)):
        for j in range(i + 1, len(squares)):
            r1, c1 = squares[i]
            r2, c2 = squares[j]
            total += 1
            if queens_attack(r1, c1, r2, c2):
                attacking += 1
    
    non_attacking = total - attacking
    return total, attacking, non_attacking

def formula_count(n):
    """Compute counts using formulas."""
    total = n * n * (n * n - 1) // 2  # C(n²,2)
    
    # Attacking pairs:
    # Same row: n rows, each with C(n,2) pairs = n * n*(n-1)/2
    same_row = n * n * (n - 1) // 2
    
    # Same column: n columns, each with C(n,2) pairs = n * n*(n-1)/2
    same_col = n * n * (n - 1) // 2
    
    # Diagonals (positive slope y=x+k): 
    # For each diagonal of length d, we get C(d,2) pairs
    diag_pos = 0
    for d in range(1, n):
        pairs = d * (d - 1) // 2
        diag_pos += 2 * pairs  # top-right and bottom-left diagonals
    diag_pos += 0  # main diagonal handled separately
    for d in range(2, n):
        diag_pos += d * (d - 1) // 2
    
    # Simpler: for each diagonal length d, add C(d,2)
    diag_pos = 0
    for offset in range(-(n-1), n):
        diag_len = n - abs(offset)
        pairs = diag_len * (diag_len - 1) // 2
        diag_pos += pairs
    
    # Negative slope diagonals (same count by symmetry)
    diag_neg = diag_pos
    
    attacking = same_row + same_col + diag_pos + diag_neg
    non_attacking = total - attacking
    
    return total, attacking, non_attacking

def main():
    print("Two Queens Placement Count\n")
    print("Verification: Formula vs Brute Force\n")
    
    for n in range(2, 7):
        bf_total, bf_attacking, bf_non_attacking = brute_force_count(n)
        fm_total, fm_attacking, fm_non_attacking = formula_count(n)
        
        match = (bf_total == fm_total and 
                 bf_attacking == fm_attacking and 
                 bf_non_attacking == fm_non_attacking)
        status = "✓" if match else "✗"
        
        print(f"N={n}x{n} Board {status}")
        print(f"  Total placements:        {bf_total:6d}")
        print(f"  Attacking pairs:         {bf_attacking:6d}")
        print(f"  Non-attacking pairs:     {bf_non_attacking:6d}")
        print()
    
    # Display example for N=4
    print("Example: 4x4 board showing one non-attacking pair")
    board = [['.' for _ in range(4)] for _ in range(4)]
    board[0][0] = 'Q'
    board[2][3] = 'Q'
    for row in board:
        print(' '.join(row))
    print("Queens at (0,0) and (2,3) do not attack each other")

if __name__ == "__main__":
    main()
