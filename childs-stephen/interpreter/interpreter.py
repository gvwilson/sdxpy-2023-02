# 1 + (2 * 3)
# Lisp == Lots of Irritating Single Parenthsis


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


def run_seq(env, args):
    result = None
    for expression in args:
        result = run(env, expression)
    return result


def run_set(env, args):
    name = args[0]
    value = run(env, args[1])
    env[name] = value
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


def run_def(env, args):
    assert len(args) == 3
    name = args[0]
    params = args[1]
    body = args[2]
    run_set(env, [name, ["func", params, body]])


def run_call(env, args):
    # Set up the call
    assert len(args) >= 1
    name = args[0]
    # evaluates all the arguments to the function
    values = [run(env, a) for a in args[1:]]

    # Find the function.
    func = run_get(env, name)
    assert isinstance(func, list) and (func[0] == "func")
    params, body = func[1], func[2]
    assert len(values) == len(params)

    # Run in new environment
    env.append(dict(zip(params, values)))
    result = run(env, body)
    env.pop

    # Report
    return result


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

stuff = {"reiko": 1, "alex": 2}

program = [
    "seq",
    ["set", "reiko", 1],
    ["set", "alex", 2],
    ["add", ["get", "reiko"], ["mul", ["get", "alex"], 3]],
]

print(run(stuff, program))

mckenzie = ["if", 0, 100, -100]
print(run({}, mckenzie))

stuff2 = {}
program2 = ["seq", ["def", "f1", [], [1]], ["add", 1, 2]]
run(stuff2, program2)
print(stuff2)

stuff3 = {}
program3 = [
    "seq",
    ["def", "addone", ["num"], ["add", "num", 1]],
    ["set", "reiko", 1],
    ["call", "addone", ["reiko"]],
]
run(stuff3, program3)
print(stuff3)
