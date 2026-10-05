import heapq

class PuzzleNode:
    def __init__(self, state, parent=None, move=None, g=0, h=0):
        self.state = state      # 1D tuple of length 9 representing 3x3 grid
        self.parent = parent    # Link to parent node to reconstruct path
        self.move = move        # The direction moved to get here ('Up', 'Down', etc.)
        self.g = g              # g(n): Cost from start to current node
        self.h = h              # h(n): Manhattan distance to goal
        self.f = g + h          # f(n): Total estimated cost

    # Defining comparison operators for priority queue sorting by total cost f(n)
    def __lt__(self, other):
        if self.f == other.f:
            return self.g > other.g  # Tie-breaker: Prefer deeper nodes
        return self.f < other.f

def get_manhattan_distance(state, goal_state):
    """Calculates total Manhattan Distance heuristic h(n) value for a state."""
    distance = 0
    goal_positions = {value: (i // 3, i % 3) for i, value in enumerate(goal_state)}
    
    for i, value in enumerate(state):
        if value != 0:  # Exclude the blank tile
            curr_row, curr_col = i // 3, i % 3
            goal_row, goal_col = goal_positions[value]
            distance += abs(curr_row - goal_row) + abs(curr_col - goal_col)
    return distance

def get_neighbors(node, goal_state):
    """Generates valid neighbor nodes by sliding tiles into the empty space (0)."""
    neighbors = []
    state = node.state
    blank_idx = state.index(0)
    row, col = blank_idx // 3, blank_idx % 3

    moves = [
        (-1, 0, 'Up'),
        (1, 0, 'Down'),
        (0, -1, 'Left'),
        (0, 1, 'Right')
    ]

    for dr, dc, move_name in moves:
        new_row, new_col = row + dr, col + dc
        
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_blank_idx = new_row * 3 + new_col
            
            new_state = list(state)
            new_state[blank_idx], new_state[new_blank_idx] = new_state[new_blank_idx], new_state[blank_idx]
            new_state_tuple = tuple(new_state)

            h = get_manhattan_distance(new_state_tuple, goal_state)
            neighbors.append(PuzzleNode(new_state_tuple, node, move_name, node.g + 1, h))
            
    return neighbors

def solve_8_puzzle(start_state, goal_state):
    """Solves the 8-puzzle problem using A* and tracks mathematical node variables."""
    start_tuple = tuple(start_state)
    goal_tuple = tuple(goal_state)

    start_h = get_manhattan_distance(start_tuple, goal_tuple)
    start_node = PuzzleNode(start_tuple, g=0, h=start_h)

    open_list = [start_node]
    visited = set()

    while open_list:
        current_node = heapq.heappop(open_list)

        if current_node.state == goal_tuple:
            path = []
            while current_node:
                path.append(current_node)
                current_node = current_node.parent
            return path[::-1] # Return complete path from start to goal

        visited.add(current_node.state)

        for neighbor in get_neighbors(current_node, goal_tuple):
            if neighbor.state in visited:
                continue
            heapq.heappush(open_list, neighbor)

    return None

def print_grid(state):
    """Prints a 1D state array cleanly in a 3x3 layout block."""
    for i in range(0, 9, 3):
        print(f"  {state[i]} {state[i+1]} {state[i+2]}  ")

def parse_input_state(prompt_text):
    """Helper to cleanly receive and format 9 numbers from a terminal command line."""
    print(prompt_text)
    print("Enter 9 numbers (0-8) separated by spaces (0 represents blank space):")
    while True:
        try:
            user_input = input().strip().split()
            state = [int(x) for x in user_input]
            if len(state) == 9 and sorted(state) == list(range(9)):
                return state
            print("Invalid input! Please enter exactly 9 unique digits from 0 to 8:")
        except ValueError:
            print("Invalid format! Please enter numbers only:")

# --- Driver Execution Loop ---
if __name__ == "__main__":
    print("=== 8-PUZZLE A* SEARCH SOLVER ===\n")
    
    # Standard Interactive Inputs
    # Example format to type in terminal: 1 2 3 5 6 0 7 8 4
    initial_puzzle = parse_input_state("--- Define Initial State ---")
    print()
    target_puzzle = parse_input_state("--- Define Target (Goal) State ---")
    print("\nProcessing path calculation...\n")

    solution_nodes = solve_8_puzzle(initial_puzzle, target_puzzle)

    if solution_nodes:
        print(f"🏁 Solved successfully in {len(solution_nodes) - 1} moves!\n")
        print("=========================================")
        
        for step, node in enumerate(solution_nodes):
            if step == 0:
                print(f" [START STATE]")
            else:
                print(f" [STEP {step}] Move Blank Tile: '{node.move}'")
            
            print_grid(node.state)
            print(f" Metrics ->  g(n) = {node.g} | h(n) = {node.h} | f(n) = {node.f}")
            print("=========================================")
    else:
        print("❌ Unsolvable Puzzle: No path exists between these two configurations.")
