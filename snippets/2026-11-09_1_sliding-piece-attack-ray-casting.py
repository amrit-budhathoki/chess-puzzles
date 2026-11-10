# Title: Sliding Piece Attack Ray Casting

# Puzzle: Determine if a square is attacked by sliding pieces (rook, bishop, queen)
# using ray casting along four diagonal and four orthogonal directions.
# Idea: Cast rays from the target square in all 8 directions. Stop when hitting
# a piece and check if it can attack along that ray. Verify against brute force.

def is_attacked_by_sliding(board, target_row, target_col, by_color):
    """Check if target square is attacked by opponent sliding pieces.
    board: 8x8 list, None or ('P','N','B','R','Q','K', piece_color)
    by_color: 'white' or 'black' - the attacking side
    """
    # Directions: (row_delta, col_delta)
    # Orthogonal (rook/queen): up, down, left, right
    # Diagonal (bishop/queen): 4 diagonals
    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),  # orthogonal
        (-1, -1), (-1, 1), (1, -1), (1, 1)  # diagonal
    ]
    
    for dr, dc in directions:
        r, c = target_row + dr, target_col + dc
        while 0 <= r < 8 and 0 <= c < 8:
            cell = board[r][c]
            if cell is not None:
                piece, color = cell
                if color == by_color:
                    # Check if piece can attack along this direction
                    is_orthogonal = (dr == 0 or dc == 0)
                    is_diagonal = (dr != 0 and dc != 0)
                    if (piece == 'R' and is_orthogonal) or \
                       (piece == 'B' and is_diagonal) or \
                       (piece == 'Q'):
                        return True
                break
            r += dr
            c += dc
    return False

def is_attacked_brute_force(board, target_row, target_col, by_color):
    """Brute force: check all pieces of by_color if they attack target."""
    for r in range(8):
        for c in range(8):
            if board[r][c] is None:
                continue
            piece, color = board[r][c]
            if color != by_color:
                continue
            # Check if this piece attacks target
            if piece == 'R' and (r == target_row or c == target_col):
                # Verify no pieces block the path
                if r == target_row:
                    path_clear = all(board[r][min(c,target_col)+i] is None 
                                   for i in range(1, abs(target_col-c)))
                else:
                    path_clear = all(board[min(r,target_row)+i][c] is None 
                                   for i in range(1, abs(target_row-r)))
                if path_clear:
                    return True
            elif piece == 'B':
                dr, dc = target_row - r, target_col - c
                if abs(dr) == abs(dc) and dr != 0:
                    path_clear = all(board[r+i*dr//abs(dr)][c+i*dc//abs(dc)] is None 
                                   for i in range(1, abs(dr)))
                    if path_clear:
                        return True
            elif piece == 'Q':
                dr, dc = target_row - r, target_col - c
                if dr == 0 or dc == 0 or (abs(dr) == abs(dc) and dr != 0):
                    if dr == 0 and dc == 0:
                        continue
                    steps = max(abs(dr), abs(dc))
                    if dr == 0:
                        path_clear = all(board[r][min(c,target_col)+i] is None 
                                       for i in range(1, steps))
                    elif dc == 0:
                        path_clear = all(board[min(r,target_row)+i][c] is None 
                                       for i in range(1, steps))
                    else:
                        path_clear = all(board[r+i*dr//steps][c+i*dc//steps] is None 
                                       for i in range(1, steps))
                    if path_clear:
                        return True
    return False

# Test: Empty board with one rook attacking a square
board = [[None]*8 for _ in range(8)]
board[0][0] = ('R', 'white')
target = (4, 0)

ray_result = is_attacked_by_sliding(board, target[0], target[1], 'white')
brute_result = is_attacked_brute_force(board, target[0], target[1], 'white')
print(f"Rook at a1 attacks e1? Ray: {ray_result}, Brute: {brute_result}, Match: {ray_result == brute_result}")

# Test: Bishop with blocking piece
board[2][2] = ('P', 'black')
board[4][4] = ('B', 'white')
ray_result = is_attacked_by_sliding(board, 6, 6, 'white')
brute_result = is_attacked_brute_force(board, 6, 6, 'white')
print(f"Bishop at e5 attacks g7 (pawn blocks at c3)? Ray: {ray_result}, Brute: {brute_result}, Match: {ray_result == brute_result}")

# Test: Queen attacking diagonally
board = [[None]*8 for _ in range(8)]
board[3][3] = ('Q', 'white')
ray_result = is_attacked_by_sliding(board, 5, 5, 'white')
brute_result = is_attacked_brute_force(board, 5, 5, 'white')
print(f"Queen at d4 attacks f6? Ray: {ray_result}, Brute: {brute_result}, Match: {ray_result == brute_result}")

print("\nAll tests passed!" if all([
    is_attacked_by_sliding(board, 5, 5, 'white') == is_attacked_brute_force(board, 5, 5, 'white')
]) else "Test mismatch!")
