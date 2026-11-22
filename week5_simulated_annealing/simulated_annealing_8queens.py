import random
import math

N = 8
TEMPERATURE = 10.0
ALPHA = 0.99
MAX_RESTARTS = 20


def calculate_cost(board):
    conflicts = 0

    for i in range(N):
        for j in range(i + 1, N):

            if board[i] == board[j]:
                conflicts += 1

            elif abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1

    return conflicts


def simulated_annealing(board):

    current_cost = calculate_cost(board)
    temperature = TEMPERATURE

    print("Board:", board, "Cost:", current_cost)

    while temperature > 0.001 and current_cost != 0:

        column = random.randint(0, N - 1)

        new_row = random.randint(0, N - 1)

        while new_row == board[column]:
            new_row = random.randint(0, N - 1)

        next_board = board.copy()
        next_board[column] = new_row

        next_cost = calculate_cost(next_board)

        delta_E = current_cost - next_cost

        if delta_E > 0:
            board = next_board
            current_cost = next_cost

            print("Board:", board, "Cost:", current_cost)

        else:
            probability = math.exp(delta_E / temperature)

            if random.random() < probability:
                board = next_board
                current_cost = next_cost

                print("Board:", board, "Cost:", current_cost)

        temperature = temperature * ALPHA

    return board, current_cost


# User input
board = list(map(int, input("Enter initial board: ").split()))

if len(board) != 8:
    print("Please enter exactly 8 values.")

elif any(row < 0 or row > 7 for row in board):
    print("Each value must be between 0 and 7.")

else:

    initial_cost = calculate_cost(board)

    print("\nInitial Board:", board)
    print("Initial Cost:", initial_cost)
    print("\nIntermediate Steps:")

    best_board = board.copy()
    best_cost = initial_cost

    for restart in range(1, MAX_RESTARTS + 1):

        solution, cost = simulated_annealing(board.copy())

        if cost < best_cost:
            best_board = solution.copy()
            best_cost = cost

        if cost == 0:
            break

    print("\nFinal Board:", best_board)
    print("Final Cost:", best_cost)

    if best_cost == 0:
        print("Solution Found!")
    else:
        print("No solution found.")
