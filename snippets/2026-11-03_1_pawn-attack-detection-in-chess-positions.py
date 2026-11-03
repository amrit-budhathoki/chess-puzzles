# Title: Pawn Attack Detection in Chess Positions

# Puzzle: Detect if a king is under attack by enemy pawns.
# Idea: Pawns attack diagonally one square forward (relative to their color).
# For white pawns: they attack squares diagonally upward (decreasing rank).
# For black pawns: they attack squares diagonally downward (increasing rank).
# We verify the formula by checking all possible pawn positions on a small board.

def pawn_attacks(pawn_pos, is_white):
    """Return set of squares attacked by a pawn at pawn_pos."""
    file, rank = pawn_pos
    attacks = set()
    
    if is_white:
        # White pawns attack diagonally upward (rank increases toward rank 8)
        target_rank = rank + 1
        if target_rank < 8:
            if file > 0:
                attacks.add((file - 1, target_rank))
            if file < 7:
                attacks.add((file + 1, target_rank))
    else:
        # Black pawns attack diagonally downward (rank decreases toward rank 1)
        target_rank = rank - 1
        if target_rank >= 0:
            if file > 0:
                attacks.add((file - 1, target_rank))
            if file < 7:
                attacks.add((file + 1, target_rank))
    
    return attacks

def is_king_in_check_from_pawns(king_pos, white_pawns, black_pawns, is_white_king):
    """Check if king is attacked by any pawn."""
    if is_white_king:
        # White king is attacked by black pawns
        for pawn in black_pawns:
            if king_pos in pawn_attacks(pawn, False):
                return True
    else:
        # Black king is attacked by white pawns
        for pawn in white_pawns:
            if king_pos in pawn_attacks(pawn, True):
                return True
    return False

def pos_to_notation(file, rank):
    return chr(ord('a') + file) + str(rank + 1)

# Test case 1: White king attacked by black pawn
print("Test 1: White king at e4, black pawn at d5")
white_king = (4, 3)  # e4
black_pawns = [(3, 4)]  # d5
result = is_king_in_check_from_pawns(white_king, [], black_pawns, True)
print(f"  King at {pos_to_notation(*white_king)}, pawn at {pos_to_notation(*black_pawns[0])}")
print(f"  Is in check: {result} (expected: True)\n")

# Test case 2: White king NOT attacked
print("Test 2: White king at e4, black pawn at d6 (too far)")
white_king = (4, 3)  # e4
black_pawns = [(3, 5)]  # d6
result = is_king_in_check_from_pawns(white_king, [], black_pawns, True)
print(f"  King at {pos_to_notation(*white_king)}, pawn at {pos_to_notation(*black_pawns[0])}")
print(f"  Is in check: {result} (expected: False)\n")

# Test case 3: Black king attacked by white pawn
print("Test 3: Black king at e5, white pawn at d4")
black_king = (4, 4)  # e5
white_pawns = [(3, 3)]  # d4
result = is_king_in_check_from_pawns(black_king, white_pawns, [], False)
print(f"  King at {pos_to_notation(*black_king)}, pawn at {pos_to_notation(*white_pawns[0])}")
print(f"  Is in check: {result} (expected: True)\n")

# Test case 4: Multiple pawns, one attacks
print("Test 4: Black king at c3, multiple white pawns (only b2 attacks)")
black_king = (2, 2)  # c3
white_pawns = [(1, 1), (3, 1)]  # b2, d2
result = is_king_in_check_from_pawns(black_king, white_pawns, [], False)
print(f"  King at {pos_to_notation(*black_king)}, pawns at {[pos_to_notation(*p) for p in white_pawns]}")
print(f"  Is in check: {result} (expected: True)\n")

# Brute force verification on small board
print("Brute force verification (all pawn positions on 4x4 board):")
errors = 0
for pawn_file in range(4):
    for pawn_rank in range(4):
        pawn = (pawn_file, pawn_rank)
        attacks = pawn_attacks(pawn, True)
        # Verify by checking all squares
        for king_file in range(4):
            for king_rank in range(4):
                king = (king_file, king_rank)
                formula_result = is_king_in_check_from_pawns(king, [pawn], [], True)
                expected = king in attacks
                if formula_result != expected:
                    errors += 1
                    print(f"  ERROR: pawn at {pos_to_notation(*pawn)}, king at {pos_to_notation(*king)}")

if errors == 0:
    print(f"  ✓ All 256 cases (4x4 board, 1 pawn) verified correctly")
else:
    print(f"  ✗ Found {errors} errors")
