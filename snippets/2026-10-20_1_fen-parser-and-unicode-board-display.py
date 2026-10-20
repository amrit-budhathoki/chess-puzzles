# Title: FEN Parser and Unicode Board Display

# This program parses a FEN (Forsyth-Edwards Notation) string and displays
# the chess position using Unicode piece symbols. FEN is the standard way to
# represent a chess position in text. We extract the board portion, decode
# rank by rank (from rank 8 to rank 1), and render with Unicode characters.

def fen_to_board(fen):
    """Parse FEN string and return 8x8 board list."""
    board_fen = fen.split()[0]
    ranks = board_fen.split('/')
    board = []
    for rank in ranks:
        row = []
        for char in rank:
            if char.isdigit():
                row.extend(['.'] * int(char))
            else:
                row.append(char)
        board.append(row)
    return board

def print_board(board):
    """Print the board with Unicode pieces and coordinates."""
    piece_map = {
        'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
        'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟',
        '.': '·'
    }
    
    print("\n  a b c d e f g h")
    print("  ─────────────────")
    for i, row in enumerate(board):
        rank_num = 8 - i
        print(f"{rank_num}│", end="")
        for piece in row:
            print(f" {piece_map[piece]}", end="")
        print(f" │{rank_num}")
    print("  ─────────────────")
    print("  a b c d e f g h\n")

def count_pieces(board):
    """Count pieces by type."""
    counts = {}
    for row in board:
        for piece in row:
            if piece != '.':
                counts[piece] = counts.get(piece, 0) + 1
    return counts

# Test cases
test_fens = [
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR",  # Starting position
    "r1bqkb1r/pppp1ppp/2n2n2/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R",  # Italian Game
    "8/8/8/4k3/8/8/4K3/8",  # King and King endgame
]

for fen in test_fens:
    board = fen_to_board(fen)
    print(f"FEN: {fen}")
    print_board(board)
    pieces = count_pieces(board)
    print(f"Piece counts: {pieces}")
    total_pieces = sum(pieces.values())
    print(f"Total pieces: {total_pieces}")
    print("=" * 40 + "\n")
