# Title: Wheat and Chessboard Problem with Exponential Verification

# The wheat and chessboard problem: if you place 1 grain of wheat on square 1,
# 2 grains on square 2, 4 on square 3, and so on (doubling each square),
# how much wheat is on the board after 64 squares?
# Solution: use the geometric series formula 2^64 - 1, then verify against brute force.

def brute_force_total(num_squares):
    """Calculate total grains by summing each square."""
    total = 0
    for square in range(1, num_squares + 1):
        grains = 2 ** (square - 1)
        total += grains
    return total

def formula_total(num_squares):
    """Calculate total using geometric series formula: 2^n - 1."""
    return 2 ** num_squares - 1

def verify_formula(max_squares=20):
    """Verify formula matches brute force for small values."""
    print("Verification: Formula vs Brute Force")
    print("-" * 50)
    for n in [1, 2, 4, 8, 10, 16, 20]:
        if n <= max_squares:
            brute = brute_force_total(n)
            formula = formula_total(n)
            match = "✓" if brute == formula else "✗"
            print(f"Squares: {n:2d} | Formula: {formula:20d} | {match}")
    print()

def display_board_sample():
    """Show the exponential growth on a chessboard (first 8 squares)."""
    print("Chessboard visualization (first 8 squares):")
    print("-" * 60)
    total = 0
    for row in range(1, 3):
        for col in range(1, 5):
            square = (row - 1) * 4 + col
            grains = 2 ** (square - 1)
            total += grains
            print(f"[{grains:>10d}]", end=" ")
        print()
    print(f"\nTotal after 8 squares: {total}")
    print()

def main():
    num_squares = 64
    
    verify_formula(20)
    display_board_sample()
    
    # Calculate for full chessboard
    result = formula_total(num_squares)
    
    print(f"Full Chessboard ({num_squares} squares):")
    print("-" * 60)
    print(f"Total grains of wheat: {result}")
    print(f"Scientific notation: {result:.3e}")
    print(f"Number of digits: {len(str(result))}")
    print()
    
    # Some perspective
    grain_weight_mg = 50  # approximate weight of wheat grain
    total_weight_kg = (result * grain_weight_mg) / 1_000_000
    
    print("Perspective:")
    print(f"If each grain weighs ~{grain_weight_mg}mg:")
    print(f"Total weight: {total_weight_kg:.2e} kg")
    print(f"              {total_weight_kg / 1_000_000_000:.0f} billion metric tons")

if __name__ == "__main__":
    main()
