# Title: Elo Rating Change Calculator

# This program implements the standard FIDE Elo rating system formula.
# Given two players' ratings and match result, it calculates the new ratings.
# The formula: New Rating = Old Rating + K * (Actual Score - Expected Score)
# We verify the formula against brute-force calculation for consistency.

def calculate_elo_change(rating1, rating2, result1, k_factor=32):
    """
    Calculate Elo rating changes after a game.
    rating1, rating2: current ratings
    result1: 1.0 (win), 0.5 (draw), 0.0 (loss) for player 1
    result2: opposite of result1
    Returns: (new_rating1, new_rating2)
    """
    result2 = 1.0 - result1
    
    # Expected score formula: E = 1 / (1 + 10^((opponent_rating - your_rating) / 400))
    expected1 = 1.0 / (1.0 + 10.0 ** ((rating2 - rating1) / 400.0))
    expected2 = 1.0 / (1.0 + 10.0 ** ((rating1 - rating2) / 400.0))
    
    # New rating = old rating + K * (actual - expected)
    new_rating1 = rating1 + k_factor * (result1 - expected1)
    new_rating2 = rating2 + k_factor * (result2 - expected2)
    
    return new_rating1, new_rating2

def verify_against_brute_force(rating1, rating2, result1):
    """Verify formula by manual calculation step-by-step."""
    k = 32
    r_diff = rating2 - rating1
    exponent = r_diff / 400.0
    power = 10.0 ** exponent
    expected1 = 1.0 / (1.0 + power)
    expected2 = 1.0 - expected1
    
    new_r1 = rating1 + k * (result1 - expected1)
    new_r2 = rating2 + k * ((1.0 - result1) - expected2)
    
    return new_r1, new_r2

# Test cases
test_cases = [
    (1600, 1400, 1.0),   # Higher rated player wins
    (1600, 1400, 0.5),   # Draw
    (1600, 1400, 0.0),   # Lower rated player wins (upset)
    (2000, 2000, 1.0),   # Equal rating, player 1 wins
    (1200, 1800, 0.5),   # Large rating difference, draw
]

print("Elo Rating Change Calculator")
print("=" * 70)
print(f"{'Player 1':<12} {'Player 2':<12} {'Result':<10} {'New Rating 1':<14} {'New Rating 2':<14}")
print("-" * 70)

for r1, r2, result in test_cases:
    new_r1, new_r2 = calculate_elo_change(r1, r2, result, k_factor=32)
    verify_r1, verify_r2 = verify_against_brute_force(r1, r2, result)
    
    # Check consistency
    assert abs(new_r1 - verify_r1) < 0.001, "Verification mismatch!"
    assert abs(new_r2 - verify_r2) < 0.001, "Verification mismatch!"
    
    result_str = "Win" if result == 1.0 else ("Draw" if result == 0.5 else "Loss")
    change1 = new_r1 - r1
    change2 = new_r2 - r2
    
    print(f"{r1:<12.0f} {r2:<12.0f} {result_str:<10} {new_r1:<14.1f} {new_r2:<14.1f}")
    print(f"{'Change:':<12} {'':<12} {'':<10} {change1:<+14.1f} {change2:<+14.1f}")
    print()

print("=" * 70)
print("Formula verified: New Rating = Old Rating + K × (Actual - Expected)")
print("Expected Score = 1 / (1 + 10^((opponent - you) / 400))")
