# Title: Chess960 Starting Position Generator

# Chess960 (Fischer Random Chess) randomizes the starting position while maintaining
# certain rules: bishops on opposite colors, king between rooks, pawns on rank 2/7.
# We generate valid Chess960 positions and display them in FEN notation and ASCII board.

import random

def generate_chess960_position():
    """Generate a valid Chess960 starting position."""
    # Place bishops on opposite colors
    light_bishop = random.randrange(0, 4) * 2  # 0, 2, 4, 6
    dark_bishop = random.randrange(0, 4) * 2 + 1  # 1, 3, 5, 7
    
    # Remaining squares for queen, king, and rooks
    remaining = [i for i in range(8) if i != light_bishop and i != dark_bishop]
    
    # Place queen on a random remaining square
    queen_idx = random.randint(0, len(remaining) - 1)
    queen = remaining.pop(queen_idx)
    
    # Place king between rooks: choose 2 positions for rooks, king goes between them
    rook_positions = random.sample(remaining, 2)
    rook_positions.sort()
    king = None
    for i in range(rook_positions[0] + 1, rook_positions[1]):
        if i in remaining:
            king = i
            break
    
    if king is None:
        return generate_chess960_position()  # Retry if no valid king position
    
    remaining.remove(king)
    for r in rook_positions:
        remaining.remove(r)
    
    # Place knights on remaining squares
    knights = random.sample(remaining, 2)
    
    # Build back rank
    back_rank = ['.' for _ in range(8)]
    back_rank[light_bishop] = 'B'
    back_rank[dark_bishop] = 'B'
    back_rank[queen] = 'Q'
    back_rank[king] = 'K'
    for r in rook_positions:
        back_rank[r] = 'R'
    for n in knights:
        back_rank[n] = 'N'
    
    return ''.join(back_rank)

def board_to_fen(back_rank_str):
    """Convert back rank string to full FEN position."""
    white_back = back_rank_str
    white_pawns = 'pppppppp'
    black_pawns = 'PPPPPPPP'
    black_back = back_rank_str.lower()
    
    fen = f"{black_back}/8/{black_pawns}/8/8/{white_pawns}/8/{white_back} w KQkq - 0 1"
    return fen

def print_board(back_rank_str):
    """Print Chess960 starting board in ASCII."""
    print("\n  a b c d e f g h")
    print("8 " + " ".join(back_rank_str.lower()) + " 8")
    print("7 p p p p p p p p 7")
    print("6 . . . . . . . . 6")
    print("5 . . . . . . . . 5")
    print("4 . . . . . . . . 4")
    print("3 . . . . . . . . 3")
    print("2 P P P P P P P P 2")
    print("1 " + " ".join(back_rank_str) + " 1")
    print("  a b c d e f g h\n")

def is_valid_chess960(back_rank_str):
    """Verify Chess960 constraints."""
    pieces = back_rank_str
    
    # Check for exactly one king, one queen, two rooks, two bishops, two knights
    if pieces.count('K') != 1 or pieces.count('Q') != 1:
        return False
    if pieces.count('R') != 2 or pieces.count('B') != 2 or pieces.count('N') != 2:
        return False
    
    # Bishops on opposite colors
    bishops = [i for i, p in enumerate(pieces) if p == 'B']
    if (bishops[0] % 2) == (bishops[1] % 2):
        return False
    
    # King between rooks
    rooks = [i for i, p in enumerate(pieces) if p == 'R']
    king_pos = pieces.index('K')
    if not (min(rooks) < king_pos < max(rooks)):
        return False
    
    return True

# Generate and display multiple Chess960 positions
print("Chess960 Starting Position Generator")
print("=" * 40)

for i in range(3):
    back_rank = generate_chess960_position()
    
    # Verify validity
    if not is_valid_chess960(back_rank):
        print(f"ERROR: Invalid position generated!")
        continue
    
    fen = board_to_fen(back_rank)
    print(f"\nPosition {i+1}:")
    print(f"Back rank: {back_rank}")
    print_board(back_rank)
    print(f"FEN: {fen}")

print("All positions generated successfully!")
