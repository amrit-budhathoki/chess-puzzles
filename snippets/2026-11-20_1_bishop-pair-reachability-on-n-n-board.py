# Title: Bishop Pair Reachability on N×N Board

# Puzzle: Given an N×N chessboard, count how many pairs of bishops can be placed
# such that they can reach each other (same color square, connected via moves).
# Bishops move diagonally, so two bishops on the same color reach each other if
# their diagonals intersect or touch via a continuous path.
# Solution: Use BFS/DFS to find connected components of same-color squares,
# then count pairs within each component. Verify formula against brute force.

def get_square_color(r, c):
    """Return 'light' or 'dark' based on square color."""
    return 'light' if (r + c) % 2 == 0 else 'dark'

def bishop_reachability_brute_force(n):
    """Brute force: try all pairs, check if reachable via BFS."""
    def can_reach(r1, c1, r2, c2):
        """Check if bishop at (r1, c1) can reach (r2, c2)."""
        if get_square_color(r1, c1) != get_square_color(r2, c2):
            return False
        if r1 == r2 and c1 == c2:
            return False
        
        visited = set()
        queue = [(r1, c1)]
        visited.add((r1, c1))
        
        while queue:
            r, c = queue.pop(0)
            if r == r2 and c == c2:
                return True
            
            # Four diagonal directions
            for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                nr, nc = r + dr, c + dc
                while 0 <= nr < n and 0 <= nc < n:
                    if (nr, nc) not in visited:
                        visited.add((nr, nc))
                        queue.append((nr, nc))
                    nr += dr
                    nc += dc
        
        return False
    
    count = 0
    for r1 in range(n):
        for c1 in range(n):
            for r2 in range(r1, n):
                for c2 in range(n):
                    if (r1, c1) < (r2, c2) and can_reach(r1, c1, r2, c2):
                        count += 1
    return count

def bishop_reachability_component(n):
    """Find connected components of same-color squares, count pairs."""
    visited = [[False] * n for _ in range(n)]
    components = []
    
    for start_r in range(n):
        for start_c in range(n):
            if visited[start_r][start_c]:
                continue
            
            color = get_square_color(start_r, start_c)
            component = []
            queue = [(start_r, start_c)]
            visited[start_r][start_c] = True
            
            while queue:
                r, c = queue.pop(0)
                component.append((r, c))
                
                for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                    nr, nc = r + dr, c + dc
                    while 0 <= nr < n and 0 <= nc < n:
                        if not visited[nr][nc] and get_square_color(nr, nc) == color:
                            visited[nr][nc] = True
                            queue.append((nr, nc))
                        nr += dr
                        nc += dc
            
            components.append(component)
    
    total_pairs = 0
    for component in components:
        size = len(component)
        pairs = size * (size - 1) // 2
        total_pairs += pairs
    
    return total_pairs, components

def main():
    print("Bishop Pair Reachability Analysis\n")
    
    for n in range(2, 7):
        brute = bishop_reachability_brute_force(n)
        component_count, comps = bishop_reachability_component(n)
        
        print(f"N = {n}:")
        print(f"  Brute force: {brute}")
        print(f"  Component method: {component_count}")
        print(f"  Match: {brute == component_count}")
        
        light_count = (n * n + 1) // 2 if n % 2 == 1 else n * n // 2
        dark_count = n * n - light_count
        
        print(f"  Light squares: {light_count}, Dark squares: {dark_count}")
        print()

if __name__ == "__main__":
    main()
