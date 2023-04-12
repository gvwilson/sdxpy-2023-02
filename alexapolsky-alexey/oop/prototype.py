from start import *


def clone(obj, **kwargs):
    return obj.copy() | {'_parent': obj} | kwargs


def find(thing, method_name):
    """Find a method."""
    if thing is None:
        raise NotImplementedError(method_name)
    if method_name in thing:
        return thing[method_name]
    return find(thing["_parent"], method_name)


def call(thing, method_name, *args):
    """Call a method."""
    method = find(thing, method_name)
    if not callable(method):
        return method
    return method(thing, *args)



def test_clone():

    Square = {
        "side": None,
        "perimeter": square_perimeter,
        "area": square_area,
        "_classname": "Square",
        "_parent": None,
        "_new": square_new,
    }

    square_clone = clone(Square)
    assert Square == square_clone

    square_clone2 = clone(Square, side=2)
    assert square_clone2.get("side") == 2


def test_find():

    Square = {
        "side": None,
        "perimeter": square_perimeter,
        "area": square_area,
        "_classname": "Square",
        "_parent": None,
        "_new": square_new
    }
    square_clone2 = clone(Square, side=2)


def test_call():

    Square = {
        "side": None,
        "perimeter": square_perimeter,
        "area": square_area,
        "_classname": "Square",
        "_parent": None,
        "_new": square_new,
        "double_num": lambda thing, x: x * 2

    }
    square_clone2 = clone(Square, side=2)
    res = call(square_clone2, "double_num", 1)
    print(res)


def test_call_inheritance():

    """
    Question: Do you find prototypes easier
    or harder to understand than classes?
    Answer:
        1) Prototypes seem to consume more memory.
        2) Multiple inheritance may cause name conflict if both parents have the same prop
        3) Identity of class becomes a problem, how to verify is_instance(Prototype, object) ?
        4) Dynamic change of parent attrs/methods in prototype also may require some explicit synchronization
        in cloned children
    :return:
    """

    Square = {
        "side": None,
        "perimeter": square_perimeter,
        "area": square_area,
        "_classname": "Square",
        "_parent": None,
        "_new": square_new,
        "double_num": lambda thing, x: x * 2

    }
    square_clone2 = clone(Square, side=2)
    square_clone3 = clone(square_clone2)
    print(square_clone2)
    print(square_clone3)