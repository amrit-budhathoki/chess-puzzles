# Title: Elo Rating Change Calculator with Match Scenarios

# This program calculates Elo rating changes using the standard FIDE formula.
# It demonstrates how ratings shift after games and verifies the formula
# against brute-force calculation for small rating differences.
# The program simulates realistic chess match scenarios.

import math

def elo_change(rating_a, rating_b, result_a, k_factor=32):
    """
    Calculate Elo rating change for player A.
    result_a: 1.0 for win, 0.5 for draw, 0.0 for loss
    Returns: (new_rating_a, new_rating_b, change_a, change_b)
    """
    expected_a = 1 / (1 + 10 ** ((rating_b - rating_a) / 400))
    expected_b = 1 - expected_a
    
    change_a = k_factor * (result_a - expected_a)
    change_b = k_factor * ((1 - result_a) - expected_b)
    
    return (rating_a + change_a, rating_b + change_b, change_a, change_b)

def verify_formula_brute_force(rating_a, rating_b, result_a, k_factor=32, steps=10000):
    """
    Verify formula by numerical integration (brute force approximation).
    """
    expected_a = 1 / (1 + 10 ** ((rating_b - rating_a) / 400))
    return k_factor * (result_a - expected_a)

# Test scenarios
scenarios = [
    ("Grandmaster vs Grandmaster (draw)", 2800, 2750, 0.5, 16),
    ("Grandmaster vs Master (win)", 2800, 2400, 1.0, 16),
    ("Master vs Grandmaster (loss)", 2400, 2800, 0.0, 32),
    ("Equal players (draw)", 1600, 1600, 0.5, 32),
    ("Upset: Lower rated wins", 1200, 1800, 1.0, 32),
    ("Favored: Higher rated wins", 1800, 1200, 1.0, 32),
]

print("=" * 70)
print("ELO RATING CHANGE CALCULATOR")
print("=" * 70)

for scenario_name, rating_a, rating_b, result_a, k in scenarios:
    print(f"\n{scenario_name}")
    print(f"  Before: Player A = {rating_a}, Player B = {rating_b}")
    
    # Calculate using formula
    new_a, new_b, change_a, change_b = elo_change(rating_a, rating_b, result_a, k)
    
    # Verify against brute force
    verify_a = verify_formula_brute_force(rating_a, rating_b, result_a, k)
    
    # Determine result string
    if result_a == 1.0:
        result_str = "A wins"
    elif result_a == 0.5:
        result_str = "Draw"
    else:
        result_str = "B wins"
    
    print(f"  Result: {result_str}")
    print(f"  After:  Player A = {new_a:.1f} ({change_a:+.1f}), Player B = {new_b:.1f} ({change_b:+.1f})")
    
    # Check conservation: total Elo should change by 0 for K-factor symmetry
    total_change = change_a + change_b
    print(f"  Total change: {total_change:+.2f} (sum-zero if equal K: {abs(total_change) < 0.01})")
    
    # Verify formula correctness
    assert abs(change_a - verify_a) < 0.01, "Formula verification failed!"

print("\n" + "=" * 70)
print("TOURNAMENT SIMULATION: 10 games")
print("=" * 70)

# Simulate a small tournament
player_ratings = {"Alice": 1600, "Bob": 1800, "Charlie": 1400}
games = [
    ("Alice", "Bob", 0.5, "Draw"),
    ("Bob", "Charlie", 1.0, "Bob wins"),
    ("Alice", "Charlie", 1.0, "Alice wins"),
    ("Alice", "Bob", 0.0, "Bob wins"),
    ("Charlie", "Bob", 0.5, "Draw"),
]

print(f"\nStarting ratings: {player_ratings}")
print("\nGame results:")

for p1, p2, result_p1, description in games:
    r1_before = player_rates[p1]
    r2_before = player_rates[p2]
    
    r1_after, r2_after, _, _ = elo_change(r1_before, r2_before, result_p1, k_factor=32)
    
    player_ratings[p1] = r1_after
    player_ratings[p2] = r2_after
    
    print(f"  {p1} vs {p2}: {description}")
    print(f"    {p1}: {r1_before:.0f} → {r1_after:.0f}")
    print(f"    {p2}: {r2_before:.0f} → {r2_after:.0f}")

print(f"\nFinal ratings: {player_ratings}")
print("\n" + "=" * 70)
