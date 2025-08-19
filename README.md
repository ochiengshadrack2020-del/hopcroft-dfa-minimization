# 🏆 Coding Challenge: Hopcroft DFA Minimization

This repository implements **Hopcroft’s algorithm** to minimize a deterministic finite automaton (DFA).  
The task is to partition DFA states into equivalence classes of the minimal DFA.

---

## 📌 Task

Implement:

```python
hopcroft_minimize(accepting_states, input_alphabet, inverse_transition_func)
```

### **Inputs**
- `accepting_states`: `set` of accepting states
- `input_alphabet`: `set` of symbols
- `inverse_transition_func`: `dict` mapping `(symbol, state) -> set of predecessor states`

### **Output**
- Collection of partitions of states, represented as `frozenset`s  
  (e.g. `{frozenset({0, 1}), frozenset({2})}`)

### **Constraints**
- Handle large state spaces efficiently
- Missing predecessors = treated as empty
- Use only Python built-ins (no external libraries)

---

## 📂 Repo Layout

```
solution/
  ├── main.py   # Implementation
  └── test.py   # Unit tests
README.md        # This file
```

---

## ⚙️ Implementation

`solution/main.py`

```python
from collections import deque
from typing import Any, Dict, Set, Tuple, FrozenSet


def _all_states(accepting_states, input_alphabet, inverse_transition_func):
    states = set(accepting_states)
    for (sym, tgt), preds in inverse_transition_func.items():
        states.add(tgt)
        states.update(preds)
    return states


def hopcroft_minimize(accepting_states, input_alphabet, inverse_transition_func):
    Q = _all_states(accepting_states, input_alphabet, inverse_transition_func)

    # Initial partition
    F = set(accepting_states) & Q
    NF = Q - F
    P = []
    if F: P.append(F)
    if NF: P.append(NF)

    if len(P) <= 1:
        return {frozenset(block) for block in P}

    block_of = {s: idx for idx, blk in enumerate(P) for s in blk}
    W = deque()

    # Initialize worklist with the smaller block for each symbol
    if F and NF:
        smaller_idx = 0 if len(F) <= len(NF) else 1
        for a in input_alphabet:
            W.append((smaller_idx, a))

    def predecessors(block_states, symbol):
        preds = set()
        for t in block_states:
            preds.update(inverse_transition_func.get((symbol, t), set()))
        return preds

    while W:
        A_idx, a = W.popleft()
        if A_idx >= len(P) or not P[A_idx]:
            continue
        A = P[A_idx]
        predA = predecessors(A, a)
        if not predA:
            continue

        affected = {}
        for q in predA:
            b = block_of.get(q)
            if b is None or not P[b]:
                continue
            affected.setdefault(b, set()).add(q)

        for Y_idx, X in affected.items():
            Y = P[Y_idx]
            if not X or len(X) == len(Y):
                continue
            Y_minus_X = Y - X
            if len(X) <= len(Y_minus_X):
                new_block, kept_block = Y_minus_X, X
            else:
                new_block, kept_block = X, Y_minus_X
            P[Y_idx] = kept_block
            new_idx = len(P)
            P.append(new_block)
            for s in new_block:
                block_of[s] = new_idx
            for s in kept_block:
                block_of[s] = Y_idx
            smaller_idx = new_idx if len(new_block) <= len(kept_block) else Y_idx
            for sym in input_alphabet:
                W.append((smaller_idx, sym))

    return {frozenset(blk) for blk in P if blk}


if __name__ == "__main__":
    accepting = {1}
    sigma = {'a'}
    inv = {('a', 1): {0, 1}}
    print("Partition:", hopcroft_minimize(accepting, sigma, inv))
```

---

## 🧪 Tests

`solution/test.py`

```python
from solution.main import hopcroft_minimize


def test_two_state_chain():
    accepting = {1}
    sigma = {'a'}
    inv = {('a', 1): {0, 1}}
    parts = hopcroft_minimize(accepting, sigma, inv)
    assert parts == {frozenset({0}), frozenset({1})}


def test_all_accepting_equivalent():
    accepting = {0, 1, 2}
    sigma = {'a', 'b'}
    inv = {
        ('a', 0): {0},
        ('b', 1): {1, 2},
        ('a', 2): {2},
    }
    parts = hopcroft_minimize(accepting, sigma, inv)
    assert parts == {frozenset({0, 1, 2})}


def test_three_sinks_merge():
    accepting = {3}
    sigma = {'a', 'b'}
    inv = {
        ('a', 0): {0}, ('b', 0): {0},
        ('a', 1): {1}, ('b', 1): {1},
        ('a', 2): {2}, ('b', 2): {2},
        ('a', 3): {3}, ('b', 3): {3},
    }
    parts = hopcroft_minimize(accepting, sigma, inv)
    assert parts == {frozenset({0,1,2}), frozenset({3})}


def test_distinguishable_by_depth():
    accepting = {2}
    sigma = {'a'}
    inv = {('a', 1): {0}, ('a', 2): {1, 2}}
    parts = hopcroft_minimize(accepting, sigma, inv)
    assert parts == {frozenset({0}), frozenset({1}), frozenset({2})}


def test_missing_predecessors_and_extraneous_states():
    accepting = {5}
    sigma = {'x', 'y'}
    inv = {
        ('x', 4): {1, 2},
        ('y', 3): set(),
        ('x', 6): {4},
    }
    parts = hopcroft_minimize(accepting, sigma, inv)
    nonacc = frozenset({1,2,3,4,6})
    acc = frozenset({5})
    assert {nonacc, acc} == parts or {acc, nonacc} == parts
```

---

## ▶️ Running Locally

```bash
# Run implementation demo
python solution/main.py

# Run tests
python -m pytest -q solution/test.py
```

---

## 🚀 Upload to GitHub

```bash
git init
git add -A
git commit -m "Implement Hopcroft DFA minimization"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/beat-hopcroft.git
git push -u origin main
```

---

✅ Passing CI = passing the challenge.  
You now have a fully working Hopcroft minimization repo with tests.
