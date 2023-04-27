import math
from copy import deepcopy

# ----------------------------------------------------------------------
# Functions implementing the prototype system.
# ----------------------------------------------------------------------

def clone(thing):
    new_thing = deepcopy(thing)
    new_thing["_parent"] = thing
    return new_thing

def find(thing, method_name):
    if thing is None:
        raise NotImplementedError(method_name)
    if method_name in thing:
        return thing[method_name]
    return find(thing["_parent"], method_name)

def call(thing, method_name, *args):
    method = find(thing, method_name)
    return method(thing, *args)

# ----------------------------------------------------------------------
# The generic Shape prototype.
# ----------------------------------------------------------------------

def shape_density(thing, weight):
    """Calculate the density of a generic shape."""
    return weight / call(thing, "area")

Shape = {
    "name": None,
    "density": shape_density,
    "_classname": "Shape",
    "_parent": None
}

# ----------------------------------------------------------------------
# The Square prototype (cloned from Shape).
# ----------------------------------------------------------------------

def square_perimeter(thing):
    """Perimeter of a square."""
    return 4 * thing["side"]

def square_area(thing):
    """Area of a square."""
    return thing["side"] ** 2

Square = clone(Shape) | {
    "perimeter": square_perimeter,
    "area": square_area,
    "side": None,
    "_classname": "Square"
}

# ----------------------------------------------------------------------
# The Circle prototype (cloned from Shape).
# ----------------------------------------------------------------------

def circle_perimeter(thing):
    """Perimeter of a circle."""
    return 2 * math.pi * thing["radius"]

def circle_area(thing):
    """Area of a circle."""
    return math.pi * thing["radius"] ** 2

# Properties of the Circle 'class'.
Circle = clone(Shape) | {
    "perimeter": circle_perimeter,
    "area": circle_area,
    "radius": None,
    "_classname": "Circle",
}

# ----------------------------------------------------------------------
# Examples of all of this in action.
# ----------------------------------------------------------------------

sq = clone(Square)
sq["name"] = "sq"
sq["side"] = 3

ci = clone(Circle)
ci["name"] = "ci"
ci["radius"] = 2

examples = [sq, ci]
for ex in examples:
    n = ex["name"]
    d = call(ex, "density", 5)
    print(f"{n}: {d:.2f}")
