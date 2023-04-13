import math

from copy import deepcopy


def clone(thing):
    new_thing = deepcopy(thing)
    new_thing["_parent"].append(thing)
    return new_thing


def find(thing, method_name):
    search_stack = [thing] + thing['_parent'][::-1]
    for obj in search_stack:
        if method_name in obj:
            return obj[method_name]
    raise AttributeError(f"{thing} has no attribute/method {method_name}")


def call(thing, method_name, *args):
    method = find(thing, method_name)
    return method(thing, *args)


UrPrototype = dict(_parent=[])


# Shape "class"
def shape_density(thing, weight):
    """Calculate the density of a generic shape."""
    return weight / call(thing, "area")


def shape_new(name):
    """Build a generic shape."""
    shape = clone(UrPrototype)
    shape['name'] = name
    shape['density'] = shape_density
    return shape


# Square "class"
def square_perimeter(thing):
    """Perimeter of a square."""
    return 4 * thing["side"]


def square_area(thing):
    """Area of a square."""
    return thing["side"] ** 2


def square_new(name, side):
    """Construct a square (a Shape with extra/overridden properties)."""
    square = clone(shape_new(name))
    square["side"] = 3
    square["perimeter"] = square_perimeter
    square["area"] = square_area
    return square


# Circle "class"
def circle_perimeter(thing):
    """Perimeter of a circle."""
    return 2 * math.pi * thing["radius"]


def circle_area(thing):
    """Area of a circle."""
    return math.pi * thing["radius"] ** 2


def circle_new(name, radius):
    """Construct a circle (a Shape with extra/overridden properties)."""
    circle = clone(shape_new(name))
    circle["radius"] = radius
    circle["perimeter"] = circle_perimeter
    circle["area"] = circle_area
    return circle


# Color "class"
def color_get(thing):
    return find(thing, "color")


def color_new(color):
    _color = clone(UrPrototype)
    _color["color_get"] = color_get
    _color["color"] = color
    return _color


# pseudo-tests
a_circle = circle_new("ci", 2)
a_square = square_new("sq", 3)
a_color = color_new("red")

zero_density_square = clone(a_square)
zero_density_square["density"] = lambda thing, weight: 0

a_red_square = clone(a_square)
a_red_square["name"] = "rsq"
a_red_square["_parent"].append(a_color)

examples = [zero_density_square,
            a_circle,
            a_square,
            a_red_square]
for ex in examples:
    n = ex["name"]
    d = call(ex, "density", 5)
    try:
        c = call(ex, "color_get")
    except AttributeError:
        c = "colorless"
    print(f"{n}: {d:.2f}, {c}")
