# Title: Bitboard Move Generation and Popcount Verification

# This program demonstrates bitboard representation of chess positions and efficient
# move generation using bit manipulation. We represent each piece type as a 64-bit
# integer (one bit per square). We generate all legal king moves from a position and
# verify the popcount (number of set bits) matches brute-force counting.

def print_board(bitboard):
    """Display a bitboard as an 8x8 chess board."""
    for rank in range(7, -1, -1):
        row = ""
        for file in range(8):
            sq = rank * 8 + file
            row += "X " if (bitboard >> sq) & 1 else ". "
        print(f"{rank + 1} {row}")
    print("  a b c d e f g h")

def popcount(bb):
    """Count number of set bits in bitboard (Brian Kernighan's algorithm)."""
    count = 0
    while bb:
        bb &= bb - 1
        count += 1
    return count

def king_moves(square):
    """Generate bitboard of all squares a king on 'square' can move to."""
    bb = 1 << square
    moves = (bb << 8) | (bb >> 8) | (bb << 1) | (bb >> 1) | \
            (bb << 9) | (bb >> 9) | (bb << 7) | (bb >> 7)
    
    # Mask off edges to prevent wrapping
    not_a_file = 0xfefefefefefefefe
    not_h_file = 0x7f7f7f7f7f7f7f7f
    
    moves &= (not_a_file | not_h_file)
    if square % 8 == 0:  # on a-file
        moves &= not_a_file
    if square % 8 == 7:  # on h-file
        moves &= not_h_file
    
    return moves

def knight_moves(square):
    """Generate bitboard of all squares a knight on 'square' can move to."""
    bb = 1 << square
    moves = (bb << 17) | (bb >> 17) | (bb << 15) | (bb >> 15) | \
            (bb << 10) | (bb >> 10) | (bb << 6) | (bb >> 6)
    
    # Remove wrapping artifacts near file edges
    not_a_file = 0xfefefefefefefefe
    not_b_file = 0xfdfdfdfdfdfdfdfd
    not_g_file = 0x7f7f7f7f7f7f7f7f
    not_h_file = 0xbfbfbfbfbfbfbfbf
    
    if square % 8 <= 1:
        moves &= not_a_file & not_b_file
    elif square % 8 >= 6:
        moves &= not_g_file & not_h_file
    
    return moves

def verify_move_counts():
    """Verify popcount matches brute-force for all king and knight positions."""
    print("=== King Move Generation ===")
    test_squares = [0, 7, 28, 35, 63]  # corners and center
    for sq in test_squares:
        moves = king_moves(sq)
        count = popcount(moves)
        # Brute force: count neighbors
        file, rank = sq % 8, sq // 8
        brute_force = sum(1 for f in range(max(0, file-1), min(8, file+2))
                          for r in range(max(0, rank-1), min(8, rank+2))
                          if (f, r) != (file, rank))
        status = "✓" if count == brute_force else "✗"
        print(f"Square {sq:2d} (rank {rank}, file {file}): {count} moves {status}")
    
    print("\n=== Knight Move Generation ===")
    for sq in test_squares:
        moves = knight_moves(sq)
        count = popcount(moves)
        # Brute force knight moves
        file, rank = sq % 8, sq // 8
        knight_deltas = [(2,1), (2,-1), (-2,1), (-2,-1),
                         (1,2), (1,-2), (-1,2), (-1,-2)]
        brute_force = sum(1 for df, dr in knight_deltas
                          if 0 <= file + df < 8 and 0 <= rank + dr < 8)
        status = "✓" if count == brute_force else "✗"
        print(f"Square {sq:2d} (rank {rank}, file {file}): {count} moves {status}")
    
    print("\n=== Visualize King Moves from e4 (square 28) ===")
    moves_bb = king_moves(28)
    print_board(moves_bb | (1 << 28))

verify_move_counts()
