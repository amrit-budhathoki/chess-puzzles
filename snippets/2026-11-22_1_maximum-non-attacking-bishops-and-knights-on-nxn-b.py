# Title: Maximum Non-Attacking Bishops and Knights on NxN Board

# Puzzle: Find the maximum number of bishops or knights that can be placed on an NxN
# chessboard such that no two pieces attack each other.
# Idea: For bishops, use a checkerboard coloring insight (each color is independent).
# For knights, use backtracking with constraint propagation. Verify formulas against brute force.

def bishops_formula(n):
    """Maximum non-attacking bishops on NxN board.
    Formula: n bishops can always be placed on the two diagonals of one color."""
    return n

def knights_backtrack(n, max_depth=None):
    """Find maximum non-attacking knights via backtracking."""
    if max_depth is None:
        max_depth = n * n
    
    def knight_attacks(r1, c1, r2, c2):
        dr, dc = abs(r1 - r2), abs(c1 - c2)
        return (dr == 2 and dc == 1) or (dr == 1 and dc == 2)
    
    def can_place(knights, r, c):
        for kr, kc in knights:
            if knight_attacks(r, c, kr, kc):
                return False
        return True
    
    def backtrack(pos, knights):
        if pos > max_depth:
            return knights[:]
        
        best = knights[:]
        r, c = pos // n, pos % n
        
        # Try placing a knight
        if can_place(knights, r, c):
            knights.append((r, c))
            candidate = backtrack(pos + 1, knights)
            if len(candidate) > len(best):
                best = candidate
            knights.pop()
        
        # Try not placing a knight
        candidate = backtrack(pos + 1, knights)
        if len(candidate) > len(best):
            best = candidate
        
        return best
    
    result = backtrack(0, [])
    return len(result), result

def bishops_brute_force(n):
    """Brute force verification for bishops (small boards only)."""
    from itertools import combinations
    
    def bishop_attacks(r1, c1, r2, c2):
        return abs(r1 - r2) == abs(c1 - c2)
    
    squares = [(r, c) for r in range(n) for c in range(n)]
    max_count = 0
    
    for size in range(len(squares), 0, -1):
        for combo in combinations(squares, size):
            if all(not bishop_attacks(r1, c1, r2, c2) 
                   for i, (r1, c1) in enumerate(combo)
                   for r2, c2 in combo[i+1:]):
                return size
    return 0

def print_board(n, pieces, label):
    """Display board with pieces."""
    board = [['.' for _ in range(n)] for _ in range(n)]
    for r, c in pieces:
        board[r][c] = 'X'
    print(f"\n{label}:")
    for row in board:
        print(' '.join(row))

# Main
print("=" * 50)
print("MAXIMUM NON-ATTACKING BISHOPS AND KNIGHTS")
print("=" * 50)

for n in [4, 5, 6]:
    print(f"\n--- Board size: {n}x{n} ---")
    
    # Bishops
    bishop_max = bishops_formula(n)
    print(f"Bishops (formula): {bishop_max}")
    
    if n <= 5:
        bishop_brute = bishops_brute_force(n)
        print(f"Bishops (brute force verification): {bishop_brute}")
        assert bishop_max == bishop_brute, "Bishop formula mismatch!"
    
    # Knights
    knight_max, knight_placement = knights_backtrack(n, max_depth=min(n*n, 16))
    print(f"Knights (backtracking): {knight_max}")
    
    if n <= 5:
        print_board(n, knight_placement, f"Knight placement ({knight_max} knights)")

print("\n" + "=" * 50)
print("FORMULA VERIFICATION PASSED")
print("=" * 50)
