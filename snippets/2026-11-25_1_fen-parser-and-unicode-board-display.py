# Title: FEN Parser and Unicode Board Display

# This program parses a FEN (Forsyth-Edwards Notation) string and displays
# the chess board using Unicode piece symbols. FEN is a standard notation for
# describing a particular board position in chess. The idea is to correctly
# interpret the piece placement part (first field) and render it visually.

def parse_fen_board(fen_string):
    """Parse FEN string and return 8x8 board representation."""
    board_part = fen_string.split()[0]
    board = []
    for rank in board_part.split('/'):
        row = []
        for char in rank:
            if char.isdigit():
                row.extend(['.'] * int(char))
            else:
                row.append(char)
        board.append(row)
    return board

def piece_to_unicode(piece):
    """Convert piece character to Unicode symbol."""
    piece_map = {
        'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
        'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟',
        '.': ' '
    }
    return piece_map.get(piece, '?')

def print_board(board):
    """Print the board with ranks and files labeled."""
    print("\n  a b c d e f g h")
    for rank_idx, row in enumerate(board):
        rank_num = 8 - rank_idx
        print(f"{rank_num} ", end="")
        for piece in row:
            print(piece_to_unicode(piece) + " ", end="")
        print(f" {rank_num}")
    print("  a b c d e f g h\n")

def validate_board_structure(board):
    """Verify the board has correct dimensions and valid pieces."""
    if len(board) != 8:
        return False
    for row in board:
        if len(row) != 8:
            return False
        for piece in row:
            if piece not in 'KQRBNPkqrbnp.':
                return False
    return True

# Test cases
test_fens = [
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",  # Starting position
    "r1bqkb1r/pppp1ppp/2n2n2/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4",  # Italian Game
    "8/8/8/4k3/8/8/4K3/8 w - - 0 1",  # King and king endgame
]

print("FEN Parser and Unicode Board Display")
print("=" * 40)

for fen in test_fens:
    board = parse_fen_board(fen)
    
    if not validate_board_structure(board):
        print(f"Invalid board structure for: {fen[:30]}...")
        continue
    
    print(f"FEN: {fen[:50]}...")
    print_board(board)
    
    # Verify board has 32 pieces (optional check)
    piece_count = sum(1 for row in board for piece in row if piece != '.')
    print(f"Piece count: {piece_count}\n")

print("All test cases processed successfully!")
