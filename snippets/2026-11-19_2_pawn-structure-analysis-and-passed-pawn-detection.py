# Title: Pawn Structure Analysis and Passed Pawn Detection

# This program parses a FEN string and analyzes pawn structure.
# It detects passed pawns (pawns with no enemy pawns blocking their advance).
# A passed pawn is one where no enemy pawn can stop it from promoting.
# We validate the passed pawn detection by checking all squares ahead.

def parse_fen(fen):
    """Parse FEN string and return board as 8x8 list."""
    board = []
    rows = fen.split()[0].split('/')
    for row in rows:
        rank = []
        for char in row:
            if char.isdigit():
                rank.extend(['.'] * int(char))
            else:
                rank.append(char)
        board.append(rank)
    return board

def print_board(board):
    """Print board with Unicode chess pieces."""
    pieces = {
        'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
        'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟',
        '.': '·'
    }
    print("\n  a b c d e f g h")
    for i, rank in enumerate(board):
        print(f"{8-i} {' '.join(pieces.get(sq, sq) for sq in rank)} {8-i}")
    print("  a b c d e f g h\n")

def find_passed_pawns(board):
    """Find all passed pawns on the board."""
    passed = {'white': [], 'black': []}
    
    for row in range(8):
        for col in range(8):
            sq = board[row][col]
            if sq == 'P':  # White pawn
                is_passed = True
                # Check columns col-1, col, col+1 for all squares ahead
                for check_row in range(row - 1, -1, -1):
                    for check_col in range(max(0, col-1), min(8, col+2)):
                        if board[check_row][check_col] == 'p':
                            is_passed = False
                            break
                    if not is_passed:
                        break
                if is_passed:
                    passed['white'].append((row, col))
            
            elif sq == 'p':  # Black pawn
                is_passed = True
                # Check columns col-1, col, col+1 for all squares ahead
                for check_row in range(row + 1, 8):
                    for check_col in range(max(0, col-1), min(8, col+2)):
                        if board[check_row][check_col] == 'P':
                            is_passed = False
                            break
                    if not is_passed:
                        break
                if is_passed:
                    passed['black'].append((row, col))
    
    return passed

def square_name(row, col):
    """Convert board coordinates to algebraic notation."""
    return chr(ord('a') + col) + str(8 - row)

# Test with classic pawn structure puzzle
fen = "8/pp6/8/4P3/3p4/8/PP6/8 w - - 0 1"
print("FEN:", fen)
board = parse_fen(fen)
print_board(board)

passed = find_passed_pawns(board)
print("Passed Pawns Analysis:")
print(f"White passed pawns: {[square_name(r, c) for r, c in passed['white']]}")
print(f"Black passed pawns: {[square_name(r, c) for r, c in passed['black']]}")

# Verify with another position
fen2 = "8/8/8/PP1p4/2P5/8/8/8 w - - 0 1"
print("\n" + "="*40)
print("FEN:", fen2)
board2 = parse_fen(fen2)
print_board(board2)

passed2 = find_passed_pawns(board2)
print("Passed Pawns Analysis:")
print(f"White passed pawns: {[square_name(r, c) for r, c in passed2['white']]}")
print(f"Black passed pawns: {[square_name(r, c) for r, c in passed2['black']]}")
