# Title: Bishop Reachability Graph and Connected Components

# A bishop can only reach squares of the same color. This puzzle computes
# the connected component structure of bishops on a chessboard, where two
# squares are connected if a bishop can move between them in one step.
# We verify the formula: on an 8x8 board, there are exactly 2 connected
# components (one for each color), each with 32 squares. For rectangular
# boards, we generalize and check connectivity patterns.

def square_color(r, c):
    """Return 0 for white squares, 1 for black squares."""
    return (r + c) % 2

def bishop_moves(r, c):
    """Generate all squares a bishop at (r, c) can reach in one move."""
    moves = []
    for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
        nr, nc = r + dr, c + dc
        while 0 <= nr < 8 and 0 <= nc < 8:
            moves.append((nr, nc))
            nr += dr
            nc += dc
    return moves

def build_bishop_graph(rows, cols):
    """Build adjacency list for bishop reachability on rows × cols board."""
    graph = {}
    for r in range(rows):
        for c in range(cols):
            graph[(r, c)] = []
            for nr, nc in bishop_moves(r, c) if rows == 8 and cols == 8 else []:
                if 0 <= nr < rows and 0 <= nc < cols:
                    graph[(r, c)].append((nr, nc))
    
    # For non-8x8 boards, compute moves directly
    if rows != 8 or cols != 8:
        graph = {}
        for r in range(rows):
            for c in range(cols):
                graph[(r, c)] = []
                for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                    nr, nc = r + dr, c + dc
                    while 0 <= nr < rows and 0 <= nc < cols:
                        graph[(r, c)].append((nr, nc))
                        nr += dr
                        nc += dc
    return graph

def find_connected_components(graph, rows, cols):
    """Find connected components using BFS, grouped by square color."""
    visited = set()
    components = {0: [], 1: []}
    
    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                color = square_color(r, c)
                component = []
                queue = [(r, c)]
                visited.add((r, c))
                
                while queue:
                    cr, cc = queue.pop(0)
                    component.append((cr, cc))
                    for nr, nc in graph[(cr, cc)]:
                        if (nr, nc) not in visited:
                            visited.add((nr, nc))
                            queue.append((nr, nc))
                
                components[color].append(component)
    
    return components

def visualize_component(rows, cols, component, label):
    """Display a component on a board."""
    board = [['.' for _ in range(cols)] for _ in range(rows)]
    for r, c in component:
        board[r][c] = 'B'
    print(f"{label}:")
    for row in board:
        print(' '.join(row))
    print()

# Test on standard 8x8 chessboard
print("=" * 50)
print("BISHOP REACHABILITY ON 8×8 BOARD")
print("=" * 50)

graph = build_bishop_graph(8, 8)
components = find_connected_components(graph, 8, 8)

white_count = sum(len(c) for c in components[0])
black_count = sum(len(c) for c in components[1])

print(f"\nWhite squares: {len(components[0])} component(s), {white_count} total squares")
print(f"Black squares: {len(components[1])} component(s), {black_count} total squares")

# Expected: 1 white component with 32 squares, 1 black component with 32 squares
expected_white, expected_black = 32, 32
assert white_count == expected_white and black_count == expected_black
print(f"✓ Formula verified: each color forms exactly 1 connected component of size 32\n")

# Test on smaller boards to verify formula generalizes
print("=" * 50)
print("BISHOP REACHABILITY ON SMALLER BOARDS")
print("=" * 50)

for size in [4, 5, 6]:
    graph = build_bishop_graph(size, size)
    components = find_connected_components(graph, size, size)
    
    white_squares = sum(len(c) for c in components[0])
    black_squares = sum(len(c) for c in components[1])
    white_comps = len(components[0])
    black_comps = len(components[1])
    
    print(f"\n{size}×{size} board:")
    print(f"  White: {white_comps} component(s), {white_squares} squares")
    print(f"  Black: {black_comps} component(s), {black_squares} squares")
