def clone(thing):
    return thing | {"_parent": thing}


def find(thing, method_name):
    if thing is None:
        raise NotImplementedError("method_name")
    if method_name in thing:
        return thing["method_name"]
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
