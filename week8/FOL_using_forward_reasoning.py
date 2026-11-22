
# FIRST ORDER LOGIC - FORWARD CHAINING

# ---------------- STEP 1: INPUT PARSING ----------------

import ast

def parse_tuple_input(prompt_text):
    """Parse user input safely."""
    val = input(prompt_text).strip()

    if not val:
        return []

    try:
        return ast.literal_eval(val)

    except Exception as e:
        print("Invalid input:", e)
        return None


# ---------------- STEP 2: FORWARD CHAINING ENGINE ----------------

class FOLForwardChaining:

    def __init__(self, initial_kb, rules):
        self.kb = set(tuple(fact) for fact in initial_kb)
        self.rules = rules

    # Unification
    def unify(self, pattern, fact, theta):

        if pattern[0] != fact[0] or len(pattern) != len(fact):
            return None

        theta = theta.copy()

        for p, f in zip(pattern[1:], fact[1:]):

            if p.startswith("?"):

                if p in theta:
                    if theta[p] != f:
                        return None
                else:
                    theta[p] = f

            elif p != f:
                return None

        return theta

    # Match all premises
    def match_premises(self, premises, facts, theta, index=0):

        if index == len(premises):
            return [theta]

        results = []

        for fact in facts:

            new_theta = self.unify(
                premises[index], fact, theta
            )

            if new_theta is not None:

                results.extend(
                    self.match_premises(
                        premises,
                        facts,
                        new_theta,
                        index + 1
                    )
                )

        return results

    # Substitute variables
    def substitute(self, conclusion, theta):

        return tuple(
            theta.get(arg, arg) for arg in conclusion
        )

    # Forward chaining algorithm
    def run(self, goal, verbose=True):

        goal = tuple(goal)
        iteration = 1

        if verbose:
            print("\nInitial Knowledge Base:")

            for fact in sorted(self.kb):
                print(" ", fact)

        while True:

            new_facts = set()

            if verbose:
                print(f"\n========== ITERATION {iteration} ==========")

            for premises, conclusion in self.rules:

                substitutions = self.match_premises(
                    premises,
                    self.kb,
                    {}
                )

                for theta in substitutions:

                    derived = self.substitute(
                        conclusion,
                        theta
                    )

                    if derived not in self.kb and derived not in new_facts:

                        if verbose:
                            print("\nRule Applied:")
                            print(premises, "=>", conclusion)
                            print("Substitution:", theta)
                            print("Derived Fact:", derived)

                        if derived == goal:
                            print("\nSUCCESS!")
                            print("Goal Proved:", goal)
                            return True

                        new_facts.add(derived)

            if not new_facts:

                print("\nFAILURE!")
                print("Goal cannot be proved:", goal)
                return False

            self.kb.update(new_facts)
            iteration += 1


# ---------------- STEP 3: INTERACTIVE INTERFACE ----------------

def interactive_solver():

    print("=" * 55)
    print("     FOL FORWARD CHAINING SOLVER")
    print("=" * 55)

    # Initial facts
    print("\nStep 1: Enter Initial Knowledge Base (Facts)")
    print('Example: [("American", "Robert"), ("Missile", "T1")]')

    kb_input = None

    while kb_input is None:
        kb_input = parse_tuple_input("Enter KB Facts: ")

    # Rules
    print("\nStep 2: Enter Inference Rules")
    print('Example: [([("Missile", "?x")], ("Weapon", "?x"))]')

    rules_input = None

    while rules_input is None:
        rules_input = parse_tuple_input("Enter Inference Rules: ")

    # Goal
    print("\nStep 3: Enter Target Goal")
    print('Example: ("Criminal", "Robert")')

    goal_input = None

    while goal_input is None:
        goal_input = parse_tuple_input("Enter Target Goal: ")

        if isinstance(goal_input, list) and len(goal_input) == 1:
            goal_input = goal_input[0]

        if not isinstance(goal_input, tuple):
            print("Please enter the goal as a tuple.")
            goal_input = None

    # Run engine
    print("\nProcessing input and running inference...")

    engine = FOLForwardChaining(
        initial_kb=kb_input,
        rules=rules_input
    )

    engine.run(goal=goal_input, verbose=True)


# ---------------- STEP 4: EXECUTION ----------------

if __name__ == "__main__":
    interactive_solver()
