from collections import ChainMap


def env_get(env, name):
    # This is simplified by using a ChainMap,
    # no need to check first and last dicts
    assert name in env.keys(), f"Unknown variable {name}"
    return env[name]


# This seems redundant with env_get,
# but it seems simple enough that it doesn't matter?
def env_get_array(env, name):
    assert name in env.keys() and isinstance(
        env[name], list), f"Unknown array {name}"
    return env[name]


def env_set(env, name, value):
    env[name] = value
    return value


def run_add(env, args):
    left, right = args[0], args[1]
    return run(env, left) + run(env, right)


def check_index(array, index):
    assert isinstance(index, int)
    assert index < len(array), (f"Index {index} out of bounds for "
                                f"array of length {len(array)}")


def run_array(env, args):
    assert len(args) == 1
    numel = args[0]
    assert isinstance(numel, int)
    return [0] * numel


def run_call(env, args):
    assert len(args) >= 1
    name = args[0]
    func = env_get(env, name)
    assert func[0] == "func", f"Unknown function {name}"
    params = func[1]
    body = func[2]
    assert len(args[1:]) == len(params), (f"{name} takes {len(func[1])}"
                                          f"arguments, but {len(args[1])}"
                                          "were provided")
    local_env = {}
    for arg, param in zip(args[1:], params):
        # Run with default env before passing to set
        run_set(local_env, [param, run(env, arg)])
    return run(ChainMap(local_env, env), body)


def run_def(env, args):
    assert len(args) == 3
    name = args[0]
    params = args[1]
    body = args[2]
    env_set(env, name, ["func", params, body])
    return None


def run_get(env, args):
    # For getting array entries:
    # ["get", "var", i]
    if len(args) == 2:
        name = args[0]
        array = env_get_array(env, name)
        index = run(env, args[1])
        check_index(array, index)
        return array[index]
    # For getting a variable
    # ["get", "var"]
    elif len(args) == 1:
        name = args[0]
        return env_get(env, name)
    else:
        assert False, f"Expected 1 or 2 arguments, {len(args)} given"


def run_if(env, args):
    cond = args[0]
    if_true = args[1]
    if_false = args[2]
    if run(env, cond):
        return run(env, if_true)
    else:
        return run(env, if_false)


def run_mul(env, args):
    left, right = args[0], args[1]
    return run(env, left) * run(env, right)


def run_seq(env, args):
    result = None
    for expression in args:
        result = run(env, expression)
    return result


def run_set(env, args):
    # For setting array entry:
    # ["set", "var", i, value]
    if len(args) == 3:
        name = args[0]
        array = env_get_array(env, name)
        index = run(env, args[1])
        check_index(array, index)
        value = run(env, args[2])
        assert isinstance(value, int), "Arrays can only have integer values"
        array[index] = value
    # For setting variable:
    # ["set", "var", value]
    elif len(args) == 2:
        name = args[0]
        value = run(env, args[1])
        env[name] = value
    else:
        assert False, f"Expected 2 or 3 arguments, {len(args)} given"
    return value


def run_while(env, args):
    assert len(args) == 2
    cond = args[0]
    body = args[1]
    while run(env, cond):
        value = run(env, body)
    # Return last value in while loop
    return value


FUNCS = {
    name.removeprefix("run_"): func
    for (name, func) in globals().items() if name.startswith("run_")
}


# dispatch function, finds operation and dispatches it to proper function
def run(env, expr):
    if isinstance(expr, int):
        return expr
    op = expr[0]
    args = expr[1:]
    assert op in FUNCS, f"Unknown operation {op}"
    func = FUNCS[op]
    return func(env, args)


program = [
    "seq",
    ["set", "test", 1],
    ["set", "other", 2],
    [
        "add",
        ["get", "test"],
        ["mul", ["get", "other"], 3]
    ]
]
# print(run({}, program))
test_if = ["if", 0, 100, -100]


# This tests recursion
test_factorial = [
    "seq",
    ["set", "num", 2],
    ["def", "factorial", ["num"],
     ["if", ["get", "num"],
      ["mul", ["get", "num"],
       ["call", "factorial",
            ["add", ["get", "num"], -1]
        ]
       ],
      1,
      ]
     ],
    ["def", "add_one", ["num"],
     ["add", ["get", "num"], 1]
     ],
    ["call", "factorial",
     ["call", "add_one", ["get", "num"]]
     ]
]

# This tests whether functions can access global variables
test_global_non_local_variable = [
    "seq",
    ["def", "needs_a", ["b"],
     # return a + b
     ["add", ["get", "a"], ["get", "b"]]
     ],
    ["set", "a", 4],  # a = 4
    ["call", "needs_a", 2]  # 4 + 2 = 6
]

# This tests whether functions can access variables that are defined by an
# earlier function call, but are not global
test_non_global_non_local_variable = [
    "seq",
    ["def", "needs_a", ["b"],
     # return a + b
     ["add", ["get", "a"], ["get", "b"]]
     ],
    ["def", "add_num_b", ["num", "b"],
     # a = num, return needs_a(b)
     ["seq",
      ["set", "a", ["get", "num"]],
      ["call", "needs_a", ["get", "b"]]
      ]
     ],
    ["call", "add_num_b", 4, 2]  # 4 + 2 = 6
]


test_func = [
    "seq",
    ["set", "a", 5],
    ["set", "b", 3],
    ["def", "self", ["val"], ["get", "val"]],
    ["call", "self",
     ["add",
      ["get", "a"],
      ["get", "b"]
      ]
     ]
]


test_array = [
    "seq",
    ["set", "a", ["array", 3]],  # a = int[3]
    ["set", "a", 0, 1],  # a[0] = 1
    ["set", "a", 1, 2],  # a[1] = 2
    ["set", "a", 2,  # a[2] = a[0] + a[1]
     ["add",
      ["get", "a", 0],
      ["get", "a", 1]
      ]
     ],
    ["get", "a",
     ["add", 4, -2]]  # a[4 - 2]
]


test_while = [
    "seq",
    ["set", "x", 5],  # x = 5
    ["set", "y", 1],  # y = 1
    ["while", ["get", "x"],  # while x > 0
     ["seq",
      ["set", "x", ["add", ["get", "x"], -1]],  # x -= 1
      ["set", "y", ["mul", ["get", "y"], 2]]  # y *= 2
      ]
     ],
    ["get", "y"]  # y should be 2^5 = 32
]


print(run({}, test_while))
