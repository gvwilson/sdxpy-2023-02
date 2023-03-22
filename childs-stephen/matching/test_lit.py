from match import Lit, Any


def test_literal_match_entire_string():
    assert Lit("abc").match("abc")


def test_literal_substring_alone_no_match():
    assert not Lit("ab").match("abc")


def test_literal_superstring_no_match():
    assert not Lit("abc").match("ab")


def test_literal_followed_by_literal_match():
    assert Lit("a", Lit("b")).match("ab")


def test_literal_followed_by_literal_no_match():
    assert not Lit("a", Lit("b")).match("ac")


def test_any_matches_empty():
    assert Any().match("")


def test_any_matches_entire_string():
    assert Any().match("abc")


def test_any_matches_as_prefix():
    assert Any(Lit("def")).match("abcdef")


def test_any_matches_as_suffix():
    assert Lit("abc", Any()).match("abcdef")


def test_any_matches_interior():
    assert Lit("a", Any(Lit("c"))).match("abc")
