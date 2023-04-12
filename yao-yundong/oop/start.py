import math
# ----------------------------------------------------------------------
# Functions implementing the object system.
# ----------------------------------------------------------------------

def make(cls, *args):
    """Make an 'instance' of a 'class'."""
    return cls["_new"](*args)

def find(cls, method_name):
    """Find a method."""
    if cls is None:
        raise NotImplementedError("method_name")
    if method_name in cls:
        return cls[method_name]
    return find(cls["_parent"], method_name)

def call(thing, method_name, *args):
    """Call a method."""
    if method_name in thing:
        method = thing[method_name]
    else:
        method = find(thing["_class"], method_name)
    return method(thing, *args)

# ----------------------------------------------------------------------
# The generic Shape class.
# ----------------------------------------------------------------------

def shape_new(name):
    """Build a generic shape."""
    return {
        "name": name,
        "_class": Shape
    }

def shape_density(thing, weight):
    """Calculate the density of a generic shape."""
    return weight / call(thing, "area")

# Properties of the Shape 'class'.
Shape = {
    "density": shape_density,
    "_classname": "Shape",
    "_parent": None,
    "_new": shape_new
}

# ----------------------------------------------------------------------
# The Square class (derived from Shape).
# ----------------------------------------------------------------------

def square_perimeter(thing):
    """Perimeter of a square."""
    return 4 * thing["side"]

def square_area(thing):
    """Area of a square."""
    return thing["side"] ** 2

def square_new(name, side):
    """Construct a square (a Shape with extra/overridden properties)."""
    new_methods = {k:v for k,v in Square.items() if not k.startswith("_") }
    return make(Shape, name) | new_methods |  {
        "side": side,
        "_class": Square
    }

# Properties of the Square 'class'.
Square = {
    "perimeter": square_perimeter,
    "area": square_area,
    "_classname": "Square",
    "_parent": Shape,
    "_new": square_new
}

# ----------------------------------------------------------------------
# The Square class (derived from Shape).
# ----------------------------------------------------------------------

def circle_perimeter(thing):
    """Perimeter of a circle."""
    return 2 * math.pi * thing["radius"]

def circle_area(thing):
    """Area of a circle."""
    return math.pi * thing["radius"] ** 2

def circle_new(name, radius):
    """Construct a circle (a Shape with extra/overridden properties)."""
    new_methods = {k:v for k,v in Circle.items() if not k.startswith("_") }
    return make(Shape, name) | new_methods | {
        "radius": radius,
        "_class": Circle
    }

# Properties of the Circle 'class'.
Circle = {
    "perimeter": circle_perimeter,
    "area": circle_area,
    "_classname": "Circle",
    "_parent": Shape,
    "_new": circle_new
}

# ----------------------------------------------------------------------
# Examples of all of this in action.
# ----------------------------------------------------------------------

examples = [make(Square, "sq", 3), make(Circle, "ci", 2)]
for ex in examples:
    n = ex["name"]
    d = call(ex, "density", 5)
    print(f"{n}: {d:.2f}")
