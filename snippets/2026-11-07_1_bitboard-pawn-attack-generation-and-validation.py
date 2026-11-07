# Title: Bitboard Pawn Attack Generation and Validation

# A bitboard is a 64-bit integer representing a chess board (one bit per square).
# This program demonstrates pawn attack generation using bitboard shifts and masks.
# Pawns attack diagonally one square forward. We compute attacks for white and black
# pawns separately, then verify against a brute-force approach for correctness.

def square_to_bit(row, col):
    """Convert (row, col) to bit position. Row 0 is rank 1 (white's side)."""
    return 1 << (row * 8 + col)

def bit_to_square(bit):
    """Convert bit position back to (row, col)."""
    pos = bit.bit_length() - 1
    return divmod(pos, 8)

def print_bitboard(bb, label=""):
    """Display a bitboard as an 8x8 grid."""
    if label:
        print(label)
    for row in range(7, -1, -1):
        for col in range(8):
            bit = (bb >> (row * 8 + col)) & 1
            print("X" if bit else ".", end=" ")
        print(f" (rank {row + 1})")
    print()

def white_pawn_attacks_bitboard(pawns):
    """
    Compute all squares attacked by white pawns using bitboard shifts.
    White pawns move up (increasing row). They attack diagonally up-left and up-right.
    """
    # Shift up-left: pawns move from row to row+1, col to col-1
    # This is: shift left 1 bit (col-1) and left 8 bits (row+1) = left 9 bits
    # But exclude file A (leftmost column wraps around), so mask out col 7 after shift
    left_attacks = (pawns << 9) & 0xfefefefefefefefe
    # Shift up-right: col+1, row+1 = right 7 bits
    # Exclude file H (rightmost), mask out col 0 after shift
    right_attacks = (pawns << 7) & 0x7f7f7f7f7f7f7f7f
    return left_attacks | right_attacks

def black_pawn_attacks_bitboard(pawns):
    """
    Compute all squares attacked by black pawns using bitboard shifts.
    Black pawns move down (decreasing row). They attack diagonally down-left and down-right.
    """
    left_attacks = (pawns >> 7) & 0xfefefefefefefefe
    right_attacks = (pawns >> 9) & 0x7f7f7f7f7f7f7f7f
    return left_attacks | right_attacks

def white_pawn_attacks_bruteforce(pawns):
    """Brute force: check each pawn, add its attack squares."""
    attacks = 0
    for row in range(8):
        for col in range(8):
            if (pawns >> (row * 8 + col)) & 1:
                # Pawn at (row, col) attacks (row+1, col-1) and (row+1, col+1)
                if row < 7:
                    if col > 0:
                        attacks |= 1 << ((row + 1) * 8 + col - 1)
                    if col < 7:
                        attacks |= 1 << ((row + 1) * 8 + col + 1)
    return attacks

def black_pawn_attacks_bruteforce(pawns):
    """Brute force: check each pawn, add its attack squares."""
    attacks = 0
    for row in range(8):
        for col in range(8):
            if (pawns >> (row * 8 + col)) & 1:
                # Pawn at (row, col) attacks (row-1, col-1) and (row-1, col+1)
                if row > 0:
                    if col > 0:
                        attacks |= 1 << ((row - 1) * 8 + col - 1)
                    if col < 7:
                        attacks |= 1 << ((row - 1) * 8 + col + 1)
    return attacks

# Test case 1: white pawns on starting position
white_pawns_start = 0x00FF  # Rank 2 (row 1)
white_attacks_fast = white_pawn_attacks_bitboard(white_pawns_start)
white_attacks_slow = white_pawn_attacks_bruteforce(white_pawns_start)
print("White pawns starting position (rank 2):")
print_bitboard(white_pawns_start, "Pawns:")
print_bitboard(white_attacks_fast, "Attacks (bitboard):")
assert white_attacks_fast == white_attacks_slow, "White pawn attack mismatch!"
print("✓ White pawn attacks verified\n")

# Test case 2: black pawns on starting position
black_pawns_start = 0xFF00000000000000  # Rank 7 (row 6)
black_attacks_fast = black_pawn_attacks_bitboard(black_pawns_start)
black_attacks_slow = black_pawn_attacks_bruteforce(black_pawns_start)
print("Black pawns starting position (rank 7):")
print_bitboard(black_pawns_start, "Pawns:")
print_bitboard(black_attacks_fast, "Attacks (bitboard):")
assert black_attacks_fast == black_attacks_slow, "Black pawn attack mismatch!"
print("✓ Black pawn attacks verified\n")

# Test case 3: scattered pawns
scattered = square_to_bit(3, 2) | square_to_bit(4, 5) | square_to_bit(2, 7)
attacks_fast = white_pawn_attacks_bitboard(scattered)
attacks_slow = white_pawn_attacks_bruteforce(scattered)
print("Scattered white pawns:")
print_bitboard(scattered, "Pawns:")
print_bitboard(attacks_fast, "Attacks (bitboard):")
assert attacks_fast == attacks_slow, "Scattered pawn attack mismatch!"
print("✓ All bitboard pawn attack tests passed!")
