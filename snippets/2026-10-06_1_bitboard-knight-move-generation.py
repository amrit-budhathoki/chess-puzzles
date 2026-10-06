# Title: Bitboard Knight Move Generation

# A bitboard is a 64-bit integer where each bit represents a square on a chess board.
# This program generates all possible knight moves from a given square using bitboard tricks.
# We precompute knight move masks (which squares a knight can reach from each square)
# and validate the results against brute force enumeration.

def square_to_bit(rank, file):
    """Convert rank (0-7) and file (0-7) to a bit position."""
    return rank * 8 + file

def bit_to_square(bit):
    """Convert bit position to (rank, file)."""
    return (bit // 8, bit % 8)

def generate_knight_moves_brute(rank, file):
    """Brute force: return all valid knight moves from (rank, file)."""
    moves = []
    deltas = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), 
              (1, -2), (1, 2), (2, -1), (2, 1)]
    for dr, df in deltas:
        nr, nf = rank + dr, file + df
        if 0 <= nr < 8 and 0 <= nf < 8:
            moves.append((nr, nf))
    return moves

def generate_knight_moves_bitboard(square_bit):
    """Bitboard approach: compute knight moves using bit operations."""
    rank, file = bit_to_square(square_bit)
    moves_bb = 0
    
    deltas = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), 
              (1, -2), (1, 2), (2, -1), (2, 1)]
    for dr, df in deltas:
        nr, nf = rank + dr, file + df
        if 0 <= nr < 8 and 0 <= nf < 8:
            moves_bb |= (1 << square_to_bit(nr, nf))
    
    return moves_bb

def precompute_knight_masks():
    """Precompute knight move masks for all 64 squares."""
    masks = [0] * 64
    for sq in range(64):
        masks[sq] = generate_knight_moves_bitboard(sq)
    return masks

def bitboard_to_squares(bb):
    """Convert a bitboard to list of square indices."""
    squares = []
    for i in range(64):
        if bb & (1 << i):
            squares.append(i)
    return squares

def print_board_with_moves(start_sq, knight_moves_bb):
    """Print an 8x8 board showing knight position and reachable squares."""
    print(f"\nKnight on square {start_sq} (rank {start_sq // 8}, file {start_sq % 8}):")
    for rank in range(7, -1, -1):
        row = f"{rank} "
        for file in range(8):
            sq = rank * 8 + file
            if sq == start_sq:
                row += "N "
            elif knight_moves_bb & (1 << sq):
                row += "* "
            else:
                row += ". "
        print(row)
    print("  0 1 2 3 4 5 6 7")

# Main program
knight_masks = precompute_knight_masks()

# Test a few squares
test_squares = [0, 27, 63]  # corner, center-ish, opposite corner

print("Knight Move Validation (Bitboard vs Brute Force):")
print("=" * 50)

all_correct = True
for sq in test_squares:
    rank, file = bit_to_square(sq)
    brute_moves = generate_knight_moves_brute(rank, file)
    bb_moves = knight_masks[sq]
    bb_squares = bitboard_to_squares(bb_moves)
    
    brute_set = set((r * 8 + f) for r, f in brute_moves)
    bb_set = set(bb_squares)
    
    match = brute_set == bb_set
    all_correct = all_correct and match
    
    print(f"Square {sq}: {len(brute_set)} moves - {'✓' if match else '✗ MISMATCH'}")
    print_board_with_moves(sq, bb_moves)

print("=" * 50)
print(f"All tests passed: {all_correct}")

# Show statistics
move_counts = [bin(knight_masks[sq]).count('1') for sq in range(64)]
print(f"\nMove count statistics:")
print(f"  Minimum: {min(move_counts)} (corner/edge squares)")
print(f"  Maximum: {max(move_counts)} (central squares)")
print(f"  Average: {sum(move_counts) / 64:.1f}")
