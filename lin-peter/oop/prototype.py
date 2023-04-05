import math

# ----------------------------------------------------------------------
# Functions implementing the object system.
# ----------------------------------------------------------------------

my_class = []

def make(cls, *args):
    """Make a new 'class'."""
    # if class already exists, make a clone
    if type(cls) is dict and cls in my_class:
        return clone(cls, *args)
    # if class is new, add it to class array
    my_class.append(cls["_new"](*args))
    return my_class[-1]

def clone(cls, *args):
    """Make an 'clone' of a 'class'."""
    # if cloning from an existing class
    cloned_object = cls.copy()
    return cloned_object["_new"](*args)

def find(thing, method_name):
    """Find a method in my_class list."""
    if thing is None:
        raise NotImplementedError("method_name")
    if method_name in thing.keys():
        return thing[method_name]
    return find(thing["_parent"], method_name)

def call(thing, method_name, *args):
    """Call a method."""
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
    return weight / call(thing, "volume") if "volume" in thing["_class"] else weight / call(thing, "area")

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
    return clone(Shape, name) | {
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
    return clone(Shape, name) | {
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
# The Cube class (derived from Square).
# ----------------------------------------------------------------------

def cube_new(name, side):
    """Construct a cube (a Shape with extra/overridden properties)."""
    return clone(Shape, name) | {
        "side": side,
        "_class": Cube
    }

def cube_volume(thing):
    """Volume of a cube."""
    return thing["side"]**3

# Properties of the Cube 'class'.
Cube = {
    "volume": cube_volume,
    "_classname": "Cube",
    "_parent": Square,
    "_new": cube_new
}

# ----------------------------------------------------------------------
# Examples of all of this in action.
# ----------------------------------------------------------------------

examples = [make(Square, "sq", 3), make(Circle, "ci", 2), make(Cube, "cu", 4)]
for ex in examples:
    n = ex["name"]
    d = call(ex, "density", 5)
    print(f"{n}: {d:.2f}")


