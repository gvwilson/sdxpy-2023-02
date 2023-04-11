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
    for parent in cls["_parent"]: # use a list to implement multiple inheritance
        try: 
            return find(parent, method_name) # look sequentially
        except:
            pass
    raise NotImplementedError("method_name")
    #return find(cls["_parent"], method_name)

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
    return weight / call(thing, "area")

# Properties of the Shape 'class'.
Shape = {
    "density": shape_density,
    "_classname": "Shape",
    #"_parent": None,
    "_parent": [None],
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

# adding method to test implmentation
def square_volume(thing):
    """Volume of a square box."""
    return thing["side"] ** 3

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
    "volume": square_volume,
    "_classname": "Square",
    #"_parent": Shape,
    "_parent": [Shape],
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

# adding method to test implementation
def circle_diameter(thing):
    """Diameter of a circle."""
    return thing["radius"] * 2

def circle_new(name, radius):
    """Construct a circle (a Shape with extra/overridden properties)."""
    return make(Shape, name) | {
        "radius": radius,
        "_class": Circle
    }

# Properties of the Circle 'class'.
Circle = {
    "perimeter": circle_perimeter,
    "area": circle_area,
    "diameter": circle_diameter, 
    "_classname": "Circle",
    #"_parent": Shape,
    "_parent": [Shape],
    "_new": circle_new
}

# ----------------------------------------------------------------------
# The Squircle class (derived from Shape).
# ----------------------------------------------------------------------

def squircle_new(name, side, radius):
    """Construct a Squircle (a Shape with extra/overridden properties)."""
    return make(Shape, name) | {
        "radius": radius,
        "side": side,
        "_class": Squircle
    }

# Properties of the Squircle 'class'.
Squircle = {
    "_classname": "Squircle",
    "_parent": [Square, Circle],
    "_new": squircle_new
}

# ----------------------------------------------------------------------
# Examples of all of this in action.
# ----------------------------------------------------------------------

squircle = make(Squircle, "sqcl", 3, 2)
call(squircle, "diameter") # should look in Circle 
call(squircle, "volume") # should look in Volume 
call(squircle, "circumference") # should raise an exception 
