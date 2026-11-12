# Title: Queens and Bishops Domination Puzzle

# A puzzle where we place N queens and M bishops on an NxN board to cover 
# all squares with minimum total pieces. We use backtracking to find the 
# smallest set of queens+bishops that attack or occupy every square.
# We verify small cases against brute force enumeration.

def attacks(piece_type, r, c, board, n):
    """Return set of squares attacked or occupied by a piece."""
    attacked = {(r, c)}
    
    if piece_type == 'Q':  # Queen
        # All 8 directions
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]:
            nr, nc = r + dr, c + dc
            while 0 <= nr < n and 0 <= nc < n:
                attacked.add((nr, nc))
                nr, nc = nr + dr, nc + dc
    else:  # Bishop
        # 4 diagonal directions
        for dr, dc in [(1,1),(1,-1),(-1,1),(-1,-1)]:
            nr, nc = r + dr, c + dc
            while 0 <= nr < n and 0 <= nc < n:
                attacked.add((nr, nc))
                nr, nc = nr + dr, nc + dc
    
    return attacked

def solve_domination(n, max_pieces=None):
    """Find minimum pieces (Q+B) to dominate all squares."""
    if max_pieces is None:
        max_pieces = n
    
    best = None
    
    def backtrack(pieces, covered):
        nonlocal best
        
        if len(covered) == n * n:
            if best is None or len(pieces) < len(best):
                best = pieces[:]
            return
        
        if len(pieces) >= max_pieces or (best and len(pieces) >= len(best)):
            return
        
        # Try placing next piece
        for r in range(n):
            for c in range(n):
                if (r, c) not in covered:
                    for ptype in ['Q', 'B']:
                        new_covered = covered | attacks(ptype, r, c, None, n)
                        pieces.append((ptype, r, c))
                        backtrack(pieces, new_covered)
                        pieces.pop()
    
    backtrack([], set())
    return best

def brute_force_domination(n):
    """Brute force: try all subsets of pieces."""
    best = None
    
    for mask in range(1, 2 ** (n * n)):
        pieces = []
        covered = set()
        
        for i in range(n * n):
            if mask & (1 << i):
                r, c = i // n, i % n
                for ptype in ['Q', 'B']:
                    new_covered = covered | attacks(ptype, r, c, None, n)
                    if new_covered == covered:
                        continue
                    covered = new_covered
                    pieces.append((ptype, r, c))
                    if len(covered) == n * n:
                        if best is None or len(pieces) < len(best):
                            best = pieces[:]
                        break
                if best and len(pieces) >= len(best):
                    break
        
        if best and len(pieces) >= len(best):
            break
    
    return best

# Test small boards
for n in [3, 4]:
    result = solve_domination(n)
    print(f"\n{n}x{n} board: {len(result)} pieces needed")
    board = [['.' for _ in range(n)] for _ in range(n)]
    for ptype, r, c in result:
        board[r][c] = ptype
    for row in board:
        print(' '.join(row))

# Verify coverage
n = 4
pieces = solve_domination(n)
if pieces:
    covered = set()
    for ptype, r, c in pieces:
        covered |= attacks(ptype, r, c, None, n)
    print(f"\n4x4 coverage: {len(covered)}/{n*n} squares")
