# Title: Bishop Reachability on Same-Colored Squares

# A bishop can only reach squares of the same color as its starting square.
# This puzzle demonstrates that bishops are confined to their color due to the
# alternating checkerboard pattern. We verify the formula: on an 8×8 board,
# each color has 32 squares, and a bishop can theoretically reach up to 13
# different squares (including its starting position) depending on placement.
# We compute reachable squares for each bishop position and verify our logic.

def square_color(row, col):
    """Return the color of a square: True for light (even sum), False for dark."""
    return (row + col) % 2 == 0

def bishop_reachable(bishop_row, bishop_col, board_size=8):
    """Return set of (row, col) tuples reachable by a bishop."""
    reachable = {(bishop_row, bishop_col)}
    
    # Four diagonal directions: up-left, up-right, down-left, down-right
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    
    for dr, dc in directions:
        r, c = bishop_row + dr, bishop_col + dc
        while 0 <= r < board_size and 0 <= c < board_size:
            reachable.add((r, c))
            r += dr
            c += dc
    
    return reachable

def verify_same_color_constraint():
    """Verify that all reachable squares have the same color as the bishop."""
    board_size = 8
    all_valid = True
    
    for row in range(board_size):
        for col in range(board_size):
            bishop_color = square_color(row, col)
            reachable = bishop_reachable(row, col, board_size)
            
            for r, c in reachable:
                target_color = square_color(r, c)
                if bishop_color != target_color:
                    all_valid = False
                    print(f"ERROR: Bishop at ({row},{col}) color {bishop_color} reached ({r},{c}) color {target_color}")
    
    return all_valid

def analyze_bishop_positions():
    """Analyze reachability statistics for all bishop positions."""
    board_size = 8
    light_squares_reachable = []
    dark_squares_reachable = []
    
    for row in range(board_size):
        for col in range(board_size):
            reachable_count = len(bishop_reachable(row, col, board_size))
            if square_color(row, col):
                light_squares_reachable.append(reachable_count)
            else:
                dark_squares_reachable.append(reachable_count)
    
    print("=== Bishop Reachability Analysis ===\n")
    print(f"Light squares reachable counts: min={min(light_squares_reachable)}, "
          f"max={max(light_squares_reachable)}, avg={sum(light_squares_reachable)/len(light_squares_reachable):.1f}")
    print(f"Dark squares reachable counts:  min={min(dark_squares_reachable)}, "
          f"max={max(dark_squares_reachable)}, avg={sum(dark_squares_reachable)/len(dark_squares_reachable):.1f}")
    
    print(f"\nTotal light squares on board: {len(light_squares_reachable)}")
    print(f"Total dark squares on board:  {len(dark_squares_reachable)}")
    
    # Count light/dark squares reachable from corner vs center
    corner_light = bishop_reachable(0, 0)
    center_light = bishop_reachable(3, 3)
    print(f"\nFrom corner (0,0): {len(corner_light)} squares reachable")
    print(f"From center (3,3): {len(center_light)} squares reachable")

def draw_bishop_reach(bishop_row, bishop_col):
    """Draw a visual board showing bishop and its reachable squares."""
    board_size = 8
    reachable = bishop_reachable(bishop_row, bishop_col, board_size)
    
    print(f"\nBishop at ({bishop_row},{bishop_col}) reaches {len(reachable)-1} other squares:")
    print("  ┌─" + "─┬─" * 7 + "─┐")
    
    for row in range(board_size):
        print(f"  │", end="")
        for col in range(board_size):
            if (row, col) == (bishop_row, bishop_col):
                print("B", end="")
            elif (row, col) in reachable:
                print("×", end="")
            else:
                print(" ", end="")
            print("│" if col < board_size - 1 else "│", end="")
        print()
        if row < board_size - 1:
            print("  ├─" + "─┼─" * 7 + "─┤")
    print("  └─" + "─┴─" * 7 + "─┘")

if __name__ == "__main__":
    # Verify the fundamental constraint
    if verify_same_color_constraint():
        print("✓ All reachable squares match bishop color\n")
    
    analyze_bishop_positions()
    draw_bishop_reach(3, 3)
    draw_bishop_reach(0, 0)
