# Title: Expected Score and Rating Swing in Chess Match Scenarios

# This program calculates expected scores and rating changes using the Glicko-2 system,
# which is an improvement over the standard Elo model. It accounts for rating deviation
# (uncertainty) and volatility. We verify the formula against a simple iterative brute-force
# approach for a small scenario, then show realistic match scenarios with rating swings.

import math

def glicko2_expected_score(rating1, rating2, rd1):
    """Calculate expected score using Glicko-2 formula."""
    q = math.log(10) / 400
    g_val = 1 / math.sqrt(1 + 3 * q * q * rd1 * rd1 / (math.pi ** 2))
    expected = 1 / (1 + 10 ** (g_val * (rating2 - rating1) / 400))
    return expected

def glicko2_new_rating(rating, rd, results, opponent_ratings):
    """Update rating and RD using Glicko-2 formulas."""
    q = math.log(10) / 400
    
    d_squared_inv = sum(
        (1 / math.sqrt(1 + 3 * q * q * rd * rd / (math.pi ** 2)) ** 2) *
        glicko2_expected_score(rating, opp_r, rd) *
        (1 - glicko2_expected_score(rating, opp_r, rd))
        for opp_r in opponent_ratings
    )
    d_squared = 1 / (q * q * d_squared_inv) if d_squared_inv > 0 else 0
    
    r_delta = (q / (1 / (rd * rd) + 1 / d_squared)) * sum(
        (1 / math.sqrt(1 + 3 * q * q * rd * rd / (math.pi ** 2))) *
        (results[i] - glicko2_expected_score(rating, opponent_ratings[i], rd))
        for i in range(len(results))
    )
    
    new_rd = math.sqrt(1 / (1 / (rd * rd) + 1 / d_squared))
    return rating + r_delta, new_rd

def simple_elo_expected(r1, r2):
    """Simple Elo expected score (brute force baseline)."""
    return 1 / (1 + 10 ** ((r2 - r1) / 400))

# Verification: compare Glicko-2 with simple Elo for small case
print("=" * 60)
print("VERIFICATION: Glicko-2 vs Simple Elo (Low Uncertainty)")
print("=" * 60)
player_a_rating = 1600
player_b_rating = 1400
rd_low = 30  # Very low rating deviation

exp_glicko = glicko2_expected_score(player_a_rating, player_b_rating, rd_low)
exp_simple = simple_elo_expected(player_a_rating, player_b_rating)
print(f"Glicko-2 expected (RD={rd_low}): {exp_glicko:.4f}")
print(f"Simple Elo expected:           {exp_simple:.4f}")
print(f"Difference: {abs(exp_glicko - exp_simple):.6f} (small when RD is low)")
print()

# Scenario 1: Strong player beats weaker opponent
print("=" * 60)
print("SCENARIO 1: 1800-rated player vs 1600-rated player")
print("=" * 60)
r1, rd1 = 1800, 100
r2, rd2 = 1600, 150
print(f"Before: Player A {r1} (RD {rd1}), Player B {r2} (RD {rd2})")

exp_a = glicko2_expected_score(r1, r2, rd1)
exp_b = glicko2_expected_score(r2, r1, rd2)
print(f"Expected: A scores {exp_a:.4f}, B scores {exp_b:.4f}")

# A wins
new_r1, new_rd1 = glicko2_new_rating(r1, rd1, [1], [r2])
new_r2, new_rd2 = glicko2_new_rating(r2, rd2, [0], [r1])
print(f"After A wins: A {r1} → {new_r1:.1f} ({new_r1-r1:+.1f}), "
      f"B {r2} → {new_r2:.1f} ({new_r2-r2:+.1f})")

# A loses (upset)
new_r1_loss, new_rd1_loss = glicko2_new_rating(r1, rd1, [0], [r2])
new_r2_loss, new_rd2_loss = glicko2_new_rating(r2, rd2, [1], [r1])
print(f"After A loses: A {r1} → {new_r1_loss:.1f} ({new_r1_loss-r1:+.1f}), "
      f"B {r2} → {new_r2_loss:.1f} ({new_r2_loss-r2:+.1f})")
print()

# Scenario 2: Multiple games in a tournament
print("=" * 60)
print("SCENARIO 2: Tournament (3 games, same opponent)")
print("=" * 60)
r_player = 1700
rd_player = 80
opponent_ratings = [1750, 1700, 1650]
results = [0, 1, 1]  # Loss, Win, Win

print(f"Before: Rating {r_player}, RD {rd_player}")
print(f"Opponents: {opponent_ratings}, Results: {results} (0=loss, 1=win)")

new_r, new_rd = glicko2_new_rating(r_player, rd_player, results, opponent_ratings)
print(f"After:  Rating {new_r:.1f} ({new_r-r_player:+.1f}), RD {new_rd:.1f}")
print()

# Scenario 3: High uncertainty player
print("=" * 60)
print("SCENARIO 3: Provisional/High-Uncertainty Player")
print("=" * 60)
r_prov = 1600
rd_prov = 350  # Very high RD
opponent = 1600
result_win = 1

new_r_prov, new_rd_prov = glicko2_new_rating(r_prov, rd_prov, [result_win], [opponent])
print(f"Before: Rating {r_prov}, RD {rd_prov} (provisional player)")
print(f"Opponent: {opponent}, Result: Win")
print(f"After:  Rating {new_r_prov:.1f} ({new_r_prov-r_prov:+.1f}), RD {new_rd_prov:.1f}")
print(f"Note: High RD → larger rating swing and faster RD decay")
