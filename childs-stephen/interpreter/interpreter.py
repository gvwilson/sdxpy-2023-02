# 1 + (2 * 3)
# Lisp == Lots of Irritating Single Parenthsis
from collections import ChainMap


def run_add(env, args):
    left, right = args[0], args[1]
    return run(env, left) + run(env, right)


# env is short for environment
# getenv - get value of environment variable
def run_get(env, args):
    name = args[0]
    return env[name]


def run_mul(env, args):
    left, right = args[0], args[1]
    return run(env, left) * run(env, right)


def run_lt(env, args):
    left, right = args[0], args[1]
    return run(env, left) < run(env, right)


def run_gt(env, args):
    left, right = args[0], args[1]
    return run(env, left) > run(env, right)


def run_seq(env, args):
    result = None
    for expression in args:
        result = run(env, expression)
    return result


def run_repeat(env, args):
    result = None
    for i in range(args[0]):
        result = run(env, args[1])
    return result


# ["while", cond, loop]
def run_while(env, args):
    cond = args[0]
    loop = args[1]
    while run(env, cond):
        run(env, loop)


# recursive version
def run_while2(env, args):
    cond = args[0]
    loop = args[1]
    run_if(env, [cond, ["seq", loop, ["while2", cond, loop]], 0])


def run_print(env, args):
    result = []
    for expression in args:
        result.append(run(env, expression))
    print(result)


def run_set(env, args):
    name = args[0]
    value = run(env, args[1])
    env[name] = value
    return value


# ["array", 10]
def run_array(env, args):
    size = args[0]
    return ["arr"] + [None] * size


def run_arr(env, args):
    return args


# ["array_set", "name", 2, 1]
# name = name of the array, 2 = index, 1 = value to set
def run_array_set(env, args):
    name = args[0]
    index = run(env, args[1])
    value = run(env, args[2])
    array = env[name]
    assert array[0] == "arr"
    assert index < len(array) - 1  # keeping track of array designation.
    array[index + 1] = value  # index 0 of the python list is the word array.
    return value  # consistent with set


# ["array_get", "name", 2]
# get value at index 2 of array name
def run_array_get(env, args):
    name = args[0]
    index = run(env, args[1])
    array = env[name]
    assert array[0] == "arr"
    assert index < len(array) - 1
    return array[index + 1]


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


def run_def(env, args):
    assert len(args) == 3
    name = args[0]
    params = args[1]
    body = args[2]
    run_set(env, [name, ["func", params, body]])


def run_call(env, args):
    # Set up the call
    assert len(args) >= 1
    # name = args[0]
    # evaluates all the arguments to the function
    values = [run(env, a) for a in args[1:]]

    # Find the function.
    func = run_get(env, args)
    assert isinstance(func, list) and (func[0] == "func")
    params, body = func[1], func[2]
    assert len(values) == len(params)

    # Run in new environment
    child_env = env.new_child(m=dict(zip(params, values)))
    # env.append(dict(zip(params, values)))
    # print(f"Env in function: {env}")
    result = run(child_env, body)
    # env.pop()
    # print(f"Env after function: {env}")

    # Report
    return result


def run_func(env, expr):
    return ["func"] + expr


# could loop over globals to get all functions starting with run_
FUNCS = {
    name.replace("run_", ""): func
    for (name, func) in globals().items()
    if name.startswith("run_")
}


# dispatch
def run(env, expr):
    # integers evaluate to themselves
    if isinstance(expr, int):
        return expr
    assert isinstance(expr, list)
    op = expr[0]
    args = expr[1:]
    assert op in FUNCS, f"Unknown operation {op}"
    func = FUNCS[op]
    return func(env, args)


# reiko + (alex * 3)
# program = ["add", 1, ["mul", 2, 3]]

# print(run(["add", 1, 2]))

print("\n*** PROGRAM ONE ***\n")
print("Add two variables.\n\n")

