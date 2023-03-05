from collections import ChainMap

prog = [
    "seq",
    ["def", "double", ["num"], ["add", ["get", "num"], ["get", "num"]]],
    ["set", "arrb", ["array", 21]],
    ["set_element", ["get", "arrb"], 20, 1],
    ["set", "c", 20],
    [
        "while",
        ["get", "c"],
        [
            "seq",
            ["set", "x", ["get", "c"]],
            ["set", "c", ["decrement", ["get", "c"]]],
            [
                "set_element",
                ["get", "arrb"],
                ["get", "c"],
                ["call", "double", ["get_element", ["get", "arrb"], ["get", "x"]]],
            ],
        ],
    ],
    ["get", "arrb"],
]


def do(env, expr):
    # Integers evaluate to themselves.
    if isinstance(expr, int):
        return expr
    # Lists trigger function calls.
    assert isinstance(expr, list)
    assert expr[0] in OPS, f"Unknown operation {expr[0]}"
    func = OPS[expr[0]]
    return func(env, expr[1:])


def do_add(env, expr):
    assert len(expr) == 2
    left = do(env, expr[0])
    right = do(env, expr[1])
    return left + right


def do_decrement(env, expr):
    assert len(expr) == 1
    left = do(env, expr[0])
    return left - 1


def do_abs(env, args):
    assert len(args) == 1
    val = do(env, args[0])
    return abs(val)


# ["get", "name"]
def do_get(env, args):
    assert len(args) == 1
    assert isinstance(args[0], str)
    assert args[0] in env, f"Unknown variable {args[0]}"
    return env[args[0]]


# ["set", "name", …expression…]
def do_set(env, args):
    assert len(args) == 2
    assert isinstance(args[0], str)
    value = do(env, args[1])
    env[args[0]] = value
    return value


def do_seq(env, args):
    assert len(args) > 0
    for item in args:
        result = do(env, item)
    return result


def env_get(env: ChainMap, name):
    assert isinstance(name, str)
    if name in env.maps[-1]:
        return env.maps[-1][name]
    if name in env.maps[0]:
        return env.maps[0][name]
    assert False, f"Unknown variable {name}"


def env_set(env, name, value):
    assert isinstance(name, str)
    env[name] = value


def do_def(env, args):
    assert len(args) == 3
    name = args[0]
    params = args[1]
    body = args[2]
    env_set(env, name, ["func", params, body])
    return None


def do_call(env: ChainMap, args):
    # Set up the call.
    assert len(args) >= 1
    name = args[0]
    values = [do(env, a) for a in args[1:]]
    # Find the function.
    func = env_get(env, name)
    assert isinstance(func, list) and (func[0] == "func")
    params, body = func[1], func[2]
    assert len(values) == len(params)
    # Run in new environment.
    result = do(env.new_child(m=dict(zip(params, values))), body)
    return result


def do_array(env, args):
    assert len(args) == 1
    assert isinstance(args[0], int) and 0 < args[0]
    return [None for i in range(args[0])]


def do_get_element(env, args):
    assert len(args) == 2
    array = do(env, args[0])
    index = do(env, args[1])
    assert isinstance(array, list)
    assert isinstance(index, int)
    assert 0 <= index < len(array), f"Index out of range: {index}"
    return array[index]


def do_set_element(env, args):
    assert len(args) == 3
    array = do(env, args[0])
    index = do(env, args[1])
    value = do(env, args[2])
    assert isinstance(array, list)
    assert isinstance(index, int)
    assert 0 <= index < len(array), f"Index out of range: {index}"
    array[index] = value
    return value


# 0 is (the only) false
# returns what the last evaluation of the body returns
def do_while(env, args):
    assert len(args) == 2
    last = None
    while True:
        cond = do(env, args[0])
        assert isinstance(
            cond, int
        ), "that's a-crazy condition - i only know the int world"
        if not cond:
            return last
        else:
            last = do(env, args[1])


OPS = {
    name.replace("do_", ""): func
    for (name, func) in globals().items()
    if name.startswith("do_")
}

print(do(ChainMap(), prog))
