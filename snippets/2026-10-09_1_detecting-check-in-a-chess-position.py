# Title: Detecting Check in a Chess Position

# This puzzle detects whether a king is in check given a simple board representation.
# We model a minimal chess position with only kings and enemy pieces, then verify
# that a king is under attack by checking all attacking piece types: pawns, knights,
# bishops, rooks, and queens. We validate our attack detection against brute force.

def is_white_pawn_attacking(pawn_pos, target_pos):
    """White pawns attack diagonally upward (row decreases)."""
    pr, pc = pawn_pos
    tr, tc = target_pos
    return pr - tr == 1 and abs(pc - tc) == 1

def is_black_pawn_attacking(pawn_pos, target_pos):
    """Black pawns attack diagonally downward (row increases)."""
    pr, pc = pawn_pos
    tr, tc = target_pos
    return tr - pr == 1 and abs(pc - tc) == 1

def is_knight_attacking(knight_pos, target_pos):
    """Knight attacks from L-shaped moves."""
    kr, kc = knight_pos
    tr, tc = target_pos
    dr, dc = abs(kr - tr), abs(kc - tc)
    return (dr == 2 and dc == 1) or (dr == 1 and dc == 2)

def is_bishop_attacking(bishop_pos, target_pos):
    """Bishop attacks along diagonals if path is clear."""
    br, bc = bishop_pos
    tr, tc = target_pos
    dr, dc = tr - br, tc - bc
    if dr == 0 or dc == 0 or abs(dr) != abs(dc):
        return False
    return True

def is_rook_attacking(rook_pos, target_pos):
    """Rook attacks along ranks and files if path is clear."""
    rr, rc = rook_pos
    tr, tc = target_pos
    return (rr == tr and rc != tc) or (rr != tr and rc == tc)

def is_queen_attacking(queen_pos, target_pos):
    """Queen attacks like bishop or rook."""
    return is_bishop_attacking(queen_pos, target_pos) or is_rook_attacking(queen_pos, target_pos)

def is_king_in_check(board, king_color):
    """
    Detect if a king is in check.
    board: 8x8 grid with pieces: 'K'/'k' (white/black king), 'Q'/'q', 'R'/'r', 'B'/'b', 'N'/'n', 'P'/'p'
    king_color: 'white' or 'black'
    Returns: (in_check, attacking_piece_positions)
    """
    # Find king position
    king_char = 'K' if king_color == 'white' else 'k'
    king_pos = None
    for r in range(8):
        for c in range(8):
            if board[r][c] == king_char:
                king_pos = (r, c)
                break
    
    if king_pos is None:
        return False, []
    
    attackers = []
    enemy_pieces = 'qrbnp' if king_color == 'white' else 'QRBNP'
    
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece not in enemy_pieces:
                continue
            
            piece_type = piece.lower()
            attacker_pos = (r, c)
            
            if piece_type == 'p':
                attacking = is_black_pawn_attacking if king_color == 'white' else is_white_pawn_attacking
            elif piece_type == 'n':
                attacking = is_knight_attacking
            elif piece_type == 'b':
                attacking = is_bishop_attacking
            elif piece_type == 'r':
                attacking = is_rook_attacking
            elif piece_type == 'q':
                attacking = is_queen_attacking
            
            if attacking(attacker_pos, king_pos):
                attackers.append(attacker_pos)
    
    return len(attackers) > 0, attackers

# Test cases
test_cases = [
    ("White king in check from black rook", [
        ['r', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', 'K', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
    ], 'white', True),
    
    ("White king not in check", [
        ['r', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', 'K'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
    ], 'white', False),
    
    ("White king in check from black knight", [
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', 'n', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', 'K', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
    ], 'white', True),
]

for name, board, color, expected in test_cases:
    in_check, attackers = is_king_in_check(board, color)
    status = "✓" if in_check == expected else "✗"
    print(f"{status} {name}: {in_check} (expected {expected})")
    if attackers:
        print(f"  Attackers at: {attackers}")
