import math
from copy import deepcopy
# ----------------------------------------------------------------------
# Functions implementing the object system.
# ----------------------------------------------------------------------

def clone(thing, new_attrs):
    """Clone a new object from an existing one."""
    new_thing = deepcopy(thing)
    new_thing["_parent"] = thing
    for k, v in new_attrs.items():
        new_thing[k] = v    
    
    return new_thing

def find(thing, method_name):
    """Find a method."""
    if method_name not in thing:
        raise NotImplementedError("method_name:", thing["_name"], method_name)
    return thing[method_name]

def call(thing, method_name, *args):
    """Call a method."""
    method = find(thing, method_name)
    return method(thing, *args)


# ----------------------------------------------------------------------
# Examples of all of this in action.
# ----------------------------------------------------------------------

def shape_density(thing, weight):
    """Calculate the density of a generic shape."""
    return weight / call(thing, "area")

shape = {
    "density": shape_density,
    "_name": "Shape",
    "_parent": None
}

def square_perimeter(thing):
    """Perimeter of a square."""
    return 4 * thing["side"]

def square_area(thing):
    """Area of a square."""
    return thing["side"] ** 2

Square = {
    "perimeter": square_perimeter,
    "area": square_area,
    "_name": "Square",
}



def circle_perimeter(thing):
    """Perimeter of a circle."""
    return 2 * math.pi * thing["radius"]

def circle_area(thing):
    """Area of a circle."""
    return math.pi * thing["radius"] ** 2


Circle = {
    "perimeter": circle_perimeter,
    "area": circle_area,
    "_name": "Circle",
}

square = clone(shape, Square)
circle = clone(shape, Circle)

examples = [clone(square, {"_name":"sq", "side":3}), clone(circle, {"_name":"ci", "radius":2})]
for ex in examples:
    n = ex["_name"]
    d = call(ex, "density", 5)
    print(f"{n}: {d:.2f}")