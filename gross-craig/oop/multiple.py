import math

# ----------------------------------------------------------------------
# Functions implementing the object system.
# ----------------------------------------------------------------------

def make(cls, *args):
    """Make an 'instance' of a 'class'."""
    return cls["_new"](*args)

def find_internal(cls, method_name):
    """Find a method."""
    if method_name in cls:
        return cls[method_name]
    for parent_cls in cls["_parent"]:
        method = find_internal(parent_cls, method_name)
        if method:
            return method
    return None

def find(cls, method_name):
    """Search class for method or throw exception if does not exist."""
    method = find_internal(cls, method_name)
    if not method:
        raise NotImplementedError(method_name)
    return method

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

def shape_equals(thing, other):
    return thing["name"] == other["name"]

# Properties of the Shape 'class'.
Shape = {
    "density": shape_density,
    "equals": shape_equals,
    "_classname": "Shape",
    "_parent": [],
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

def square_equals(thing, other):
    return thing["side"] == other["side"]

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
    "equals": square_equals,
    "_classname": "Square",
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
    "_classname": "Circle",
    "_parent": [Shape],
    "_new": circle_new
}

# ----------------------------------------------------------------------
# The Colorable class
# ----------------------------------------------------------------------

def colorable_appearance(thing):
    return f"{thing['shade']} {thing['color']}"

def colorable_equals(thing, other):
    return thing['color'] == other['color'] and \
            thing['color'] == other['color']

def colorable_new(color, shade):
    return {
        "color": color,
        "shade": shade,
        "_class": Colorable
    }

Colorable = {
    "appearance": colorable_appearance,
    "equals": colorable_equals,
    "_classname": "Colorable",
    "_parent": [],
    "_new": colorable_new
}

# ----------------------------------------------------------------------
# The ColorableSquare class (inherits from Colorable and Square)
# ----------------------------------------------------------------------

def colorable_square_new(name, color, shade, side):
    return make(Colorable, color, shade) | make(Square, name, side) | {
        "_class": ColorableSquare
    }

def colorable_square_paint(thing):
    area = call(thing, "area")
    appearance = call(thing, "appearance")
    print(f"I need {area} square units of {appearance} paint")

ColorableSquare = {
    "paint": colorable_square_paint,
    "_classname": "ColorableSquare",
    "_parent": [Colorable, Square],
    "_new": colorable_square_new
}

# ----------------------------------------------------------------------
# Examples of all of this in action.
# ----------------------------------------------------------------------

blue_square = make(ColorableSquare, "blue square", "blue", "light", 3)
name = blue_square["name"]
print(f"{name} appearance: {call(blue_square, 'appearance')}")
print(f"{name} area: {call(blue_square, 'area')}")
print(f"{name} density: {call(blue_square, 'density', 5)}")
call(blue_square, "paint")

bigger_blue_square = make(ColorableSquare, "bigger blue square", "blue",
                          "light", 4)
name = bigger_blue_square["name"]
print(f"{name} appearance: {call(bigger_blue_square, 'appearance')}")
print(f"{name} area: {call(bigger_blue_square, 'area')}")
call(bigger_blue_square, "paint")

red_square = make(ColorableSquare, "red square", "red", "dark", 3)
name = red_square["name"]
print(f"{name} appearance: {call(red_square, 'appearance')}")
print(f"{name} area: {call(red_square, 'area')}")
call(red_square, "paint")

# equals only tests color rather than size (or both) since Colorable is first
# in the method resolution order and equals was not overridden in
# ColorableSquare
print(call(blue_square, "equals", bigger_blue_square))
print(call(blue_square, "equals", red_square))
