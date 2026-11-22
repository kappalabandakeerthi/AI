import math
import random


def calculate_conflicts(board):
  """Calculates the total number of pair conflicts (row and diagonal collisions).

  Index represents the Column, Value represents the Row.
  """
  conflicts = 0
  n = len(board)

  # Check every unique pair of columns
  for c1 in range(n):
    for c2 in range(c1 + 1, n):
      r1 = board[c1]
      r2 = board[c2]

      # Constraint 1: Row Collision (Two queens share the same row value)
      if r1 == r2:
        conflicts += 1

      # Constraint 2: Diagonal Collision (|r1 - r2| == |c1 - c2|)
      if abs(r1 - r2) == abs(c1 - c2):
        conflicts += 1

  return conflicts


def solve_8_queens_annealing():
  print("--- Simulated Annealing: 8-Queens Puzzle ---")
  print("Representation: Index = Column, Value = Row (Valid range: 0-7)")
  print("Provide 8 space-separated row integers (e.g., 0 1 2 3 4 5 6 7):\n")

  # 1. Handle User Input
  try:
    user_input = input("Enter initial board layout: ")
    current_board = [int(x) for x in user_input.split()]
    if len(current_board) != 8 or any(x < 0 or x > 7 for x in current_board):
      raise ValueError
  except ValueError:
    print(
        "\n[!] Invalid format. Defaulting to diagonal board: [0, 1, 2, 3, 4, 5,"
        " 6, 7]"
    )
    current_board = list(range(8))

  # Calculate initial state metrics
  current_conflicts = calculate_conflicts(current_board)

  # Annealing Hyperparameters
  T = 10.0
  alpha = 0.95
  step = 0

  print(
      f"\n[INITIAL STATE] Board: {current_board} | Conflicts:"
      f" {current_conflicts}\n"
  )
  print(
      f"{'Step':<6} | {'Proposed Mutation':<35} | {'Conflicts':<10} |"
      f" {'Decision Basis':<25}"
  )
  print("-" * 85)

  # Loop until a solution with exactly 0 conflicts is discovered
  while current_conflicts > 0:
    step += 1

    # 2. Neighbor Generation: Pick a random column and change its row value
    target_col = random.randint(0, 7)
    old_row = current_board[target_col]

    # Select a brand new row position
    new_row = random.randint(0, 7)
    while new_row == old_row:
      new_row = random.randint(0, 7)

    # Construct the proposed neighbor board state
    proposed_board = list(current_board)
    proposed_board[target_col] = new_row
    proposed_conflicts = calculate_conflicts(proposed_board)

    # 3. Acceptance Criterion (Metropolis-Hastings Engine)
    delta_E = proposed_conflicts - current_conflicts
    action_log = f"Col {target_col}: Row {old_row} -> Row {new_row}"

    if delta_E < 0:
      # Always accept a structurally better layout
      decision = "ACCEPT (Fewer Conflicts)"
      current_board = proposed_board
      current_conflicts = proposed_conflicts
    else:
      # Worse or neutral layout: evaluate probabilistically
      p = math.exp(-delta_E / T)
      r = random.random()
      if r < p:
        decision = f"ACCEPT (Probabilistic R:{r:.3f} < P:{p:.3f})"
        current_board = proposed_board
        current_conflicts = proposed_conflicts
      else:
        decision = f"REJECT (Probabilistic R:{r:.3f} >= P:{p:.3f})"

    # Log step progress
    print(
        f"{step:<6} | {action_log:<35} | {proposed_conflicts:<10} | {decision}"
    )

    # 4. Decrease system temperature according to cooling factor
    T *= alpha

    # 5. Local Minima Escape Mechanism: Re-heat if system cools without resolving completely
    if T < 0.01 and current_conflicts > 0:
      print(f"--- [SYSTEM RE-HEAT] Temperature reset to break local minimum ---")
      T = 8.0

  print("-" * 85)
  print(
      f"\n[SUCCESS] Solution found in {step} total steps!"
      f"\nFinal Board Vector (Index=Col, Val=Row): {current_board}"
      f"\nRemaining Conflicts: {current_conflicts}"
  )


if __name__ == "__main__":
  # Set a constant seed value for predictable trace validation across runs
  random.seed(42)
  solve_8_queens_annealing()
