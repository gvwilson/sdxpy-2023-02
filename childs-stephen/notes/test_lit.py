from .match import Lit


def test_exact_match():
    assert Lit("abc").match("abc")


def test_pattern_too_short():
    assert not Lit("ab").match("abc")


def test_pattern_too_long():
    assert not Lit("abc").match("ab")


def test_two_literals_in_a_row():
    assert Lit("a", Lit("b", None)).match("ab")
