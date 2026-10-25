# Title: Chess960 Starting Position Generator

# Chess960 (Fischer Random Chess) requires a legal starting position where:
# - Bishops are on opposite colors
# - King is between the two rooks
# - Pawns and knights can be anywhere else
# This generator creates valid positions by random placement with constraints.

import random

def is_valid_chess960(position):
    """Check if a position satisfies Chess960 rules."""
    # position is a list of 8 pieces for ranks 1-8 (excluding pawns)
    # Pieces: R=rook, N=knight, B=bishop, Q=queen, K=king
    
    # Find positions of bishops
    bishops = [i for i, p in enumerate(position) if p == 'B']
    if len(bishops) != 2:
        return False
    
    # Bishops must be on opposite colors (different parity)
    if (bishops[0] % 2) == (bishops[1] % 2):
        return False
    
    # Find positions of king and rooks
    king_pos = position.index('K')
    rooks = [i for i, p in enumerate(position) if p == 'R']
    
    # King must be between the two rooks
    if not (min(rooks) < king_pos < max(rooks)):
        return False
    
    return True

def generate_chess960():
    """Generate a random valid Chess960 starting position."""
    pieces = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
    
    while True:
        position = pieces.copy()
        random.shuffle(position)
        if is_valid_chess960(position):
            return position

def position_to_fen(position):
    """Convert piece position to FEN string for rank 1."""
    return '/'.join(position)

def draw_board(position):
    """Draw a simple text representation of the board with Chess960 position."""
    lines = []
    lines.append("  a b c d e f g h")
    lines.append("  ┌─┬─┬─┬─┬─┬─┬─┬─┐")
    
    # Rank 8 (black pieces - same as rank 1 for Chess960)
    rank8 = position
    line = "8 │" + "│".join(rank8) + "│ 8"
    lines.append(line)
    lines.append("  ├─┼─┼─┼─┼─┼─┼─┼─┤")
    
    # Ranks 7-2 (empty or pawns)
    for rank in range(7, 1, -1):
        if rank == 7:
            line = "7 │p│p│p│p│p│p│p│p│ 7"
        elif rank == 2:
            line = "2 │P│P│P│P│P│P│P│P│ 2"
        else:
            line = f"{rank} │ │ │ │ │ │ │ │ │ {rank}"
        lines.append(line)
        if rank > 2:
            lines.append("  ├─┼─┼─┼─┼─┼─┼─┼─┤")
    
    lines.append("  ├─┼─┼─┼─┼─┼─┼─┼─┤")
    
    # Rank 1 (white pieces)
    rank1 = position
    line = "1 │" + "│".join(rank1) + "│ 1"
    lines.append(line)
    lines.append("  └─┴─┴─┴─┴─┴─┴─┴─┘")
    lines.append("  a b c d e f g h")
    
    return '\n'.join(lines)

# Generate and display multiple Chess960 positions
print("Chess960 Starting Position Generator\n")
print("=" * 40)

for i in range(3):
    position = generate_chess960()
    print(f"\nPosition {i+1}: {' '.join(position)}")
    print(f"FEN rank 1: {position_to_fen(position)}")
    
    # Verify the position is valid
    bishops = [j for j, p in enumerate(position) if p == 'B']
    king_pos = position.index('K')
    rooks = [j for j, p in enumerate(position) if p == 'R']
    
    print(f"Bishops on files: {[chr(97+b) for b in bishops]} (opposite colors: {(bishops[0]%2) != (bishops[1]%2)})")
    print(f"King on file: {chr(97+king_pos)}, Rooks on files: {[chr(97+r) for r in rooks]}")
    print(f"King between rooks: {min(rooks) < king_pos < max(rooks)}")
    print(draw_board(position))
