import math

# ----------------------------------------------------------------------
# Functions implementing the object system.
# ----------------------------------------------------------------------

def make(cls, *args):
    """Make an 'instance' of a 'class'."""
    return cls["_new"](*args)

def find(cls, thing, method_name):
    """Find a method."""
    if method_name in thing:
        return thing[method_name]

    if cls is None:
        raise NotImplementedError(method_name)
    if method_name in cls:
        return cls[method_name]
    for parent in cls["_parent"]:
        try:
            return find(parent, thing, method_name)
        except NotImplementedError:
            pass
    raise NotImplementedError(method_name)

def call(thing, method_name, *args):
    """Call a method."""
    method = find(thing["_class"], thing, method_name)
    return method(thing, *args)

# ----------------------------------------------------------------------
# The generic Wristwatch class.
# ----------------------------------------------------------------------

def wristwatch_new():
    """Build a generic wristwatch."""
    return {
        "_class": Wristwatch
    }

def wristwatch_time(thing):
    return "2 pm"
    
# Properties of the Wristwatch 'class'.
Wristwatch = {
    "time": wristwatch_time,
    "_classname": "Wristwatch",
    "_parent": [None],
    "_new": wristwatch_new
}

def digitalwristwatch_new():
    """Construct a DigitalWristwatch (no overridden properties)."""
    return make(Wristwatch)

def digitalwristwatch_time(thing):
    return "14:00"

# Properties of the DigitalWristwatch 'class'.
DigitalWristwatch = {
    "time": digitalwristwatch_time,
    "_classname": "DigitalWristwatch",
    "_parent": [Wristwatch],
    "_new": digitalwristwatch_new
}

def analogwristwatch_new():
    """Construct a AnalogWristwatch (no overridden properties)."""
    return make(Wristwatch)

def analogwristwatch_time(thing):
    return "🕑"

# Properties of the AnalogWristwatch 'class'.
AnalogWristwatch = {
    "time": analogwristwatch_time,
    "_classname": "AnalogWristwatch",
    "_parent": [Wristwatch],
    "_new": analogwristwatch_new
}

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

def square_new(name, side):
    """Construct a square (a Shape with extra/overridden properties)."""
    return (make(Shape, name)
            | make(DigitalWristwatch)
            | {
                "side": side,
                "_class": Square
            })

# Properties of the Square 'class'.
Square = {
    "perimeter": square_perimeter,
    "area": square_area,
    "_classname": "Square",
    "_parent": [Shape, DigitalWristwatch],
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
    return (make(Shape, name)
            | make(AnalogWristwatch)
            | {
                "radius": radius,
                "_class": Circle
            })

# Properties of the Circle 'class'.
Circle = {
    "perimeter": circle_perimeter,
    "area": circle_area,
    "_classname": "Circle",
    "_parent": [Shape, AnalogWristwatch],
    "_new": circle_new
}

# ----------------------------------------------------------------------
# Examples of all of this in action.
# ----------------------------------------------------------------------

def surface_density(thing, weight):
    """Calculate the density of a generic shape."""
    return weight / call(thing, "perimeter")

examples = [make(Square, "sq", 3), make(Circle, "ci1", 3), make(Circle, "ci2", 3)]
examples[1]["density"] = surface_density

for ex in examples:
    # print(ex)
    n = ex["name"]
    d = call(ex, "density", 5)
    t = call(ex, "time")
    print(f"{n}: {d:.2f} @ {t}")
