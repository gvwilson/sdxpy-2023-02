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
    for parent in cls["_parents"]:
        method = find(parent, method_name)
        if method is not None:
            return method
    return None

def call(thing, method_name, *args):
    """Call a method."""
    if method_name in list(thing.keys()):
        if callable(thing[method_name]):
            method = thing[method_name]
            return method(*args)
        else:
            return thing[method_name]
    else:
        method = find(thing["_class"], method_name)
        if method is None:
            raise NotImplementedError(method_name)
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
    "_parents": None,
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
    return make(Shape, name) | {
        "side": side,
        "_class": Square
    }

# Properties of the Square 'class'.
Square = {
    "perimeter": square_perimeter,
    "area": square_area,
    "_classname": "Square",
    "_parents": [Shape],
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
    return make(Shape, name) | {
        "radius": radius,
        "_class": Circle
    }

def square_opinion(thing):
    """An opinion."""
    return "It's hip to be square."

# Properties of the Circle 'class'.
Circle = {
    "perimeter": circle_perimeter,
    "area": circle_area,
    "_classname": "Circle",
    "_parents": [Shape],
    "_new": circle_new,
    "opinion": square_opinion
}

# ----------------------------------------------------------------------
# The Amorphus Blob class (derived from Shape, but parented by both Circle and Square).
# ----------------------------------------------------------------------

def amorphus_blob_new(name, radius, side):
    return make(Shape, name) | {
        "_class": Amorphus_Blob,
        "radius": radius,
        "side": side
        }

Amorphus_Blob = {
    "_classname": "Blob",
    "_new": amorphus_blob_new,
    "_parents": [Circle, Square]
}

# ----------------------------------------------------------------------
# Examples of all of this in action.
# ----------------------------------------------------------------------

examples = [make(Square, "sq", 3), make(Circle, "ci", 2), make(Amorphus_Blob, "Bob", 6, 7)]
for ex in examples:
    n = ex["name"]
    d = call(ex, "density", 5)
    print(f"{n}: {d:.2f}")

call(examples[2], "perimeter") # Seems to use Circle...
call(examples[2], "area") # Also seems to use Circle... I guess it's because it's the first one it finds?
call(examples[2], "opinion") # I made a new class specific to Square and it finds it. Good enough!
