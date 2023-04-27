def clone(thing):
    return thing | {"_parent": thing}


def find(thing, method_name):
    if thing is None:
        raise NotImplementedError("method_name")
    if method_name in thing:
        return thing[method_name]
    return find(thing["_parent"], method_name)


def call(thing, method_name, *args):
    method = find(thing, method_name)
    return method(thing, *args)


# empty object that everything will be cloned from.
object = {}


def shape_density(thing, weight):
    return weight / call(thing, "area")


shape = clone(object)
shape["name"] = "shape1"
shape["density"] = shape_density

print(shape)
print(shape["_parent"])

print(id(object))
print(id(shape["_parent"]))


def square_perimeter(thing):
    return 4 * thing["side"]


def square_area(thing):
    return thing["side"] ** 2


square = clone(shape)
square["name"] = "sq"
square["perimeter"] = square_perimeter
square["area"] = square_area
square["side"] = 3

print(
    f"{square['name']}: area: {call(square, 'area')} perimeter: {call(square, 'perimeter')} density: {call(square, 'density', 5)}"
)

red_square = clone(square)
red_square["name"] = "rsq"
red_square["colour"] = "red"

print(
    f"{red_square['name']}: area: {call(red_square, 'area')} perimeter: {call(red_square, 'perimeter')} density: {call(red_square, 'density', 5)} colour: {red_square['colour']}"
)

# I think prototypes are a bit harder to understand, but I'm much more
# familiar with classes than prototypes.
# It does seem to be a potential source of confusion that you clone
# the data along with the methods. Classes force you to change that data.
