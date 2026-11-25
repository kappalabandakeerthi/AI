import random
import math

def calculate_cost(board):
    n = len(board)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j]:
                conflicts += 1
            elif abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def simulated_annealing(n=8):
    current = [random.randrange(n) for _ in range(n)]
    current_cost = calculate_cost(current)
    temperature = 100.0
    cooling_rate = 0.99
    max_iterations = 100000

    print("Initial state:", [r + 1 for r in current])
    print("Initial cost:", current_cost)

    for iteration in range(max_iterations):
        if current_cost == 0:
            break

        # Generate a neighboring state
        neighbor = current.copy()
        col = random.randrange(n)
        row = random.randrange(n - 1)
        # Ensure the queen moves to a different row
        if row >= neighbor[col]:
            row += 1
        neighbor[col] = row

        neighbor_cost = calculate_cost(neighbor)
        delta = neighbor_cost - current_cost

        # Accept a better state or probabilistically accept a worse state
        if delta <= 0:
            current = neighbor
            current_cost = neighbor_cost
        elif random.random() < math.exp(-delta / temperature):
            current = neighbor
            current_cost = neighbor_cost

        # Cool the system (prevent division by zero at very high iterations)
        temperature = max(temperature * cooling_rate, 1e-10)

        if iteration % 1000 == 0:
            print(
                "Iteration:", iteration,
                "Cost:", current_cost,
                "Temperature:", round(temperature, 4)
            )

    print("\nFinal board:", [r + 1 for r in current])
    print("Final cost:", current_cost)

    if current_cost == 0:
        print("Solution found!")
    else:
        print("No solution found within the iteration limit.")

    return current

if __name__ == "__main__":
    simulated_annealing(8)
