#! /usr/local/bin/python3

import sys
import json

# language operations

def do_add(env, args):
    assert len(args) == 2
    left = do(env, args[0])
    right = do(env, args[1])
    return left + right

def do_abs(env, args):
    assert len(args) == 1
    val = do(env, args[0])
    return abs(val)

def do_get(env, args):
    assert len(args) == 1
    assert isinstance(args[0], str)
    assert args[0] in env, f"Unknown variable {args[0]}"
    return env[args[0]]

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

def do_def(env, args):
    assert len(args) == 3
    name = args[0]
    params = args[1]
    body = args[2]
    env_set(env, name, ["func", params, body])
    return None

def do_call(env, args):
    # Set up the call.
    assert len(args) >=1
    name = args[0]
    values = [do(env, a) for a in args[1:]]

    # Find the function.
    func = env_get(env, name)
    assert isinstance(func, list) and (func[0] == "func")
    params, body = func[1], func[2]
    assert len(values) == len(params)

    # Run in new environment.
    env.append(dict(zip(params, values)))
    result = do(env, body)
    env.pop()

    # Report.
    return result

def env_get(env, name):
    assert isinstance(name, str)
    if name in env[-1]:
        return env[1][name]
    if name in env[0]:
        return env[0][name]
    assert False, f"Unknown variable {name}"

def env_set(env, name, value):
    assert isinstance(name, str)
    env[name] = value
    

# dictionary of all operations defined

OPS = {
        name.replace("do_", ""): func
        for (name, func) in globals().items()
        if name.startswith("do_")
}

def do(env, expr):
    # Integers evaluate to themselves
    if isinstance(expr, int):
        return expr

    # Lists trigger function calls.
    assert isinstance(expr, list)
    assert expr[0] in OPS, f"Unknown operation {expr[0]}"
    func = OPS[expr[0]]
    return func(env, expr[1:])


def main():
    assert len(sys.argv) == 2, "Usage: expr.py filename"
    with open(sys.argv[1], "r") as reader:
        program = json.load(reader)
    result = do({}, program)
    print(f"=> {result}")

if __name__ == "__main__":
    main()
