# Title: Count All Squares and Rectangles on a Chessboard

"""
On an 8x8 chessboard, count how many squares and rectangles can be formed.
This includes 1x1 squares up to 8x8, and all possible rectangles.

The formula for squares on an n×n board: sum of i² for i from 1 to n
The formula for rectangles on an n×n board: C(n+1,2) × C(n+1,2) where C(n,2) = n(n+1)/2

We verify these formulas against brute force counting for small boards.
"""

def count_squares_brute_force(n):
    """Count squares by checking all possible top-left corners and sizes."""
    count = 0
    # Try all possible square sizes from 1×1 to n×n
    for size in range(1, n + 1):
        # Try all possible positions for this size square
        for row in range(n - size + 1):
            for col in range(n - size + 1):
                count += 1
    return count

def count_rectangles_brute_force(n):
    """Count rectangles by checking all possible positions and dimensions."""
    count = 0
    # Try all possible widths and heights
    for width in range(1, n + 1):
        for height in range(1, n + 1):
            # Try all possible positions for this size rectangle
            for row in range(n - height + 1):
                for col in range(n - width + 1):
                    count += 1
    return count

def count_squares_formula(n):
    """Count squares using the mathematical formula."""
    return sum(i * i for i in range(1, n + 1))

def count_rectangles_formula(n):
    """Count rectangles using the mathematical formula.
    
    For an n×n board:
    - Number of ways to choose 2 horizontal lines from n+1 lines: C(n+1,2) = n(n+1)/2
    - Number of ways to choose 2 vertical lines from n+1 lines: C(n+1,2) = n(n+1)/2
    - Total rectangles = [n(n+1)/2]²
    """
    choose_2 = n * (n + 1) // 2
    return choose_2 * choose_2

def visualize_small_board(n):
    """Show rectangles on a small 3x3 board as example."""
    if n == 3:
        print("\nExample: 3×3 board with some rectangles highlighted:")
        print("Possible rectangle dimensions:")
        for width in range(1, n + 1):
            for height in range(1, n + 1):
                positions = (n - width + 1) * (n - height + 1)
                print(f"  {width}×{height}: {positions} positions")

# Test formulas against brute force for small boards
print("Verifying formulas against brute force counting:\n")
print("Board Size | Squares (Formula) | Squares (Brute) | Match")
print("-" * 60)

for size in range(1, 6):
    formula_squares = count_squares_formula(size)
    brute_squares = count_squares_brute_force(size)
    match = "✓" if formula_squares == brute_squares else "✗"
    print(f"{size}×{size}       | {formula_squares:17} | {brute_squares:15} | {match}")

print("\nBoard Size | Rectangles (Formula) | Rectangles (Brute) | Match")
print("-" * 70)

for size in range(1, 6):
    formula_rects = count_rectangles_formula(size)
    brute_rects = count_rectangles_brute_force(size)
    match = "✓" if formula_rects == brute_rects else "✗"
    print(f"{size}×{size}       | {formula_rects:20} | {brute_rects:18} | {match}")

# Show example for 3×3
visualize_small_board(3)

# Calculate for standard 8×8 chessboard
print("\n" + "=" * 60)
print("STANDARD 8×8 CHESSBOARD RESULTS:")
print("=" * 60)

n = 8
total_squares = count_squares_formula(n)
total_rectangles = count_rectangles_formula(n)

print(f"\nSquares on an 8×8 board:")
print(f"  Breakdown by size:")
for size in range(1, n + 1):
    count_for_size = (n - size + 1) ** 2
    print(f"    {size}×{size}: {count_for_size}")
print(f"  Total squares: {total_squares}")

print(f"\nRectangles on an 8×8 board: {total_rectangles}")
print(f"\nNote: This includes all {total_squares} squares (which are special rectangles)")
print(f"Non-square rectangles: {total_rectangles - total_squares}")
