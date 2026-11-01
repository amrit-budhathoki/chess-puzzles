# Title: Rook and Bishop Check Detection with Ray Casting

# This program detects whether a king is in check from rooks and bishops
# using ray casting along ranks, files, and diagonals. We validate the
# ray-casting formula against brute-force square-by-square checking.

def is_valid(r, c):
    return 0 <= r < 8 and 0 <= c < 8

def ray_cast_check(board, king_r, king_c):
    """Check if king at (king_r, king_c) is in check using ray casting."""
    # Directions: (rank, file), (rank, file), (diagonal), (diagonal)
    directions = [
        [(0, 1), (0, -1)],      # Rook: horizontal
        [(1, 0), (-1, 0)],      # Rook: vertical
        [(1, 1), (-1, -1)],     # Bishop: diagonal /
        [(1, -1), (-1, 1)]      # Bishop: diagonal \
    ]
    
    attacking_pieces = [('R', 'R'), ('R', 'R'), ('B', 'B'), ('B', 'B')]
    
    for dir_pair, pieces in zip(directions, attacking_pieces):
        for dr, dc in dir_pair:
            r, c = king_r + dr, king_c + dc
            while is_valid(r, c):
                piece = board[r][c]
                if piece != '.':
                    if piece.upper() in pieces:
                        return True
                    break
                r += dr
                c += dc
    
    return False

def brute_force_check(board, king_r, king_c):
    """Brute force: check every square to see if it attacks the king."""
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece == '.':
                continue
            
            if piece.upper() == 'R':
                if r == king_r or c == king_c:
                    if no_pieces_between(board, r, c, king_r, king_c):
                        return True
            elif piece.upper() == 'B':
                if abs(r - king_r) == abs(c - king_c):
                    if no_pieces_between(board, r, c, king_r, king_c):
                        return True
    
    return False

def no_pieces_between(board, r1, c1, r2, c2):
    """Check if path is clear between two squares."""
    dr = 0 if r1 == r2 else (1 if r2 > r1 else -1)
    dc = 0 if c1 == c2 else (1 if c2 > c1 else -1)
    r, c = r1 + dr, c1 + dc
    while (r, c) != (r2, c2):
        if board[r][c] != '.':
            return False
        r += dr
        c += dc
    return True

def board_to_string(board):
    """Pretty print the board."""
    print("  a b c d e f g h")
    for i in range(8):
        print(f"{8-i} {' '.join(board[i])} {8-i}")
    print("  a b c d e f g h\n")

# Test cases
test_cases = [
    {
        "name": "Rook check on same rank",
        "board": [
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['R', '.', '.', '.', 'k', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
        ],
        "king": (3, 4),
        "expected": True
    },
    {
        "name": "Bishop check on diagonal",
        "board": [
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', 'B', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', 'k', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
        ],
        "king": (3, 4),
        "expected": True
    },
    {
        "name": "No check (piece blocked)",
        "board": [
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['R', '.', 'p', '.', 'k', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
        ],
        "king": (3, 4),
        "expected": False
    },
    {
        "name": "No check (no attacker)",
        "board": [
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', 'k', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
        ],
        "king": (3, 4),
        "expected": False
    },
]

print("Chess Check Detection: Ray Casting vs Brute Force\n")

for test in test_cases:
    board = test["board"]
    kr, kc = test["king"]
    expected = test["expected"]
    
    ray_result = ray_cast_check(board, kr, kc)
    brute_result = brute_force_check(board, kr, kc)
    
    match = "✓" if ray_result == brute_result == expected else "✗"
    print(f"{match} {test['name']}")
    board_to_string(board)
    print(f"  Ray Cast: {ray_result}, Brute Force: {brute_result}, Expected: {expected}\n")
