# Title: Blitz Tournament Round-Robin Elo Calculator

# Given a round-robin tournament result (all players play each other once),
# calculate final Elo ratings using the standard FIDE formula.
# We verify the formula by brute-force recalculation and check that total
# rating points are conserved (zero-sum property).

def elo_delta(rating_a, rating_b, result_a, k_factor=32):
    """
    Calculate Elo change for player A.
    result_a: 1.0 = win, 0.5 = draw, 0.0 = loss
    Formula: delta = K * (result - expected)
    expected = 1 / (1 + 10^((rating_b - rating_a) / 400))
    """
    expected = 1.0 / (1.0 + 10.0 ** ((rating_b - rating_a) / 400.0))
    delta = k_factor * (result_a - expected)
    return delta

def calculate_tournament_elos(initial_ratings, results, k_factor=32):
    """
    results[i][j] = score from player i vs player j
    For each pair, results[i][j] + results[j][i] should equal 1.0
    """
    n = len(initial_ratings)
    new_ratings = initial_ratings[:]
    total_delta = 0.0
    
    for i in range(n):
        for j in range(n):
            if i != j:
                delta = elo_delta(
                    initial_ratings[i],
                    initial_ratings[j],
                    results[i][j],
                    k_factor
                )
                new_ratings[i] += delta
                total_delta += delta
    
    return new_ratings, total_delta

# Test case: 4 players, some known results
players = ["Alice", "Bob", "Charlie", "Diana"]
initial = [1600, 1500, 1400, 1300]

# Results matrix: [i][j] = score for player i vs j
# Match: Alice vs Bob -> Alice wins (1.0 for Alice, 0.0 for Bob)
# Match: Alice vs Charlie -> Draw (0.5 each)
# Match: Alice vs Diana -> Diana wins (0.0 for Alice, 1.0 for Diana)
# Match: Bob vs Charlie -> Bob wins
# Match: Bob vs Diana -> Draw
# Match: Charlie vs Diana -> Draw

results = [
    [0.0, 1.0, 0.5, 0.0],  # Alice: beat Bob, drew Charlie, lost Diana
    [0.0, 0.0, 1.0, 0.5],  # Bob: lost Alice, beat Charlie, drew Diana
    [0.5, 0.0, 0.0, 0.5],  # Charlie: drew Alice, lost Bob, drew Diana
    [1.0, 0.5, 0.5, 0.0],  # Diana: beat Alice, drew Bob, drew Charlie
]

final_ratings, total_delta = calculate_tournament_elos(initial, results, k_factor=32)

print("=" * 60)
print("ROUND-ROBIN TOURNAMENT ELO CALCULATION")
print("=" * 60)
print(f"\n{'Player':<12} {'Initial Elo':<15} {'Final Elo':<15} {'Change':<10}")
print("-" * 60)

for i, name in enumerate(players):
    delta = final_ratings[i] - initial[i]
    print(f"{name:<12} {initial[i]:<15.1f} {final_ratings[i]:<15.1f} {delta:+.1f}")

print("-" * 60)
print(f"Total Elo change (should be ~0): {total_delta:+.2f}")

# Verification: manually recalculate for Alice vs Bob
print("\n" + "=" * 60)
print("VERIFICATION: Manual calculation for Alice vs Bob match")
print("=" * 60)
expected_alice = 1.0 / (1.0 + 10.0 ** ((1500 - 1600) / 400.0))
delta_alice = 32 * (1.0 - expected_alice)
delta_bob = 32 * (0.0 - (1.0 - expected_alice))

print(f"Alice initial: 1600, Bob initial: 1500")
print(f"Expected win % for Alice: {expected_alice:.4f}")
print(f"Alice delta: {delta_alice:+.2f} → {1600 + delta_alice:.1f}")
print(f"Bob delta: {delta_bob:+.2f} → {1500 + delta_bob:.1f}")
print(f"Sum of deltas: {delta_alice + delta_bob:.2f} (zero-sum check)")
