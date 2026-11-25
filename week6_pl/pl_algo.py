from itertools import product

# Knowledge Base: (P -> Q) AND (Q -> R) AND P
def KB(model):
    P = model['P']
    Q = model['Q']
    R = model['R']
    return ((not P or Q) and (not Q or R) and P)

# Query: R
def alpha(model):
    return model['R']

# --- Method 1: Recursive Truth-Table Entailment (tt_entails) ---
def tt_entails(KB, alpha, symbols):
    return tt_check_all(KB, alpha, symbols, {})

def tt_check_all(KB, alpha, symbols, model):
    if not symbols:
        if KB(model):
            return alpha(model)
        else:
            return True

    P = next(iter(symbols))
    rest = symbols[1:]

    model_true = model.copy()
    model_true[P] = True

    model_false = model.copy()
    model_false[P] = False

    return (
        tt_check_all(KB, alpha, rest, model_true) and
        tt_check_all(KB, alpha, rest, model_false)
    )

# --- Method 2: Full Truth Table Display ---
def print_truth_table(KB, alpha, symbols):
    print("\nP Q R | P->Q Q->R | KB | R")
    print("-" * 27)

    entails = True

    for values in product([True, False], repeat=len(symbols)):
        model = dict(zip(symbols, values))

        P = model['P']
        Q = model['Q']
        R = model['R']

        p_implies_q = not P or Q
        q_implies_r = not Q or R
        kb_value = KB(model)
        query_value = alpha(model)

        print(
            f"{int(P)} {int(Q)} {int(R)} |"
            f"  {int(p_implies_q)}    {int(q_implies_r)}  |"
            f"  {int(kb_value)} | {int(query_value)}"
        )

        if kb_value and not query_value:
            entails = False

    print("-" * 27)

    if entails:
        print("KB entails the query R.")
    else:
        print("KB does not entail the query R.")

# --- Main Execution ---
if __name__ == "__main__":
    symbols = ['P', 'Q', 'R']

    print("=== Recursive Entailment Check ===")
    if tt_entails(KB, alpha, symbols):
        print("KB entails the query.")
    else:
        print("KB does not entail the query.")

    print("1BF24CS133")

    print("\n=== Full Truth Table Verification ===")
    print_truth_table(KB, alpha, symbols)
