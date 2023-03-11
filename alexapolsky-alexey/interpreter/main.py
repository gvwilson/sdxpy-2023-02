from collections import ChainMap


def run_add(env, args):
    left, right = args[0], args[1]
    return run(env, left) + run(env, right)


# env is short for environment
# getenv - get value of environment variable
def env_get(env, name):

    assert isinstance(name, str)
    if name in env:
        return env[name]
    assert False, f"Unknown variable {name}"


def run_get(env, args):
    """Return the stored value of the variable
    in global environment.
    """
    assert len(args) == 1
    return env_get(env, args[0])


def env_set(env, name, value):
    assert isinstance(name, str)
    env[name] = value


def run_mul(env, args):
    left, right = args[0], args[1]
    return run(env, left) * run(env, right)


def run_decrement(env, args):
    return run(env, args[0]) - run(env, args[1])


def run_seq(env, args):
    result = None
    for expression in args:
        result = run(env, expression)
    return result


def run_print(env, args):
    print(f'{",".join(args)}')


def run_set(env, args):
    assert len(args) == 2
    name = args[0]
    value = run(env, args[1])
    env_set(env, name, value)
    return value


# ["if", [...cond...], [...iftrue...], [...iffalse..]]
# lazy evaluation
# eager evaluation -- run the expression in args[1], args[2] before eval cond.
# lazy evaluation -- allows using if for testing if it is save to evaluate an expression
def run_if(env, args):
    cond = args[0]
    if_true = args[1]
    if_false = args[2]
    if run(env, cond):
        return run(env, if_true)
    else:
        return run(env, if_false)


def run_array(env, args):
    """
    :param env: env
    :param args: number of items in array
    :return: array of [None, None ...] kind
    """
    return [None] * args[0]


def run_setx_array(env, args):
    """
    :param env:
    :param args: arg[0] array, arg[1] index, arg[2] value
    :return: value
    """
    array = run(env, ["get", args[0]])
    index = args[1]
    value = args[2]
    array[index] = value
    return value


def run_getx_array(env, args):
    """
    :param env:
    :param args: arg[0] array, arg[1] index
    :return: value
    """
    array = run(env, ["get", args[0]])
    index = args[1]
    return array[index]


def run_while(env, args, limit=10):
    cond = args[0]
    counter = 1
    while cond and counter < limit:
        run(env, args[1])
        counter += 1


def run_def(env, args):
    """Define a new function.
    ["def" name [...params...] body] => None # and define function
    """
    assert len(args) == 3
    name = args[0]
    params = args[1]
    body = args[2]
    env_set(env, name, ["func", params, body])
    return None


def run_call(env, args):
    """Call a function.
    ["call" name ...expr...] => env[name](*expr)
    """
    # Set up the call.

    # Set up the call.
    assert len(args) >= 1
    name = args[0]
    values = [run(env, a) for a in args[1:]]
    # Find the function.
    func = env_get(env, name)
    assert isinstance(func, list) and (func[0] == "func")
    params, body = func[1], func[2]
    assert len(values) == len(params)
    # Run in new environment.
    env = env.new_child(dict(zip(params, values)))
    result = run(env, body)
    # Report.
    return result


# could loop over globals to get all functions starting with run_
FUNCS = {
    name.replace("run_", ""): func
    for (name, func) in globals().items()
    if name.startswith("run_")
}


# dispatch
def run(env, expr):
    if isinstance(expr, int):
        return expr
    op = expr[0]
    args = expr[1:]
    assert op in FUNCS, f"Unknown operation {op}"
    func = FUNCS[op]
    return func(env, args)


stuff = {"reiko": 1, "alex": 2}


# get/set tests

program = [
    "seq",
    ["set", "reiko", 1],
    ["set", "alex", 2],
    ["add", ["get", "reiko"], ["mul", ["get", "alex"], 3]],
]


program = [
    "seq",
    ["def", "double", ["num"], ["add", ["get", "num"], ["get", "num"]]],
    ["set", "small_x", 5],
    ["call", "double", ["get", "small_x"]],
]


# tests for if functions and nesting function statements one into another
program = ["seq", ["if", False, 1, 2]]

program = [
    "seq",
    ["def", "func_with_if", ["x"], ["if", ["get", "x"], 1, 2]],
    ["set", "x", False],
    ["call", "func_with_if", ["get", "x"]],
]

# Experiment with for function/iteration using recursion
program = [
    "seq",
    ["print", "staring...."],
    [
        "def",
        "repeat",
        ["x"],
        [
            "seq",
            ["print", "in loop"],
            #  experimenting with for loop implemented as recursion, looks good
            ["if", ["get", "x"], ["call", "repeat", ["decrement", ["get", "x"], 1]], 0],
        ],
    ],
    ["set", "x", 2],
    ["call", "repeat", ["get", "x"]],
]

# Array functions setx_array, getx_array
program = [
    "seq",
    ["print", "123"],
    ["set", "var", ["array", 10]],
    ["setx_array", "var", 0, 777],
    ["get", "var"],
    ["getx_array", "var", 0],
]

# while statement/function
program = ["while", False, ["print", "this should NOT be printed"]]
program = ["while", True, ["print", "iteration in while"]]


print(run(ChainMap(stuff), program))
