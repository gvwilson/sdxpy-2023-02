from match import Lit, Any, Either, Null, Not, Range


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


def test_either_two_literals_first():
    assert Either(Lit("a"), Lit("b")).match("a")


def test_either_two_literals_second():
    assert Either(Lit("a"), Lit("b")).match("b")


def test_either_two_literals_neither():
    assert not Either(Lit("a"), Lit("b")).match("c")


def test_either_two_literals_not_both():
    assert not Either(Lit("a"), Lit("b")).match("ab")


def test_either_after_any():
    assert Any(Either(Lit("x"), Lit("y"))).match("abcx")


def test_either_followed_by_literal_match():
    assert Either(Lit("a"), Lit("b"), rest=Lit("c")).match("bc")


def test_either_followed_by_literal_no_match():
    assert not Either(Lit("a"), Lit("b"), Lit("c")).match("ax")


def test_null_matches_nothing():
    assert Null().match("")


def test_null_does_not_match_anything():
    assert not Null().match("a")


def test_not_match():
    assert not Not(Lit("abc")).match("abc")


def test_not_not_match():
    assert Not(Lit("abx")).match("xyz")


def test_not_match_then_match():
    assert Not(Lit("abc"), Lit("def")).match("xyzdef")


def test_not_match_nested():
    assert Not(Lit("abc", Not(Lit("def")))).match("uvwxyz")


def test_half_match_nested():
    assert Lit("abc", Not(Lit("def"))).match("abcxyz")


def test_not_half_match_nested():
    assert not Not(Lit("abc", Not(Lit("def")))).match("abcxyz")


def test_not_any():
    assert not Not(Any()).match("")
    assert not Not(Any()).match("a")


def test_not_any_matches_as_prefix():
    assert not Not(Any(Lit("def"))).match("abcdef")


def test_not_any_matches_as_suffix():
    assert not Lit("abc", Not(Any())).match("abcdef")


def test_not_any_matches_interior():
    assert not Lit("a", Not(Any(Lit("c")))).match("abc")


def test_not_either_two_literals_first():
    assert Not(Either(Lit("a"), Lit("b"))).match("c")


def test_either_three_patterns():
    assert Either(Lit("a"), Lit("b"), Lit("c"), rest=None).match("b")


def test_either_no_patterns():
    assert Either(rest=Lit("a")).match("a")


def test_either_one_pattern():
    assert Either(Lit("a")).match("a")


def test_in_range():
    assert Range("a", "h").match("d")


def test_start_of_range():
    assert Range("a", "h").match("a")


def test_end_of_range():
    assert Range("a", "h").match("h")


def test_range_case():
    assert not Range("a", "z").match("A")


def test_outside_of_range():
    assert not Range("a", "h").match("s")


def test_not_range():
    assert Not(Range("a", "h")).match("j")


def test_not_range_rest():
    assert Not(Range("a", "h"), Lit("s")).match("js")


def test_empty_either():
    assert Either().match("")


def test_empty_either_match_something():
    assert not Either().match("s")
