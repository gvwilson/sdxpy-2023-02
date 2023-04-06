import pytest
from start import *

# @pytest.mark.parametrize("params", TESTS)
def test_initial():
    # pattern, text, expected, matcher = params
    # actual = matcher.match(text)
    # assert actual == expected, f"{pattern} vs {text}"

    examples = [make(Square, "sq", 3), make(Circle, "ci", 2)]
    for ex in examples:
        n = ex["name"]
        d = call(ex, "density", 5)
        print(f"{n}: {d:.2f}")


def test_method_found_in_object_has_priority():
    # pattern, text, expected, matcher = params
    # actual = matcher.match(text)
    # assert actual == expected, f"{pattern} vs {text}"

    Square["area"] = lambda thing: 1

    examples = [make(Square, "sq", 3), make(Circle, "ci", 2)]
    for ex in examples:
        n = ex["name"]
        d = call(ex, "density", 5)
        if type(ex) == Square:
            assert d == 1