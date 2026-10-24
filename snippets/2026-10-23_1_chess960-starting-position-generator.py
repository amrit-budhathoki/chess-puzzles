# Title: Chess960 Starting Position Generator

# Chess960 (Fischer Random Chess) uses a random legal starting position
# instead of the standard chess setup. This generator creates valid Chess960
# positions by placing pieces randomly while respecting the rules:
# - Bishops on opposite colors
# - King between rooks
# - Pawns on rank 2/7
# We verify by checking a few generated positions against the rules.

import random

def generate_chess960():
    """Generate a valid Chess960 starting position."""
    # Place bishops on opposite colored squares (a1 is dark in Chess960 context)
    # Rank 1: 8 squares indexed 0-7
    light_squares = [1, 3, 5, 7]
    dark_squares = [0, 2, 4, 6]
    
    bishop1_pos = random.choice(dark_squares)
    bishop2_pos = random.choice(light_squares)
    
    # Remaining 6 positions for queen, king, rooks, knight
    remaining = [i for i in range(8) if i != bishop1_pos and i != bishop2_pos]
    
    # Place queen, knight randomly in remaining positions
    queen_idx = random.randint(0, len(remaining) - 1)
    queen_pos = remaining.pop(queen_idx)
    
    knight_idx = random.randint(0, len(remaining) - 1)
    knight_pos = remaining.pop(knight_idx)
    
    # Remaining 4 positions: two rooks and king
    # King must be between rooks
    rook1_pos = remaining[0]
    rook2_pos = remaining[3]
    king_pos = remaining[random.randint(1, 2)]
    
    # Verify king is between rooks
    min_rook = min(rook1_pos, rook2_pos)
    max_rook = max(rook1_pos, rook2_pos)
    if not (min_rook < king_pos < max_rook):
        # Swap to ensure king is between
        king_pos, rook2_pos = rook2_pos, king_pos
    
    # Build position array (index 0-7 = files a-h on rank 1)
    position = [None] * 8
    position[bishop1_pos] = 'b'  # dark bishop
    position[bishop2_pos] = 'b'  # light bishop
    position[queen_pos] = 'q'
    position[knight_pos] = 'n'
    position[rook1_pos] = 'r'
    position[rook2_pos] = 'r'
    position[king_pos] = 'k'
    
    return position

def is_valid_chess960(pos):
    """Verify a position satisfies Chess960 rules."""
    if len(pos) != 8 or None in pos:
        return False
    
    # Check bishops on opposite colors
    bishop_positions = [i for i, p in enumerate(pos) if p == 'b']
    if len(bishop_positions) != 2:
        return False
    if (bishop_positions[0] + bishop_positions[1]) % 2 == 0:
        return False  # Same color
    
    # Check king between rooks
    rook_positions = [i for i, p in enumerate(pos) if p == 'r']
    king_pos = pos.index('k')
    if min(rook_positions) >= king_pos or max(rook_positions) <= king_pos:
        return False
    
    # Check piece counts
    if pos.count('q') != 1 or pos.count('n') != 1:
        return False
    if pos.count('r') != 2 or pos.count('k') != 1:
        return False
    
    return True

def position_to_fen_rank(pos):
    """Convert position array to FEN rank string."""
    fen = ""
    for piece in pos:
        if piece:
            fen += piece.upper()
        else:
            fen += "1"
    return fen

def draw_position(pos):
    """Draw the Chess960 position on rank 1."""
    files = "abcdefgh"
    line = "Rank 1: "
    for i, piece in enumerate(pos):
        line += files[i] + ":"
        line += (piece.upper() if piece else "-") + " "
    return line

# Generate and validate several Chess960 positions
print("Chess960 Starting Position Generator")
print("=" * 50)

valid_count = 0
for trial in range(10):
    pos = generate_chess960()
    is_valid = is_valid_chess960(pos)
    valid_count += is_valid
    
    fen_rank = position_to_fen_rank(pos)
    print(f"\nPosition {trial + 1}: {draw_position(pos)}")
    print(f"FEN rank: {fen_rank} | Valid: {is_valid}")

print("\n" + "=" * 50)
print(f"Generated 10 positions: {valid_count}/10 valid")
