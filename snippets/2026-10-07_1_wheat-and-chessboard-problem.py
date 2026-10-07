# Title: Wheat and Chessboard Problem

# The legendary problem: place 1 grain on square 1, 2 on square 2, 4 on square 3, etc.
# (doubling each square). How many grains total on a standard 8x8 board?
# Formula: sum of 2^(n-1) for n=1 to 64 = 2^64 - 1
# We verify the formula matches brute force calculation.

def wheat_and_chessboard(num_squares):
    """Calculate total grains using the doubling pattern."""
    # Brute force: sum each square individually
    total_brute = sum(2**i for i in range(num_squares))
    
    # Formula: geometric series sum = 2^n - 1
    total_formula = 2**num_squares - 1
    
    return total_brute, total_formula

def format_large_number(n):
    """Format large number with commas for readability."""
    return f"{n:,}"

def visualize_board():
    """Show first few and last few squares with grain counts."""
    print("\n8x8 Chess Board - Grain Distribution (first 4 and last 4 squares):")
    print("-" * 60)
    
    # Show first 4 squares
    for sq in range(1, 5):
        grains = 2**(sq - 1)
        print(f"Square {sq:2d}: {format_large_number(grains):>20} grains")
    
    print("    ... (56 more squares) ...")
    
    # Show last 4 squares
    for sq in range(61, 65):
        grains = 2**(sq - 1)
        print(f"Square {sq:2d}: {format_large_number(grains):>20} grains")

def main():
    print("=" * 60)
    print("THE WHEAT AND CHESSBOARD PROBLEM")
    print("=" * 60)
    
    # Verify formula with small cases
    print("\nVerification (small cases):")
    for n in [1, 2, 3, 4, 8]:
        brute, formula = wheat_and_chessboard(n)
        match = "✓" if brute == formula else "✗"
        print(f"  {n} squares: brute={brute:,} vs formula={formula:,} {match}")
    
    # Full 64-square problem
    print("\n" + "=" * 60)
    print("FULL 64-SQUARE BOARD:")
    print("=" * 60)
    
    brute, formula = wheat_and_chessboard(64)
    
    visualize_board()
    
    print("\n" + "-" * 60)
    print(f"Total grains on standard 8×8 board:")
    print(f"  {format_large_number(formula)}")
    print("-" * 60)
    
    # Some perspective
    print("\nPerspective:")
    print(f"  Scientific notation: {formula:.3e}")
    
    # Approximate grain mass (assume ~65mg per grain)
    grain_mass_mg = 65
    total_mass_kg = (formula * grain_mass_mg) / 1_000_000
    print(f"  Approximate mass (at 65mg/grain): {total_mass_kg:,.0f} kg")
    print(f"  That's about {total_mass_kg / 1_000_000:,.1f} million metric tons")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
