def hopcroft_minimize(accepting_states, input_alphabet, inverse_transition_func):
    # Initial partition: accepting vs non-accepting
    states = set()
    for (_, s), preds in inverse_transition_func.items():
        states.add(s)
        states.update(preds)
    non_accepting_states = states - accepting_states

    P = [accepting_states, non_accepting_states] if non_accepting_states else [accepting_states]
    W = [accepting_states] if len(accepting_states) < len(non_accepting_states) else [non_accepting_states]

    while W:
        A = W.pop()
        for c in input_alphabet:
            X = set()
            for state in A:
                preds = inverse_transition_func.get((c, state), set())
                X.update(preds)
            new_P = []
            for Y in P:
                inter = Y & X
                diff = Y - X
                if inter and diff:
                    new_P.extend([inter, diff])
                    if Y in W:
                        W.remove(Y)
                        W.extend([inter, diff])
                    else:
                        W.append(inter if len(inter) <= len(diff) else diff)
                else:
                    new_P.append(Y)
            P = new_P
    return {frozenset(block) for block in P}


if __name__ == "__main__":
    # Example DFA
    accepting = {2}
    alphabet = {"a", "b"}
    inverse = {
        ("a", 1): {0},
        ("b", 2): {1},
        ("a", 2): {2},
        ("b", 0): {2},
    }
    result = hopcroft_minimize(accepting, alphabet, inverse)
    print("Minimized DFA partitions:", result)
