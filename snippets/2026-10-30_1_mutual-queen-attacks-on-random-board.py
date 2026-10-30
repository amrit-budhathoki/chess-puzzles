# Title: Mutual Queen Attacks on Random Board

# Puzzle: Place N queens randomly on an NxN board and count how many pairs of queens attack each other.
# Solution: For each pair of queens, check if they share a row, column, or diagonal.
# We verify the formula against brute force for small boards to ensure correctness.

import random
from itertools import combinations

def queens_attack(q1, q2):
    """Check if two queens at positions (r1,c1) and (r2,c2) attack each other."""
    r1, c1 = q1
    r2, c2 = q2
    # Same row or column
    if r1 == r2 or c1 == c2:
        return True
    # Same diagonal (difference in rows equals difference in columns)
    if abs(r1 - r2) == abs(c1 - c2):
        return True
    return False

def count_attacking_pairs_brute_force(positions):
    """Count attacking pairs by checking all combinations."""
    count = 0
    for q1, q2 in combinations(positions, 2):
        if queens_attack(q1, q2):
            count += 1
    return count

def draw_board(n, queens):
    """Draw the board with queens marked as Q."""
    board = [['.' for _ in range(n)] for _ in range(n)]
    for r, c in queens:
        board[r][c] = 'Q'
    for row in board:
        print(' '.join(row))
    print()

def test_random_placement(n, num_trials=10):
    """Test random queen placements and verify attack counting."""
    print(f"Testing {n}x{n} board with {num_trials} random placements:")
    print("-" * 50)
    
    for trial in range(num_trials):
        # Generate random positions: one queen per row, different columns
        positions = [(i, random.randint(0, n-1)) for i in range(n)]
        
        # Count attacks
        attacks = count_attacking_pairs_brute_force(positions)
        
        print(f"Trial {trial + 1}: {attacks} attacking pairs")
        
        if n <= 6:
            draw_board(n, positions)
    
    print()

def verify_small_boards():
    """Verify correctness on small boards by comparing all possibilities."""
    print("Verification on small boards:")
    print("-" * 50)
    
    for n in range(2, 5):
        # Generate all possible placements (one queen per row)
        def generate_all_placements(n, row=0, current=[]):
            if row == n:
                yield current[:]
            else:
                for col in range(n):
                    current.append((row, col))
                    yield from generate_all_placements(n, row + 1, current)
                    current.pop()
        
        placements = list(generate_all_placements(n))
        attack_counts = [count_attacking_pairs_brute_force(p) for p in placements]
        
        avg_attacks = sum(attack_counts) / len(attack_counts) if attack_counts else 0
        max_attacks = max(attack_counts) if attack_counts else 0
        
        print(f"{n}x{n} board: {len(placements)} placements, "
              f"avg attacks: {avg_attacks:.2f}, max: {max_attacks}")
    
    print()

if __name__ == "__main__":
    random.seed(42)
    
    verify_small_boards()
    test_random_placement(5, num_trials=5)
    test_random_placement(8, num_trials=3)
