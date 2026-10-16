# Title: N-Queens Problem with Backtracking

# The N-Queens problem asks: place N queens on an N×N chessboard such that
# no two queens attack each other (same row, column, or diagonal).
# Solution uses backtracking: try placing queens row by row, and retreat
# when a conflict is detected. We verify the formula for small N against brute force.

def is_safe(board, row, col):
    """Check if placing a queen at (row, col) is safe."""
    # Check column
    for i in range(row):
        if board[i] == col:
            return False
    # Check diagonals
    for i in range(row):
        if abs(board[i] - col) == abs(i - row):
            return False
    return True

def solve_n_queens(n, row=0, board=None, solutions=None):
    """Backtracking solver for N-Queens. board[i] = column of queen in row i."""
    if board is None:
        board = [-1] * n
        solutions = []
    
    if row == n:
        solutions.append(board[:])
        return solutions
    
    for col in range(n):
        if is_safe(board, row, col):
            board[row] = col
            solve_n_queens(n, row + 1, board, solutions)
            board[row] = -1
    
    return solutions

def draw_board(solution):
    """Draw a single N-Queens solution on a chessboard."""
    n = len(solution)
    for row in range(n):
        line = ""
        for col in range(n):
            if solution[row] == col:
                line += "♛ "
            else:
                line += ". "
        print(line)
    print()

def count_solutions_brute_force(n):
    """Brute force verification: generate all permutations and count valid ones."""
    from itertools import permutations
    count = 0
    for perm in permutations(range(n)):
        valid = True
        for i in range(n):
            for j in range(i + 1, n):
                if abs(perm[i] - perm[j]) == abs(i - j):
                    valid = False
                    break
            if not valid:
                break
        if valid:
            count += 1
    return count

# Known formula results (OEIS A000170)
known_solutions = {1: 1, 2: 0, 3: 0, 4: 2, 5: 10, 6: 4, 7: 40, 8: 92}

print("N-Queens Problem: Backtracking Solution\n")
print("Verifying backtracking against brute force for small N:\n")

for n in range(1, 9):
    solutions = solve_n_queens(n)
    count = len(solutions)
    brute_count = count_solutions_brute_force(n)
    
    match = "✓" if count == brute_count else "✗"
    expected = known_solutions.get(n, "?")
    
    print(f"N={n}: Backtracking={count}, Brute Force={brute_count}, "
          f"Expected={expected} {match}")

print("\n" + "="*40)
print("First solution for N=8:\n")
solutions_8 = solve_n_queens(8)
draw_board(solutions_8[0])

print(f"Total solutions for N=8: {len(solutions_8)}")
print(f"\nSecond solution for N=8:\n")
draw_board(solutions_8[1])
