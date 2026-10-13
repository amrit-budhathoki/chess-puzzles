# Title: Exponential Growth: Wheat and Chessboard Verification

# The wheat and chessboard problem: a king promises to give a reward of grains of wheat
# by doubling the amount on each successive square of a chessboard (1, 2, 4, 8, ...).
# We compute the total using the closed-form formula 2^64 - 1 and verify it against
# brute force summation for smaller boards to demonstrate the exponential nature.

def wheat_formula(num_squares):
    """Calculate total grains using closed-form formula: 2^n - 1"""
    return 2**num_squares - 1

def wheat_brute_force(num_squares):
    """Calculate total grains by summing individual squares: sum of 2^i for i in 0..n-1"""
    total = 0
    for i in range(num_squares):
        total += 2**i
    return total

def visualize_growth(num_squares):
    """Show exponential growth on first few squares"""
    print(f"Grains per square (first 10 squares):")
    total = 0
    for i in range(min(10, num_squares)):
        grains_on_square = 2**i
        total += grains_on_square
        print(f"  Square {i+1:2d}: {grains_on_square:>20,} grains (cumulative: {total:>25,})")
    if num_squares > 10:
        print(f"  ... ({num_squares - 10} more squares omitted)")

def verify_formula(test_size):
    """Verify formula against brute force for small board"""
    formula_result = wheat_formula(test_size)
    brute_result = wheat_brute_force(test_size)
    match = "✓" if formula_result == brute_result else "✗"
    print(f"Verification for {test_size}-square board: {match}")
    print(f"  Formula:     {formula_result:,}")
    print(f"  Brute force: {brute_result:,}")
    return formula_result == brute_result

# Main computation
print("=" * 70)
print("THE WHEAT AND CHESSBOARD PROBLEM")
print("=" * 70)
print()

# Verify on small boards
print("Step 1: Verify formula on small boards")
print("-" * 70)
for size in [4, 8, 16]:
    verify_formula(size)
    print()

# Show growth pattern
print("Step 2: Exponential growth visualization")
print("-" * 70)
visualize_growth(64)
print()

# Full chessboard result
print("Step 3: Full 64-square chessboard")
print("-" * 70)
total_grains = wheat_formula(64)
print(f"Total grains of wheat on 64-square chessboard:")
print(f"  {total_grains:,}")
print()

# Context and insight
print("Step 4: Putting it in perspective")
print("-" * 70)
grains_per_kg = 50000
kg_total = total_grains / grains_per_kg
metric_tons = kg_total / 1000
print(f"Estimated mass (at 50,000 grains per kg):")
print(f"  {kg_total:,.0f} kg")
print(f"  {metric_tons:,.0f} metric tons")
print()
print(f"Global wheat production (~2023): ~770 million metric tons/year")
ratio = metric_tons / 770_000_000
print(f"Chessboard wheat is {ratio:,.1f}x annual global production")
print()

print("=" * 70)
print("Key insight: 2^64 - 1 grows astronomically fast!")
print("=" * 70)
