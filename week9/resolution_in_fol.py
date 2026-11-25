import re

def parse_literal(lit_str):
    lit_str = lit_str.strip()
    neg = lit_str.startswith('~') or lit_str.startswith('¬')
    if neg:
        lit_str = lit_str[1:].strip()

    match = re.match(r'^([A-Za-z0-9_]+)\((.*)\)$', lit_str)
    if not match:
        raise ValueError(f"Invalid literal format: {lit_str}")
    pred = match.group(1)
    args = [arg.strip() for arg in match.group(2).split(',')]
    return (neg, pred, tuple(args))

def format_literal(lit):
    neg, pred, args = lit
    prefix = "~" if neg else ""
    return f"{prefix}{pred}({', '.join(args)})"

def format_clause(clause):
    if not clause:
        return "{} (Empty Clause - Contradiction)"
    return " V ".join(format_literal(lit) for lit in clause)

def is_variable(term):
    return term.islower() and '(' not in term

def unify(x, y, subst=None):
    if subst is None:
        subst = {}
    if x == y:
        return subst
    if isinstance(x, str) and is_variable(x):
        return unify_var(x, y, subst)
    if isinstance(y, str) and is_variable(y):
        return unify_var(y, x, subst)
    if isinstance(x, tuple) and isinstance(y, tuple) and len(x) == len(y):
        for a, b in zip(x, y):
            subst = unify(a, b, subst)
            if subst is None:
                return None
        return subst
    return None

def unify_var(var, x, subst):
    if var in subst:
        return unify(subst[var], x, subst)
    if isinstance(x, str) and x in subst:
        return unify(var, subst[x], subst)
    if occur_check(var, x, subst):
        return None
    new_subst = subst.copy()
    new_subst[var] = x
    return new_subst

def occur_check(var, x, subst):
    if var == x:
        return True
    if isinstance(x, str) and x in subst:
        return occur_check(var, subst[x], subst)
    if isinstance(x, tuple):
        return any(occur_check(var, elem, subst) for elem in x)
    return False

def apply_subst_term(term, subst):
    while isinstance(term, str) and term in subst:
        term = subst[term]
    return term

def apply_subst_literal(lit, subst):
    neg, pred, args = lit
    new_args = tuple(apply_subst_term(arg, subst) for arg in args)
    return (neg, pred, new_args)

def resolve_clauses(c1, c2):
    resolvents = []
    for l1 in c1:
        neg1, pred1, args1 = l1
        for l2 in c2:
            neg2, pred2, args2 = l2
            # Check opposite signs, same predicate name, and same number of arguments
            if neg1 != neg2 and pred1 == pred2 and len(args1) == len(args2):
                subst = unify(args1, args2, {})
                if subst is not None:
                    new_c1 = [apply_subst_literal(l, subst) for l in c1 if l != l1]
                    new_c2 = [apply_subst_literal(l, subst) for l in c2 if l != l2]
                    combined = []
                    for l in new_c1 + new_c2:
                        if l not in combined:
                            combined.append(l)
                    resolvents.append((tuple(combined), subst))
    return resolvents

def fol_resolution(kb_clauses, negated_query_clauses):
    clauses = list(kb_clauses) + list(negated_query_clauses)
    seen = set(frozenset(c) for c in clauses)

    print("\n--- Initial Clauses (KB + Negated Query) ---")
    for idx, c in enumerate(clauses, 1):
        print(f"{idx}. {format_clause(c)}")
    print("\n--- Resolution Steps ---")

    step = 1
    while True:
        new_clauses = []
        n = len(clauses)
        for i in range(n):
            for j in range(i + 1, n):
                resolvents = resolve_clauses(clauses[i], clauses[j])
                for res, subst in resolvents:
                    res_set = frozenset(res)
                    if not res:
                        print(f"Step {step}: Resolve [{format_clause(clauses[i])}] and [{format_clause(clauses[j])}]")
                        if subst:
                            print(f"    Unification: {subst}")
                        print(f"    Resolvent: {format_clause(res)}")
                        return True
                    if res_set not in seen:
                        seen.add(res_set)
                        new_clauses.append(res)
                        print(f"Step {step}: Resolve [{format_clause(clauses[i])}] and [{format_clause(clauses[j])}]")
                        if subst:
                            print(f"    Unification: {subst}")
                        print(f"    Resolvent: {format_clause(res)}")
                        step += 1
        if not new_clauses:
            return False
        clauses.extend(new_clauses)

def main():
    print("=== First-Order Logic (FOL) Resolution Prover ===")
    print("Formatting Rules:")
    print(" - Use lowercase for variables (e.g., x, y, z)")
    print(" - Use Uppercase for constants and predicates (e.g., John, Peanuts, Food(x))")
    print(" - Use '~' for negation and ' | ' or ' V ' (with spaces) for OR\n")

    num_clauses = int(input("Enter the number of CNF clauses in the Knowledge Base: "))
    kb = []
    for i in range(num_clauses):
        raw = input(f"Clause {i+1}: ")
        # Split on '|' or ' V ' with spaces so words like 'Vegetables' are not split
        parts = re.split(r'\s*\|\s*|\s+V\s+', raw.strip())
        literals = [parse_literal(part) for part in parts if part]
        kb.append(tuple(literals))

    query_raw = input("\nEnter the single atomic query to prove (e.g., Likes(John, Peanuts)): ")
    q_neg, q_pred, q_args = parse_literal(query_raw)
    negated_query = [((not q_neg, q_pred, q_args),)]

    proved = fol_resolution(kb, negated_query)
    print("\n=== Result ===")
    if proved:
        print(f"Hence Proved: {query_raw} follows from the Knowledge Base.")
    else:
        print(f"Cannot Prove: {query_raw} does not follow from the Knowledge Base.")

if __name__ == "__main__":
    main()
