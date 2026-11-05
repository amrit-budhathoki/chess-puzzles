# Title: N Non-Attacking Rooks Enumeration

# A rook attacks all squares in its row and column.
# Placing N non-attacking rooks on an N×N board means exactly one rook per row
# and exactly one rook per column—this is equivalent to counting permutations.
# The answer is always N! We verify by brute-force backtracking for small N,
# then compute and display solutions for larger boards.

def count_rook_placements_backtrack(n):
    """Brute force: count all valid N non-attacking rook placements."""
    count = 0
    cols_used = set()
    
    def backtrack(row):
        nonlocal count
        if row == n:
            count += 1
            return
        for col in range(n):
            if col not in cols_used:
                cols_used.add(col)
                backtrack(row + 1)
                cols_used.remove(col)
    
    backtrack(0)
    return count

def factorial(n):
    """Compute N! directly."""
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def find_one_solution(n):
    """Find one example placement of N non-attacking rooks."""
    placement = []
    cols_used = set()
    
    def backtrack(row):
        if row == n:
            return True
        for col in range(n):
            if col not in cols_used:
                cols_used.add(col)
                placement.append((row, col))
                if backtrack(row + 1):
                    return True
                placement.pop()
                cols_used.remove(col)
        return False
    
    backtrack(0)
    return placement

def draw_board(n, placement):
    """Draw the board with rooks marked as 'R'."""
    board = [['.' for _ in range(n)] for _ in range(n)]
    for row, col in placement:
        board[row][col] = 'R'
    for row in board:
        print(' '.join(row))

# Verify formula against brute force for small values
print("=== Verification: N! formula vs brute force ===")
for n in range(1, 7):
    formula_result = factorial(n)
    brute_force_result = count_rook_placements_backtrack(n)
    match = "✓" if formula_result == brute_force_result else "✗"
    print(f"N={n}: N!={formula_result}, Brute Force={brute_force_result} {match}")

print("\n=== Example placements ===")
for n in [4, 5]:
    print(f"\nN={n} board with one valid placement:")
    placement = find_one_solution(n)
    draw_board(n, placement)
    total = factorial(n)
    print(f"Total valid placements: {total}")

print("\n=== Large board counts (formula only) ===")
for n in [8, 10, 12]:
    print(f"N={n}: {factorial(n):,} placements")
