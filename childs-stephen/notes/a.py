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


# dispatch
def run(env, expr):
    if isinstance(expr, int):
        return expr
    op = expr[0]
    args = expr[1:]
    if op == "add":
        return run_add(env, args)
    if op == "get":
        return run_get(env, args)
    if op == "mul":
        return run_mul(env, args)
    assert False, f"Unknown operation {op}"


# reiko + (alex * 3)
# program = ["add", 1, ["mul", 2, 3]]

print(run(program))
# print(run(["add", 1, 2]))

stuff = {"reiko": 1, "alex": 3}

program = ["add", ["get", "reiko"], ["mul", ["get", "alex"], 3]]

print(run(stuff, program))
