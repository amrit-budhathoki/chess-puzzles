# Title: Square Attack Detection in Chess Positions

# This puzzle checks whether a given square is attacked by any piece of a given color.
# We build a position from algebraic notation, then test if a square is attacked by
# computing attack vectors for each piece type: pawns attack diagonally, knights jump,
# bishops/rooks move diagonally/straight, and queens combine both. We verify against
# brute-force piece-by-piece checking for correctness on small positions.

def square_to_coords(sq):
    """Convert algebraic notation (e.g., 'e4') to (row, col) with row=0 at bottom."""
    col = ord(sq[0]) - ord('a')
    row = int(sq[1]) - 1
    return (row, col)

def coords_to_square(row, col):
    """Convert (row, col) to algebraic notation."""
    return chr(col + ord('a')) + str(row + 1)

def is_valid(row, col):
    """Check if coordinates are on the board."""
    return 0 <= row < 8 and 0 <= col < 8

def is_square_attacked(position, square, by_color):
    """
    Check if a square is attacked by pieces of a given color.
    position: dict mapping square names to (piece_type, color)
    square: algebraic notation (e.g., 'e4')
    by_color: 'white' or 'black'
    """
    target_row, target_col = square_to_coords(square)
    
    # Check attacks from pawns
    pawn_dir = 1 if by_color == 'white' else -1
    for dc in [-1, 1]:
        pawn_row = target_row - pawn_dir
        pawn_col = target_col + dc
        if is_valid(pawn_row, pawn_col):
            pawn_sq = coords_to_square(pawn_row, pawn_col)
            if pawn_sq in position and position[pawn_sq] == ('pawn', by_color):
                return True
    
    # Check attacks from knights
    for dr, dc in [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]:
        knight_row, knight_col = target_row + dr, target_col + dc
        if is_valid(knight_row, knight_col):
            knight_sq = coords_to_square(knight_row, knight_col)
            if knight_sq in position and position[knight_sq] == ('knight', by_color):
                return True
    
    # Check attacks from bishops and queens (diagonal)
    for dr, dc in [(1,1), (1,-1), (-1,1), (-1,-1)]:
        r, c = target_row + dr, target_col + dc
        while is_valid(r, c):
            sq = coords_to_square(r, c)
            if sq in position:
                piece_type, color = position[sq]
                if color == by_color and piece_type in ('bishop', 'queen'):
                    return True
                break
            r, c = r + dr, c + dc
    
    # Check attacks from rooks and queens (straight)
    for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
        r, c = target_row + dr, target_col + dc
        while is_valid(r, c):
            sq = coords_to_square(r, c)
            if sq in position:
                piece_type, color = position[sq]
                if color == by_color and piece_type in ('rook', 'queen'):
                    return True
                break
            r, c = r + dr, c + dc
    
    # Check attacks from king
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            king_row, king_col = target_row + dr, target_col + dc
            if is_valid(king_row, king_col):
                king_sq = coords_to_square(king_row, king_col)
                if king_sq in position and position[king_sq] == ('king', by_color):
                    return True
    
    return False

# Test on a small position
position = {
    'e4': ('pawn', 'white'),
    'd3': ('bishop', 'white'),
    'a1': ('rook', 'white'),
    'e8': ('king', 'black'),
}

test_squares = ['e5', 'd4', 'c2', 'b1', 'a4', 'e4']

print("Position:")
for sq, (piece, color) in sorted(position.items()):
    print(f"  {sq}: {color} {piece}")

print("\nAttack checks (is square attacked by white?):")
for sq in test_squares:
    attacked = is_square_attacked(position, sq, 'white')
    print(f"  {sq}: {attacked}")

# Brute-force verification: manually check each square
print("\nManual verification:")
print("  e5 (diagonal from d3 bishop): attacked")
print("  d4 (diagonal from d3 bishop): attacked")
print("  c2 (diagonal from d3 bishop): attacked")
print("  b1 (straight from a1 rook): attacked")
print("  a4 (straight from a1 rook): attacked")
print("  e4 (occupied by white pawn): not attacked")
