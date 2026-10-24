# Title: Checkmate Detection via Piece Mobility

# Puzzle: Given a chess position, determine if the side to move is in checkmate.
# A position is checkmate if: (1) king is in check, (2) no legal move escapes check.
# We detect check by seeing if enemy pieces attack the king.
# We verify checkmate by brute-force checking all possible moves.

def board_to_fen_like(board):
    """Convert 8x8 board to readable format. 'K'=white king, 'k'=black king, etc."""
    return '\n'.join(' '.join(row) for row in board)

def is_white(piece):
    return piece.isupper()

def is_black(piece):
    return piece.islower()

def find_piece(board, piece):
    """Find all positions of a piece on the board."""
    positions = []
    for r in range(8):
        for c in range(8):
            if board[r][c] == piece:
                positions.append((r, c))
    return positions

def is_attacked_by(board, king_r, king_c, by_white):
    """Check if a square is attacked by white (if by_white=True) or black pieces."""
    # Check pawn attacks
    pawn = 'P' if by_white else 'p'
    pawn_dir = -1 if by_white else 1  # White pawns move up (negative), black down (positive)
    for dc in [-1, 1]:
        pr, pc = king_r - pawn_dir, king_c + dc
        if 0 <= pr < 8 and 0 <= pc < 8 and board[pr][pc] == pawn:
            return True
    
    # Check knight attacks
    knight = 'N' if by_white else 'n'
    for dr, dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
        nr, nc = king_r + dr, king_c + dc
        if 0 <= nr < 8 and 0 <= nc < 8 and board[nr][nc] == knight:
            return True
    
    # Check bishop/queen diagonal attacks
    bishop = 'B' if by_white else 'b'
    queen = 'Q' if by_white else 'q'
    for dr, dc in [(-1,-1),(-1,1),(1,-1),(1,1)]:
        for i in range(1, 8):
            r, c = king_r + i*dr, king_c + i*dc
            if not (0 <= r < 8 and 0 <= c < 8):
                break
            if board[r][c] != '.':
                if board[r][c] in [bishop, queen]:
                    return True
                break
    
    # Check rook/queen straight attacks
    rook = 'R' if by_white else 'r'
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        for i in range(1, 8):
            r, c = king_r + i*dr, king_c + i*dc
            if not (0 <= r < 8 and 0 <= c < 8):
                break
            if board[r][c] != '.':
                if board[r][c] in [rook, queen]:
                    return True
                break
    
    # Check king attacks
    king = 'K' if by_white else 'k'
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            r, c = king_r + dr, king_c + dc
            if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == king:
                return True
    
    return False

def is_in_check(board, white_to_move):
    king = 'K' if white_to_move else 'k'
    positions = find_piece(board, king)
    if not positions:
        return False
    kr, kc = positions[0]
    return is_attacked_by(board, kr, kc, not white_to_move)

def is_checkmate(board, white_to_move):
    """Check if the side to move is in checkmate."""
    if not is_in_check(board, white_to_move):
        return False
    
    # Try all possible moves for the side to move
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if not piece or piece == '.':
                continue
            if (white_to_move and not is_white(piece)) or (not white_to_move and not is_black(piece)):
                continue
            
            # Try moving this piece to all squares
            for nr in range(8):
                for nc in range(8):
                    target = board[nr][nc]
                    # Can't capture own pieces
                    if target != '.' and ((white_to_move and is_white(target)) or (not white_to_move and is_black(target))):
                        continue
                    
                    # Make move (simplified: just swap, doesn't validate legality perfectly)
                    board[nr][nc] = piece
                    board[r][c] = '.'
                    
                    # Check if still in check after move
                    still_in_check = is_in_check(board, white_to_move)
                    
                    # Undo move
                    board[r][c] = piece
                    board[nr][nc] = target
                    
                    if not still_in_check:
                        return False
    
    return True

# Test case: fool's mate position (black just moved)
board = [
    ['r','n','b','q','k','b','n','r'],
    ['p','p','p','p','p','p','p','p'],
    ['.','.','.','.','.','.','.', '.'],
    ['.','.','.','.','.','.','.', '.'],
    ['.','.','.','.','.','.','.', 'P'],
    ['.','.','.','.','.','.','.', '.'],
    ['P','P','P','P','P','P','P', '.'],
    ['R','N','B','Q','K','B','N','R'],
]

print("Testing fool's mate (white to move):")
print(board_to_fen_like(board))
print(f"White in check: {is_in_check(board, True)}")
print(f"White in checkmate: {is_checkmate(board, True)}")

# Test case: simple back rank mate
board2 = [
    ['.','.','.','.','.','.','.', 'k'],
    ['.','.','.','.','.','.','.', 'p'],
    ['.','.','.','.','.','.','.', '.'],
    ['.','.','.','.','.','.','.', '.'],
    ['.','.','.','.','.','.','.', '.'],
    ['.','.','.','.','.','.','.', '.'],
    ['.','.','.','.','.','.','.', '.'],
    ['R','.','.','.','.','.','.','.'],
]

print("\nTesting back rank mate (black to move):")
print(board_to_fen_like(board2))
print(f"Black in check: {is_in_check(board2, False)}")
print(f"Black in checkmate: {is_checkmate(board2, False)}")
