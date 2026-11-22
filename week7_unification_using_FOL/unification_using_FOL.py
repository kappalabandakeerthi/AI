import re

def is_variable(x):
    """
    Generic variable check:
    Treats lowercase words (like x, y, z, variable1)
    OR common uppercase variable tokens (X, Y, Z) as variables.
    """
    if isinstance(x, str) and len(x) > 0:
        return x.islower() or x in ['X', 'Y', 'Z']
    return False

def is_compound(x):
    return isinstance(x, (list, tuple)) and len(x) > 0

def substitute(subst, term):
    if is_variable(term):
        return subst.get(term, term)
    if is_compound(term):
        return [term[0]] + [substitute(subst, arg) for arg in term[1:]]
    return term

def occurs_check(var, term, subst):
    if var == term:
        return True
    if is_variable(term):
        if term in subst:
            return occurs_check(var, subst[term], subst)
        return False
    if is_compound(term):
        return any(occurs_check(var, arg, subst) for arg in term[1:])
    return False

def unify_var(var, x, subst, trace):
    if var in subst:
        return unify(subst[var], x, subst, trace)
    if is_variable(x) and x in subst:
        return unify(var, subst[x], subst, trace)

    if occurs_check(var, x, subst):
        trace.append(f"FAIL: Occurs-Check Failed. Variable '{var}' occurs inside '{x}' causing an infinite loop.")
        return None

    trace.append(f"OPERATION: Binding variable '{var}' to '{x}'")
    new_subst = subst.copy()
    new_subst[var] = x

    for k, v in list(new_subst.items()):
        if k != var:
            new_subst[k] = substitute({var: x}, v)

    return new_subst

def unify(x, y, subst=None, trace=None):
    if subst is None:
        subst = {}
    if trace is None:
        trace = []

    if x == y:
        return subst

    if is_variable(x):
        return unify_var(x, y, subst, trace)

    if is_variable(y):
        return unify_var(y, x, subst, trace)

    if is_compound(x) and is_compound(y):
        # Position 0 contains the name of the function or predicate symbol
        if x[0] != y[0]:
            trace.append(f"FAIL: Predicate/Function symbol mismatch ('{x[0]}' vs '{y[0]}').")
            return None

        if len(x) != len(y):
            trace.append(f"FAIL: Argument count mismatch between structural layers.")
            return None

        for arg_x, arg_y in zip(x[1:], y[1:]):
            subst = unify(substitute(subst, arg_x), substitute(subst, arg_y), subst, trace)
            if subst is None:
                return None
        return subst

    trace.append(f"FAIL: Constant mismatch. Cannot match distinct items '{x}' and '{y}'.")
    return None

def parse_string(s):
    """
    Parses a string like 'p(f(a), g(Y))' into a nested list structure like ['p', ['f', 'a'], ['g', 'Y']]
    """
    s = s.replace(" ", "")
    tokens = re.findall(r'[A-Za-z0-9]+|[\(\),]', s)

    def parse_expr(token_list):
        if not token_list:
            return None
        token = token_list.pop(0)
        if token_list and token_list[0] == '(':
            token_list.pop(0)  # pop '('
            args = []
            while token_list[0] != ')':
                args.append(parse_expr(token_list))
                if token_list[0] == ',':
                    token_list.pop(0)  # pop ','
            token_list.pop(0)  # pop ')'
            return [token] + args
        return token

    try:
        return parse_expr(tokens)
    except:
        return None

def format_output(subst_dict):
    if not subst_dict:
        return "{}"
    return "{" + ", ".join([f"{k}/{v}".replace("'", "").replace("[", "").replace("]", "").replace(", ", "(").replace("(", "(", 1) for k, v in subst_dict.items()]) + "}"

def interactive_unifier():
    print("=== Universal First-Order Logic Unifier ===")
    print("Enter your statements using standard notation, e.g., Knows(John, x)")
    print("Type 'exit' to quit.\n")

    while True:
        str1 = input("Enter Expression 1: ").strip()
        if str1.lower() == 'exit': break
        str2 = input("Enter Expression 2: ").strip()
        if str2.lower() == 'exit': break

        expr1 = parse_string(str1)
        expr2 = parse_string(str2)

        if not expr1 or not expr2:
            print("Syntax Error: Make sure your brackets are properly closed and formatted.\n")
            continue

        trace = []
        result = unify(expr1, expr2, subst=None, trace=trace)

        print("\n--- Unification Report ---")
        if result is not None:
            print("STATUS: Unifiable [SUCCESS]")
            print("STEPS PERFORMED:")
            for step in trace:
                print(f"  -> {step}")
            print(f"FINAL MOST GENERAL UNIFIER: {format_output(result)}\n")
        else:
            print("STATUS: Not Unifiable [FAILED]")
            print(f"REASON FOR FAILURE:\n  -> {trace[-1] if trace else 'Structural mismatch.'}\n")
        print("="*50)

if __name__ == "__main__":
    interactive_unifier()
