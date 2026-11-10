# Title: Minimum Pieces to Control Every Square

# The puzzle: find the minimum number of chess pieces (any type) needed to
# control or occupy every square on an 8x8 board. We use a greedy approach:
# repeatedly place the piece that covers the most uncovered squares until
# all squares are covered. We verify against brute force for smaller boards.

def get_piece_coverage(piece_type, row, col, board_size=8):
    """Return set of squares controlled by a piece at (row, col)."""
    covered = {(row, col)}  # piece occupies its square
    
    if piece_type == 'queen':
        # horizontal and vertical
        for i in range(board_size):
            covered.add((row, i))
            covered.add((i, col))
        # diagonals
        for i in range(board_size):
            covered.add((row + i, col + i))
            covered.add((row + i, col - i))
            covered.add((row - i, col + i))
            covered.add((row - i, col - i))
    elif piece_type == 'rook':
        for i in range(board_size):
            covered.add((row, i))
            covered.add((i, col))
    elif piece_type == 'bishop':
        for i in range(board_size):
            covered.add((row + i, col + i))
            covered.add((row + i, col - i))
            covered.add((row - i, col + i))
            covered.add((row - i, col - i))
    elif piece_type == 'king':
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                covered.add((row + dr, col + dc))
    elif piece_type == 'knight':
        for dr, dc in [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]:
            covered.add((row + dr, col + dc))
    
    return {(r, c) for r, c in covered if 0 <= r < board_size and 0 <= c < board_size}

def greedy_cover(board_size, piece_type):
    """Greedy placement: repeatedly pick best piece until all squares covered."""
    all_squares = {(r, c) for r in range(board_size) for c in range(board_size)}
    uncovered = all_squares.copy()
    pieces = []
    
    while uncovered:
        best_pos = None
        best_coverage = set()
        for row in range(board_size):
            for col in range(board_size):
                coverage = get_piece_coverage(piece_type, row, col, board_size)
                new_coverage = coverage & uncovered
                if len(new_coverage) > len(best_coverage):
                    best_coverage = new_coverage
                    best_pos = (row, col)
        
        pieces.append(best_pos)
        uncovered -= best_coverage
    
    return pieces

def brute_force_min_cover(board_size, piece_type, max_pieces=8):
    """Exhaustive search for minimum pieces (only for small boards)."""
    from itertools import combinations
    
    all_squares = {(r, c) for r in range(board_size) for c in range(board_size)}
    all_positions = [(r, c) for r in range(board_size) for c in range(board_size)]
    
    for num_pieces in range(1, max_pieces + 1):
        for combo in combinations(all_positions, num_pieces):
            covered = set()
            for pos in combo:
                covered |= get_piece_coverage(piece_type, pos[0], pos[1], board_size)
            if covered == all_squares:
                return num_pieces
    return None

# Test on small board with brute force
print("=== Verification on 4x4 board ===")
for piece in ['queen', 'rook', 'bishop', 'king', 'knight']:
    greedy_result = len(greedy_cover(4, piece))
    optimal = brute_force_min_cover(4, piece, max_pieces=6)
    match = "✓" if greedy_result == optimal else "✗"
    print(f"{piece:8} greedy={greedy_result}, optimal={optimal} {match}")

# Solve for 8x8 board
print("\n=== Minimum pieces for 8x8 board ===")
results = {}
for piece in ['queen', 'rook', 'bishop', 'king', 'knight']:
    placement = greedy_cover(8, piece)
    results[piece] = placement
    print(f"{piece:8}: {len(placement)} pieces needed")
    print(f"  Positions: {placement[:5]}{'...' if len(placement) > 5 else ''}")

# Visualize queen solution
print("\n=== Queen placement visualization ===")
board = [['.' for _ in range(8)] for _ in range(8)]
for i, (r, c) in enumerate(results['queen']):
    board[r][c] = str(i + 1) if i < 9 else 'Q'
for row in board:
    print(' '.join(row))
