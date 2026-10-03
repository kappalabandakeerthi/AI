def dls(state, goal, depth, path):
    if state == goal:
        return path
    if depth <= 0:
        return None

    blank = state.index(0)
    x, y = blank // 3, blank % 3
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            n_blank = nx * 3 + ny
            new_state = list(state)
            new_state[blank], new_state[n_blank] = new_state[n_blank], new_state[blank]
            
            if tuple(new_state) not in path:
                result = dls(tuple(new_state), goal, depth - 1, path + [tuple(new_state)])
                if result:
                    return result
    return None

def iterative_deepening_search(start, goal, max_depth):
    for depth in range(max_depth + 1):
        result = dls(tuple(start), tuple(goal), depth, [tuple(start)])
        if result:
            return result
    return None

def get_row_wise_input(prompt_name):
    print(f"\nEnter the {prompt_name} state row by row (use 0 for the blank space):")
    state = []
    for i in range(3):
        while True:
            try:
                row = list(map(int, input(f"Row {i+1} (3 numbers separated by spaces): ").split()))
                if len(row) == 3:
                    state.extend(row)
                    break
                else:
                    print("Please enter exactly 3 numbers.")
            except ValueError:
                print("Invalid input. Please enter numbers only.")
    return state

def main():
    print("--- 8-Puzzle Solver using IDS ---")
    try:
        max_depth = int(input("Enter the maximum depth limit: "))
    except ValueError:
        print("Invalid depth. Defaulting to 20.")
        max_depth = 20

    initial_state = get_row_wise_input("INITIAL")
    goal_state = get_row_wise_input("GOAL")

    print("\nSearching for a solution...")
    solution = iterative_deepening_search(initial_state, goal_state, max_depth)
    
    if solution:
        print(f"\nSolution found in {len(solution) - 1} steps!")
        for idx, step in enumerate(solution):
            print(f"\nStep {idx}:")
            print(step[0:3])
            print(step[3:6])
            print(step[6:9])
    else:
        print(f"\nNo solution found within the depth limit of {max_depth}.")

if __name__ == "__main__":
    main()