stuff = ChainMap({"reiko": 1, "alex": 2})

program = [
    "seq",
    ["set", "reiko", 1],
    ["set", "alex", 2],
    ["add", ["get", "reiko"], ["mul", ["get", "alex"], 3]],
]

print(run(stuff, program))

print("\n*** PROGRAM MCKENZIE ***\n")
print("if statement\n\n")

mckenzie = ["if", 0, 100, -100]
print(run({}, mckenzie))

print("\n*** PROGRAM TWO ***\n")
print("define function\n\n")

stuff2 = ChainMap()
program2 = ["seq", ["def", "f1", [], [1]], ["add", 1, 2]]
print(run(stuff2, program2))
print(stuff2)

print("\n*** PROGRAM THREE ***\n")
print("call function\n\n")

stuff3 = ChainMap()
program3 = [
    "seq",
    ["def", "addone", ["num"], ["add", ["get", "num"], 1]],
    ["set", "reiko", 1],
    ["call", "addone", 2],
]
print(run(stuff3, program3))
print(stuff3)

print("\n*** PROGRAM FOUR ***\n")
print("Repeat and call double.\n\n")

stuff4 = ChainMap()
program4 = [
    "seq",
    ["def", "double", ["num"], ["add", ["get", "num"], ["get", "num"]]],
    ["set", "a", 1],
    [
        "repeat",
        4,
        [
            "seq",
            ["set", "a", ["call", "double", ["get", "a"]]],
            ["print", ["get", "a"]],
        ],
    ],
]

print(run(stuff4, program4))
print(stuff4)

print("\n*** PROGRAM FIVE ***\n")
print("Array set and get.\n\n")

stuff5 = ChainMap()
program5 = [
    "seq",
    ["def", "double", ["num"], ["add", ["get", "num"], ["get", "num"]]],
    ["set", "a", ["array", 10]],
    ["set", "counter", 0],
    [
        "repeat",
        10,
        [
            "seq",
            [
                "array_set",
                "a",
                ["get", "counter"],
                ["call", "double", ["get", "counter"]],
            ],
            ["set", "counter", ["add", ["get", "counter"], 1]],
        ],
    ],
    ["set", "counter", 0],
    [
        "repeat",
        10,
        [
            "seq",
            [
                "print",
                [
                    "array_get",
                    "a",
                    ["get", "counter"],
                ],
            ],
            ["set", "counter", ["add", ["get", "counter"], 1]],
        ],
    ],
    ["print", ["get", "a"]],
]

print(run(stuff5, program5))
print(stuff5)

print("\n*** PROGRAM SIX ***\n")
print("Test using ChainMap to handle environments.\n\n")

stuff6 = ChainMap()
program6 = [
    "seq",
    ["set", "two", 2],
    ["def", "chaintest", ["num"], ["add", ["get", "num"], ["get", "two"]]],
    ["set", "answer", ["call", "chaintest", 1]],
    ["print", ["get", "answer"]],
]

run(stuff6, program6)
print(stuff6)

print("\n*** PROGRAM SEVEN ***\n")
print("While loop using Python while.\n\n")

stuff7 = ChainMap()
program7 = [
    "seq",
    ["set", "counter", 0],
    [
        "while",
        ["lt", ["get", "counter"], 10],
        [
            "seq",
            ["print", ["get", "counter"]],
            ["set", "counter", ["add", ["get", "counter"], 1]],
        ],
    ],
]

run(stuff7, program7)

print("\n*** PROGRAM EIGHT ***\n")
print("While loop using recursion.\n\n")

stuff8 = ChainMap()
program8 = [
    "seq",
    ["set", "counter", 0],
    [
        "while2",
        ["lt", ["get", "counter"], 10],
        [
            "seq",
            ["print", ["get", "counter"]],
            ["set", "counter", ["add", ["get", "counter"], 1]],
        ],
    ],
]

run(stuff8, program8)
