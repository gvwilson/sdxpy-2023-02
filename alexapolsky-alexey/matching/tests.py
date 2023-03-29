import pytest

from direct import Alt, Any, End, Lit, Start, Not, Range

TESTS = [
    ["a", "b", True, Not(Lit("a"))],


    ["a", "a", True, Lit("a")],
    ["b", "a", False, Lit("b")],
    ["a", "ab", True, Lit("a")],
    ["b", "ab", True, Lit("b")],
    ["ab", "ab", True, Lit("a", Lit("b"))],
    ["ba", "ab", False, Lit("b", Lit("a"))],
    ["ab", "ba", False, Lit("ab")],
    # ["^a", "ab", True, Start(Lit("a"))],
    # ["^b", "ab", False, Start(Lit("b"))],
    # ["a$", "ab", False, Lit("a", End())],
    # ["a$", "ba", True, Lit("a", End())],
    ["a*", "", True, Any(Lit("a"))],
    ["a*", "baac", True, Any(Lit("a"))],
    ["ab*c", "ac", True, Lit("a", Any(Lit("b"), Lit("c")))],
    ["ab*c", "abc", True, Lit("a", Any(Lit("b"), Lit("c")))],
    ["ab*c", "abbbc", True, Lit("a", Any(Lit("b"), Lit("c")))],
    ["ab*c", "abxc", False, Lit("a", Any(Lit("b"), Lit("c")))],
    # ["ab|cd", "xaby", True, Alt(Lit("ab"), Lit("cd"))],
    # ["ab|cd", "acdc", True, Alt(Lit("ab"), Lit("cd"))],
    # ["a(b|c)d", "xabdy", True, Lit("a", Alt(Lit("b"), Lit("c")), Lit("d"))],
    # ["a(b|c)d", "xabady", False, Lit("a", Alt(Lit("b"), Lit("c")), Lit("d"))],
    ["a", "a", True, Range("a", "z")],
    ["n", "n", True, Range("a", "z")],
    [">", ">", False, Range("a", "z")],
    ["[a-z]a", "8a", False, Range("a", "z", Lit("a"))],
    ["8[a-z]", "8a", True, Lit("8", Range("a", "z"))]
]

@pytest.mark.parametrize("params", TESTS)
def test_direct(params):
    pattern, text, expected, matcher = params
    actual = matcher.match(text)
    assert actual == expected, f"{pattern} vs {text}"

