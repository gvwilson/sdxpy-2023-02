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


# could loop over globals to get all functions starting with run_
FUNCS = {
    "add": run_add,
    "get": run_get,
    "mul": run_mul,
    "set": run_set,
    "seq": run_seq,
    "if": run_if,
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
