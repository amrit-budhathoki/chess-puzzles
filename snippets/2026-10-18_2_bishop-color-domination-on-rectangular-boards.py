# Title: Bishop Color Domination on Rectangular Boards

# Puzzle: On an m×n chessboard, bishops can only reach squares of their own color.
# This program counts how many squares each color dominates (can reach or occupy)
# and finds which color has more control. For a standard 8×8 board, both colors
# dominate equally; for non-square boards the balance shifts. We verify the
# formula: light squares = ⌈(m×n)/2⌉, dark squares = ⌊(m×n)/2⌋, then simulate
# actual bishop reachability via BFS to confirm all same-color squares connect.

def bishop_reachability(m, n):
    """Count reachable squares from each color via BFS."""
    
    # Color assignment: (row + col) % 2
    def color(r, c):
        return (r + c) % 2
    
    # BFS from one square of each color
    def bfs_from(start_r, start_c):
        visited = set()
        queue = [(start_r, start_c)]
        visited.add((start_r, start_c))
        
        while queue:
            r, c = queue.pop(0)
            # Four diagonal directions
            for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                nr, nc = r + dr, c + dc
                while 0 <= nr < m and 0 <= nc < n:
                    if (nr, nc) not in visited:
                        visited.add((nr, nc))
                        queue.append((nr, nc))
                    nr += dr
                    nc += dc
        
        return visited
    
    # Find representatives of each color
    light_rep, dark_rep = None, None
    for r in range(m):
        for c in range(n):
            if color(r, c) == 0 and light_rep is None:
                light_rep = (r, c)
            if color(r, c) == 1 and dark_rep is None:
                dark_rep = (r, c)
    
    light_reach = bfs_from(*light_rep) if light_rep else set()
    dark_reach = bfs_from(*dark_rep) if dark_rep else set()
    
    return len(light_reach), len(dark_reach)

def count_squares_by_color(m, n):
    """Formula: light squares = ⌈(m×n)/2⌉, dark = ⌊(m×n)/2⌋."""
    total = m * n
    light = (total + 1) // 2
    dark = total // 2
    return light, dark

# Test cases
test_boards = [(8, 8), (5, 5), (4, 6), (3, 7), (2, 3)]

print("Bishop Color Domination Analysis")
print("=" * 60)

for m, n in test_boards:
    formula_light, formula_dark = count_squares_by_color(m, n)
    reach_light, reach_dark = bishop_reachability(m, n)
    
    print(f"\nBoard: {m}×{n}")
    print(f"  Formula (light, dark): {formula_light}, {formula_dark}")
    print(f"  Reachable (light, dark): {reach_light}, {reach_dark}")
    
    # Verify formula matches reachability
    assert formula_light == reach_light and formula_dark == reach_dark, \
        f"Mismatch on {m}×{n}!"
    
    if reach_light > reach_dark:
        print(f"  → Light color dominates by {reach_light - reach_dark} squares")
    elif reach_dark > reach_light:
        print(f"  → Dark color dominates by {reach_dark - reach_light} squares")
    else:
        print(f"  → Colors are balanced")

print("\n" + "=" * 60)
print("✓ All tests passed: formula verified against reachability simulation")
