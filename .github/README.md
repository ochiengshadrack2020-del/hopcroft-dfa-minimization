# Hopcroft DFA Minimization

This project implements **Hopcroft's algorithm** to minimize a deterministic finite automaton (DFA).

## Task
Implement a function `hopcroft_minimize(accepting_states, input_alphabet, inverse_transition_func)` that returns the minimized DFA as a partition of states.

### Input
- `accepting_states`: set of accepting states
- `input_alphabet`: set of symbols
- `inverse_transition_func`: dict mapping `(symbol, state) → set of predecessor states`

### Output
- A collection of partitions (e.g., `{frozenset({...}), ...}`) representing equivalent state classes.

## Repo Layout
```
solution/main.py   # Implementation
solution/test.py   # Unit tests
README.md          # Project documentation
```

## Running
Run the solution (optional):
```bash
python solution/main.py
```

Run tests with:
```bash
python -m pytest -q solution/test.py
```

## Submission
Commit and push to main branch:
```bash
git add -A
git commit -m "Implement solution"
git push origin main
```
