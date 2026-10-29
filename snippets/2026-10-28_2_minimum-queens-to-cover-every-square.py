# Title: Minimum Queens to Cover Every Square

# Puzzle: Find the minimum number of queens needed on an NxN chessboard
# such that every square is either occupied by a queen or attacked by at least one queen.
# Idea: A queen covers a square if it's on the same row, column, or diagonal.
# We use backtracking with pruning to find the minimum set, then verify against brute force for small boards.

from itertools import combinations

def queen_covers(qrow, qcol, row, col):
    """Check if a queen at (qrow, qcol) covers square (row, col)."""
    return qrow == row or qcol == col or abs(qrow - qcol) == abs(row - col)

def is_all_covered(n, queens):
    """Check if all squares on an NxN board are covered by the given queens."""
    for row in range(n):
        for col in range(n):
            covered = any(queen_covers(qr, qc, row, col) for qr, qc in queens)
            if not covered:
                return False
    return True

def min_queens_backtrack(n, max_queens=None):
    """Find minimum queens needed via backtracking."""
    if max_queens is None:
        max_queens = n
    
    for num_queens in range(1, max_queens + 1):
        squares = [(r, c) for r in range(n) for c in range(n)]
        
        def backtrack(idx, chosen):
            if len(chosen) == num_queens:
                if is_all_covered(n, chosen):
                    return chosen[:]
                return None
            
            if idx >= len(squares):
                return None
            
            r, c = squares[idx]
            chosen.append((r, c))
            result = backtrack(idx + 1, chosen)
            if result:
                return result
            chosen.pop()
            
            result = backtrack(idx + 1, chosen)
            return result
        
        result = backtrack(0, [])
        if result:
            return result
    
    return None

def min_queens_bruteforce(n, max_queens=None):
    """Find minimum queens needed via brute force (slow, for verification)."""
    if max_queens is None:
        max_queens = n
    
    for num_queens in range(1, max_queens + 1):
        squares = [(r, c) for r in range(n) for c in range(n)]
        for combo in combinations(squares, num_queens):
            if is_all_covered(n, combo):
                return list(combo)
    
    return None

def draw_board(n, queens):
    """Draw the board with queens marked."""
    queen_set = set(queens)
    for row in range(n):
        line = ""
        for col in range(n):
            if (row, col) in queen_set:
                line += "Q "
            else:
                line += ". "
        print(line)
    print()

print("Minimum Queens to Cover Every Square\n")

# Test small boards with brute force verification
for n in [3, 4, 5]:
    print(f"Board size: {n}x{n}")
    
    result_backtrack = min_queens_backtrack(n, max_queens=n)
    result_bruteforce = min_queens_bruteforce(n, max_queens=n)
    
    min_count_bt = len(result_backtrack) if result_backtrack else -1
    min_count_bf = len(result_bruteforce) if result_bruteforce else -1
    
    print(f"  Backtracking found: {min_count_bt} queens")
    print(f"  Brute force found:  {min_count_bf} queens")
    
    if min_count_bt == min_count_bf:
        print("  ✓ Results match!")
        draw_board(n, result_backtrack)
    else:
        print("  ✗ Mismatch!")
    
    print()

# Larger boards (backtracking only)
for n in [6, 7, 8]:
    print(f"Board size: {n}x{n}")
    result = min_queens_backtrack(n, max_queens=min(n, 6))
    if result:
        print(f"  Minimum queens needed: {len(result)}")
        draw_board(n, result)
    else:
        print(f"  No solution found with <= 6 queens\n")
