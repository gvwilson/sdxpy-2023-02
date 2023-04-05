import math

# ----------------------------------------------------------------------
# Functions implementing the prototype system.
# ----------------------------------------------------------------------

def clone(thing):
    return thing.copy() | {
        "_progenitor": thing
    }

def find(thing, method_name):
    """Find a method."""
    if method_name in thing:
        return thing[method_name]

    prg = thing["_progenitor"]
    if prg is None:
        raise NotImplementedError(method_name)
    return find(prg, method_name)

def call(thing, method_name, *args):
    """Call a method."""
    method = find(thing, method_name)
    return method(thing, *args)

# ----------------------------------------------------------------------
# The generic shape prototype.
# ----------------------------------------------------------------------

def shape_density(thing, weight):
    """Calculate the density of a generic shape."""
    return weight / call(thing, "area")

shape = {
    "density": shape_density,
    "name": "shape",
    "_progenitor": None
}

# ----------------------------------------------------------------------
# The square prototype (cloned from shape).
# ----------------------------------------------------------------------

def square_perimeter(thing):
    """Perimeter of a square."""
    return 4 * thing["side"]

def square_area(thing):
    """Area of a square."""
    return thing["side"] ** 2

square = clone(shape) | {
    "side": 3,
    "name": "sq",
    "perimeter": square_perimeter,
    "area": square_area
}

# ----------------------------------------------------------------------
# The circle prototype (cloned from shape).
# ----------------------------------------------------------------------

def circle_perimeter(thing):
    """Perimeter of a circle."""
    return 2 * math.pi * thing["radius"]

def circle_area(thing):
    """Area of a circle."""
    return math.pi * thing["radius"] ** 2

circle = clone(shape) | {
    "radius": 3,
    "name": "ci",
    "perimeter": circle_perimeter,
    "area": circle_area
}

# ----------------------------------------------------------------------
# The circle boundary prototype (cloned from circle).
# ----------------------------------------------------------------------

def surface_density(thing, weight):
    """Calculate the density of a generic shape."""
    return weight / call(thing, "perimeter")

circle_clone = clone(circle) | {
    "name": "cl",
    "density": surface_density
}

# ----------------------------------------------------------------------
# Examples of all of this in action.
# ----------------------------------------------------------------------

examples = [square, circle, circle_clone]

for ex in examples:
    n = ex["name"]
    d = call(ex, "density", 5)
    print(f"{n}: {d:.2f}")
