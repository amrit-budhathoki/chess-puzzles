# Title: FEN Parser and Unicode Chess Board Display

# This program parses a FEN (Forsyth-Edwards Notation) string and displays
# the chess position using Unicode chess piece symbols. FEN is a standard
# notation for describing a particular board position in chess. We extract
# the piece placement part and render it visually with proper Unicode glyphs.

def parse_fen(fen_string):
    """Parse FEN string and return 8x8 board representation."""
    board = []
    piece_part = fen_string.split()[0]
    
    for rank in piece_part.split('/'):
        row = []
        for char in rank:
            if char.isdigit():
                row.extend([' '] * int(char))
            else:
                row.append(char)
        board.append(row)
    return board

def piece_to_unicode(piece):
    """Convert FEN piece character to Unicode symbol."""
    unicode_map = {
        'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
        'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟',
        ' ': '·'
    }
    return unicode_map.get(piece, '?')

def print_board(board, title=""):
    """Print the chess board with Unicode pieces and coordinates."""
    if title:
        print(f"\n{title}")
    print("  ┌─────────────────────────────────────┐")
    for i, rank in enumerate(board):
        rank_num = 8 - i
        print(f"{rank_num} │ ", end="")
        for piece in rank:
            print(f" {piece_to_unicode(piece)} ", end="")
        print(f"│ {rank_num}")
    print("  └─────────────────────────────────────┘")
    print("    a  b  c  d  e  f  g  h")

# Example 1: Starting position
starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
board1 = parse_fen(starting_fen)
print_board(board1, "Starting Position")

# Example 2: After 1.e4
after_e4_fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR"
board2 = parse_fen(after_e4_fen)
print_board(board2, "After 1.e4")

# Example 3: A famous position (Scholar's Mate setup)
scholars_mate_fen = "rnbqkb1r/pppp1ppp/5n2/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R"
board3 = parse_fen(scholars_mate_fen)
print_board(board3, "Scholar's Mate Defense")

# Example 4: Endgame position
endgame_fen = "8/8/8/4k3/8/8/4K3/8"
board4 = parse_fen(endgame_fen)
print_board(board4, "King and King Endgame")

# Verification: Check that parsing handles all piece types and numbers correctly
test_fen = "r1bqkb1r/pppp1ppp/2n2n2/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R"
test_board = parse_fen(test_fen)
flat_count = sum(1 for row in test_board for piece in row if piece != ' ')
expected_pieces = 30
print(f"\nVerification: Counted {flat_count} pieces, expected {expected_pieces}")
assert flat_count == expected_pieces, "Piece count mismatch!"
print("✓ FEN parsing verified successfully")
