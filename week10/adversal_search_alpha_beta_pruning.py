class Node:
    def __init__(self, name, value=None):
        self.name = name
        self.value = value
        self.children = []

pruned_branches = []

def print_tree(node, level=0):
    indent = "    " * level
    if not node.children:
        print(f"{indent}- {node.name} (Leaf: {node.value})")
    else:
        print(f"{indent}- {node.name}")
        for child in node.children:
            print_tree(child, level + 1)

def alpha_beta(node, depth, alpha, beta, maximizing_player, path):
    current_path = path + [node.name]

    # Base case: leaf node
    if not node.children:
        return node.value, current_path

    if maximizing_player:
        max_eval = float('-inf')
        best_path = current_path
        for i, child in enumerate(node.children):
            eval_val, child_path = alpha_beta(child, depth + 1, alpha, beta, False, current_path)
            if eval_val > max_eval:
                max_eval = eval_val
                best_path = child_path
            alpha = max(alpha, eval_val)
            if beta <= alpha:
                # Record remaining unvisited sibling branches as pruned
                for remaining in node.children[i + 1:]:
                    pruned_branches.append(f"{node.name} -> {remaining.name}")
                break
        return max_eval, best_path
    else:
        min_eval = float('inf')
        best_path = current_path
        for i, child in enumerate(node.children):
            eval_val, child_path = alpha_beta(child, depth + 1, alpha, beta, True, current_path)
            if eval_val < min_eval:
                min_eval = eval_val
                best_path = child_path
            beta = min(beta, eval_val)
            if beta <= alpha:
                # Record remaining unvisited sibling branches as pruned
                for remaining in node.children[i + 1:]:
                    pruned_branches.append(f"{node.name} -> {remaining.name}")
                break
        return min_eval, best_path

def build_tree_from_input():
    print("--- Build Your Custom Tree ---")
    print("We will construct a tree where internal nodes branch, and leaf nodes hold numeric values.\n")

    nodes = {}

    # Helper to get or create a node
    def get_or_create(name):
        if name not in nodes:
            nodes[name] = Node(name)
        return nodes[name]

    # Get leaf values first
    try:
        num_leaves = int(input("Enter the number of leaf nodes: "))
        for _ in range(num_leaves):
            name = input("Enter leaf node name: ").strip()
            val = float(input(f"Enter evaluation value for leaf '{name}': "))
            nodes[name] = Node(name, value=val)

        # Connect parents to children
        print("\nNow define internal connections. Enter parent and its children (comma-separated).")
        print("Type 'done' when you are finished connecting nodes.")
        while True:
            parent_input = input("\nEnter parent node name (or 'done' to finish): ").strip()
            if parent_input.lower() == 'done':
                break
            children_input = input(f"Enter children names for parent '{parent_input}' (separated by commas): ")

            parent_node = get_or_create(parent_input)
            child_names = [c.strip() for c in children_input.split(",")]
            parent_node.children = [get_or_create(c_name) for c_name in child_names if c_name]

        root_name = input("\nEnter the name of the root node to start search: ").strip()
        if root_name not in nodes:
            print("Error: Root node not found!")
            return None

        return nodes[root_name]
    except Exception as e:
        print(f"An error occurred with your inputs: {e}")
        return None

if __name__ == "__main__":
    root = build_tree_from_input()

    if root:
        print("\nTree Structure:")
        print_tree(root)

        # Run search
        pruned_branches.clear()
        optimal_val, optimal_path = alpha_beta(root, 0, float('-inf'), float('inf'), True, [])

        print("\n--- Results ---")
        print(f"Value of Root Node: {optimal_val}")
        print(f"Optimal Path: {' -> '.join(optimal_path)}")
        print(f"Pruned Paths/Branches: {pruned_branches if pruned_branches else 'None'}")
    else:
        print("Could not construct the tree. Please try executing the cell again with valid inputs.")
