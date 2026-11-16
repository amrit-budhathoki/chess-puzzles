# Title: Queen Pair Placement Efficiency Analysis

# Given an N×N chessboard, count all ways to place two queens and classify them
# as attacking or non-attacking. Use combinatorics (total pairs) minus attacking pairs.
# For attacking pairs, count queen-to-queen attack vectors (horizontal, vertical, diagonal).
# Verify formula against brute force for small boards (N=4,5,6).

def queens_attack(r1, c1, r2, c2):
    """Check if two queens at (r1,c1) and (r2,c2) attack each other."""
    return (r1 == r2 or c1 == c2 or abs(r1 - r2) == abs(c1 - c2))


def brute_force_pairs(n):
    """Brute force: enumerate all pairs and classify them."""
    attacking = 0
    non_attacking = 0
    for r1 in range(n):
        for c1 in range(n):
            for r2 in range(n):
                for c2 in range(n):
                    if (r1, c1) < (r2, c2):  # avoid double counting
                        if queens_attack(r1, c1, r2, c2):
                            attacking += 1
                        else:
                            non_attacking += 1
    return attacking, non_attacking


def formula_pairs(n):
    """Calculate using formula: total pairs - attacking pairs."""
    total_pairs = n * n * (n * n - 1) // 2
    
    # Count attacking pairs:
    # - Same row: n rows, each has C(n,2) = n*(n-1)/2 pairs
    # - Same column: same as rows
    # - Diagonals: count pairs on each diagonal
    
    same_row = n * (n * (n - 1) // 2)
    same_col = n * (n * (n - 1) // 2)
    
    diagonal_pairs = 0
    # Diagonals going down-right (/)
    for offset in range(-(n-1), n):
        cells_on_diag = n - abs(offset)
        if cells_on_diag >= 2:
            diagonal_pairs += cells_on_diag * (cells_on_diag - 1) // 2
    
    # Diagonals going down-left (\)
    for offset in range(-(n-1), n):
        cells_on_diag = n - abs(offset)
        if cells_on_diag >= 2:
            diagonal_pairs += cells_on_diag * (cells_on_diag - 1) // 2
    
    attacking = same_row + same_col + diagonal_pairs
    non_attacking = total_pairs - attacking
    
    return attacking, non_attacking


def visualize_board(n, q1, q2):
    """Draw board with two queens marked."""
    board = [['.' for _ in range(n)] for _ in range(n)]
    board[q1[0]][q1[1]] = 'Q'
    board[q2[0]][q2[1]] = 'Q'
    for row in board:
        print(' '.join(row))


print("=" * 50)
print("TWO-QUEEN PLACEMENT ANALYSIS")
print("=" * 50)

# Verify formula against brute force for small boards
for n in [4, 5, 6]:
    bf_att, bf_non = brute_force_pairs(n)
    fm_att, fm_non = formula_pairs(n)
    
    total = bf_att + bf_non
    
    print(f"\nBoard size: {n}×{n}")
    print(f"Total ways to place 2 queens: {total}")
    print(f"  Attacking pairs:     {bf_att} (formula: {fm_att}) {'✓' if bf_att == fm_att else '✗'}")
    print(f"  Non-attacking pairs: {bf_non} (formula: {fm_non}) {'✓' if bf_non == fm_non else '✗'}")

# Show example for N=4
print("\n" + "=" * 50)
print("Example: One attacking pair (4×4 board)")
print("=" * 50)
visualize_board(4, (0, 0), (0, 3))
print("\nExample: One non-attacking pair (4×4 board)")
print("=" * 50)
visualize_board(4, (0, 0), (2, 3))

# Summary for larger board
print("\n" + "=" * 50)
print("Summary for N=8 (standard chessboard)")
print("=" * 50)
att, non = formula_pairs(8)
total = att + non
print(f"Total pairs: {total}")
print(f"Attacking:     {att} ({100*att/total:.1f}%)")
print(f"Non-attacking: {non} ({100*non/total:.1f}%)")
