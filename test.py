import pytest
from solution.main import hopcroft_minimize

def test_simple_dfa():
    accepting = {2}
    alphabet = {"a", "b"}
    inverse = {
        ("a", 1): {0},
        ("b", 2): {1},
        ("a", 2): {2},
        ("b", 0): {2},
    }
    result = hopcroft_minimize(accepting, alphabet, inverse)
    assert any(2 in block for block in result)

def test_all_accepting():
    accepting = {0, 1}
    alphabet = {"a"}
    inverse = {
        ("a", 0): {0, 1},
        ("a", 1): {0, 1},
    }
    result = hopcroft_minimize(accepting, alphabet, inverse)
    assert result == {frozenset({0, 1})}

def test_all_non_accepting():
    accepting = set()
    alphabet = {"a"}
    inverse = {
        ("a", 0): {0, 1},
        ("a", 1): {0, 1},
    }
    result = hopcroft_minimize(accepting, alphabet, inverse)
    assert result == {frozenset({0, 1})}
