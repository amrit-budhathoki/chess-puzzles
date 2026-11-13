# Title: Wheat and Chessboard Problem with Exponential Growth Verification

# The wheat and chessboard problem: a king offers a reward of grains of wheat
# placed on a chessboard. On square 1, place 1 grain. On square 2, place 2 grains.
# On square 3, place 4 grains. Each square has double the previous amount.
# We compute the total using the closed-form formula 2^64 - 1, then verify
# against brute force summation for smaller boards to ensure correctness.

def wheat_and_chessboard(num_squares):
    """Calculate total grains using closed-form formula: 2^n - 1"""
    return (1 << num_squares) - 1

def wheat_and_chessboard_brute(num_squares):
    """Calculate total grains by summing grain counts per square"""
    total = 0
    for square in range(1, num_squares + 1):
        grains_on_square = 1 << (square - 1)  # 2^(square-1)
        total += grains_on_square
    return total

def visualize_board(num_squares, max_display=8):
    """Display exponential growth on first few squares"""
    print(f"\nFirst {min(num_squares, max_display)} squares of the chessboard:")
    print("Square | Grains on Square | Cumulative Total")
    print("-------|------------------|------------------")
    cumulative = 0
    for square in range(1, min(num_squares, max_display) + 1):
        grains = 1 << (square - 1)
        cumulative += grains
        print(f"  {square:2d}   | {grains:16,d} | {cumulative:18,d}")
    if num_squares > max_display:
        print(f"   ... ({num_squares - max_display} more squares)")

# Verification: test formula against brute force for small boards
print("=== Formula Verification ===")
for test_size in [4, 8, 16, 32]:
    formula_result = wheat_and_chessboard(test_size)
    brute_result = wheat_and_chessboard_brute(test_size)
    match = "✓" if formula_result == brute_result else "✗"
    print(f"Board size {test_size:2d}: {match} Formula={formula_result:,d}, Brute={brute_result:,d}")

# Solve for the full 8x8 chessboard (64 squares)
print("\n=== Full Chessboard (64 squares) ===")
num_squares = 64
total_grains = wheat_and_chessboard(num_squares)

visualize_board(num_squares, max_display=10)

print(f"\nTotal grains on 64-square chessboard:")
print(f"  {total_grains:,d}")
print(f"\nIn scientific notation: {total_grains:.3e}")

# Comparison with real-world quantities
print("\n=== Real-World Perspective ===")
grains_per_kg = 50_000
kg_total = total_grains / grains_per_kg
metric_tons = kg_total / 1000

print(f"Approximate weight: {metric_tons:.2e} metric tons")
print(f"Annual world wheat production (≈700M tons): {metric_tons / 700_000_000:.1f}x")
