import pytest
from start import *


def mixintest_new(name, property1):
    return {
        "name": name,
        "_class": Shape,
        "property1": property1
    }


MixinTest = {
    "property1": 1,
    "get_property1": lambda thing: thing["property1"],
    "_classname": "MixinTest",
    "_parent": None,
    "_new": mixintest_new
}


def square_and_mixintest_new(name, side, property1):
    return make(MixinTest, name, property1) | \
           make(Square, name, side) | {
               "side": side,
               "_class": SquareAndMixinTest
           }


# Properties of the Square 'class'.
SquareAndMixinTest = {
    "_classname": "SquareAndMixinTest",
    "_parent": [Square, MixinTest],
    "_new": square_and_mixintest_new
}


def test_initial():
    examples = [make(Square, "sq", 3), make(Circle, "ci", 2)]
    for ex in examples:
        n = ex["name"]
        d = call(ex, "density", 5)
        print(f"{n}: {d:.2f}")


def test_method_found_in_object_has_priority(monkeypatch):

    monkeypatch.setitem(Square, "area", lambda thing: 1)

    examples = [make(Square, "sq", 3)]
    for ex in examples:
        n = ex["name"]
        d = call(ex, "density", 5)
        if type(ex) == Square:
            assert d == 1


def test_square_and_mixin_test():
    c = make(SquareAndMixinTest, "sq", 3, 2)
    area = call(c, "area")
    assert area == 9
    property1 = call(c, "property1")
    assert property1 == 2


def test_call_nonexistant_method_raises_exception():
    c = make(SquareAndMixinTest, "sq", 3, 2)
    with pytest.raises(NotImplementedError):
        res = call(c, "ministry_of_nonexistent_methods")