def print_board(state):
    """Helper function to print the 3x3 board layout."""
    for i in range(0, 9, 3):
        print(f" {state[i]} {state[i+1]} {state[i+2]} ")
    print("-" * 11)

def get_neighbors(state):
    """Generates all possible valid next states from the current state."""
    neighbors = []
    blank_idx = state.index(0)

    moves = {
        0: [1, 3],       1: [0, 2, 4],    2: [1, 5],    # Row 1
        3: [0, 4, 6],    4: [1, 3, 5, 7], 5: [2, 4, 8], # Row 2
        6: [3, 7],       7: [4, 6, 8],    8: [5, 7]     # Row 3
    }

    for move in moves[blank_idx]:
        next_state = list(state)
        next_state[blank_idx], next_state[move] = next_state[move], next_state[blank_idx]
        neighbors.append(tuple(next_state))

    return neighbors

def solve_8_puzzle_dfs(start_state, goal_state, depth_limit=50):
    """Solves the 8-puzzle using Depth-First Search with a depth safety cutoff."""
    stack = [(start_state, [start_state])]
    visited = {start_state}

    print("\nSearching for a solution using DFS... Please wait...")

    while stack:
        curr_state, path = stack.pop()

        if curr_state == goal_state:
            return path

        if len(path) > depth_limit:
            continue

        for neighbor in get_neighbors(curr_state):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append((neighbor, path + [neighbor]))

    return None

def parse_input(prompt_text):
    """Helper to take space-separated inputs and convert them into a tuple."""
    while True:
        try:
            print(prompt_text)
            user_input = input("Enter 9 numbers (0-8) separated by spaces: ")
            state = tuple(map(int, user_input.strip().split()))
            if len(state) == 9 and sorted(state) == list(range(9)):
                return state
            print("❌ Invalid layout! You must enter exactly 9 numbers from 0 to 8 without duplicates.")
        except ValueError:
            print("❌ Error: Please enter valid integers separated by spaces.")

if __name__ == "__main__":
    print("=== 8-Puzzle Solver using DFS ===")
    print("Use '0' to represent the blank tile.")
    print("Example layout format: 1 2 3 4 5 6 7 8 0\n")

    initial_state = parse_input("--- Enter INITIAL state ---")
    goal_state = parse_input("\n--- Enter GOAL state ---")

    print("\nInitial Board Layout:")
    print_board(initial_state)

    print("Goal Board Layout:")
    print_board(goal_state)

    solution_path = solve_8_puzzle_dfs(initial_state, goal_state)

    if solution_path:
        print(f"\n🎉 Success! Solution found in {len(solution_path) - 1} steps.")
        show_steps = input("Would you like to print out every step? (y/n): ").strip().lower()
        if show_steps == 'y':
            for step_num, state in enumerate(solution_path):
                print(f"\nStep {step_num}:")
                print_board(state)
    else:
        print("\n❌ No solution found or depth limit exceeded.")
