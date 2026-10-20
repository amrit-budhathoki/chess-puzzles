# Title: Attack Coverage by Each Chess Piece Type

# This program calculates how many squares each piece type (pawn, knight, bishop, rook, queen, king)
# attacks from every position on a standard 8x8 chessboard. We use geometric rules for each piece
# type and verify results against brute-force enumeration for correctness.

def get_attacked_squares(piece, row, col):
    """Return set of (r, c) squares attacked by piece at (row, col)."""
    attacked = set()
    
    if piece == 'P':  # White pawn attacks diagonally upward
        for dc in [-1, 1]:
            nr, nc = row - 1, col + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                attacked.add((nr, nc))
    
    elif piece == 'N':  # Knight
        for dr, dc in [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                attacked.add((nr, nc))
    
    elif piece == 'B':  # Bishop
        for dr, dc in [(1,1), (1,-1), (-1,1), (-1,-1)]:
            for dist in range(1, 8):
                nr, nc = row + dr*dist, col + dc*dist
                if 0 <= nr < 8 and 0 <= nc < 8:
                    attacked.add((nr, nc))
                else:
                    break
    
    elif piece == 'R':  # Rook
        for nr in range(8):
            if nr != row:
                attacked.add((nr, col))
        for nc in range(8):
            if nc != col:
                attacked.add((row, nc))
    
    elif piece == 'Q':  # Queen
        attacked.update(get_attacked_squares('B', row, col))
        attacked.update(get_attacked_squares('R', row, col))
    
    elif piece == 'K':  # King
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if 0 <= nr < 8 and 0 <= nc < 8:
                    attacked.add((nr, nc))
    
    return attacked

def attack_count_formula(piece, row, col):
    """Calculate attack count using geometric formulas."""
    if piece == 'P':
        return 2 if 0 < col < 7 else 1
    
    elif piece == 'N':
        # Count valid knight moves from position
        count = 0
        for dr, dc in [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]:
            if 0 <= row + dr < 8 and 0 <= col + dc < 8:
                count += 1
        return count
    
    elif piece == 'B':
        # Sum lengths of diagonals in 4 directions
        return (min(row, col) + min(7-row, 7-col) + 
                min(row, 7-col) + min(7-row, col))
    
    elif piece == 'R':
        return 14  # Always 7 horizontal + 7 vertical
    
    elif piece == 'Q':
        return attack_count_formula('B', row, col) + attack_count_formula('R', row, col)
    
    elif piece == 'K':
        corners = [(0,0), (0,7), (7,0), (7,7)]
        edges = [(r, c) for r in range(8) for c in range(8) 
                 if (r in [0,7] or c in [0,7]) and (r,c) not in corners]
        if (row, col) in corners:
            return 3
        elif (row, col) in edges:
            return 5
        else:
            return 8
    
    return 0

# Test: verify formulas match brute force
print("Verification: Formulas vs Brute Force")
print("-" * 50)
pieces = ['P', 'N', 'B', 'R', 'Q', 'K']
all_match = True
for piece in pieces:
    mismatches = 0
    for r in range(8):
        for c in range(8):
            brute = len(get_attacked_squares(piece, r, c))
            formula = attack_count_formula(piece, r, c)
            if brute != formula:
                mismatches += 1
                all_match = False
    print(f"{piece}: {'✓ PASS' if mismatches == 0 else f'✗ FAIL ({mismatches} mismatches)'}")

print("\n" + "="*50)
print("Attack Coverage Statistics")
print("="*50)

for piece in pieces:
    counts = [attack_count_formula(piece, r, c) for r in range(8) for c in range(8)]
    print(f"\n{piece} (Pawn={piece=='P'}, Knight={piece=='N'}, Bishop={piece=='B'}, Rook={piece=='R'}, Queen={piece=='Q'}, King={piece=='K'})")
    print(f"  Min attacks: {min(counts)}, Max attacks: {max(counts)}, Avg: {sum(counts)/64:.1f}")
    
    # Show heatmap
    print("  Heatmap:")
    for r in range(8):
        row_str = "    "
        for c in range(8):
            count = attack_count_formula(piece, r, c)
            row_str += f"{count:2d} "
        print(row_str)
