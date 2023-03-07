import json
import sys
from collections import ChainMap


def do_abs(env, args):
    assert len(args) == 1
    val = do(env, args[0])
    return abs(val)


def do_add(env, args):
    assert len(args) == 2
    left = do(env, args[0])
    right = do(env, args[1])
    return left + right


def do_array(env, args):
    assert len(args) == 1 and isinstance(args[0], int)
    return [None] * args[0]


def do_array_get(env, args):
    """Get an array value by index."""
    assert len(args) == 2
    array = do_get(env, args[:1])
    index = do(env, args[1])
    assert isinstance(index, int)
    return array[index]


def do_array_set(env, args):
    """Set an array value at an index."""
    assert len(args) == 3
    array = do_get(env, args[:1])
    index = do(env, args[1])
    value = do(env, args[2])
    assert isinstance(index, int)
    array[index] = value
    return value


def do_call(env, args):
    """Call a function.
    ["call" name ...expr...] => env[name](*expr)
    """
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
    env = env.new_child(dict(zip(params, values)))
    result = do(env, body)
    # Report.
    return result


def do_def(env, args):
    """Define a new function.
    ["def" name [...params...] body] => None # and define function
    """
    assert len(args) == 3
    name = args[0]
    params = args[1]
    body = args[2]
    env_set(env, name, ["func", params, body])
    return None


def do_get(env, args):
    assert len(args) == 1
    return env_get(env, args[0])


def do_if(env, args):
    """Make a choice: only one sub-expression is evaluated.
    ["if" C A B] => A if C else B
    """
    assert len(args) == 3
    cond = do(env, args[0])
    choice = args[1] if cond else args[2]
    return do(env, choice)


def do_leq(env, args):
    """Less than or equal.
    ["leq" A B] => A <= B
    """
    assert len(args) == 2
    return do(env, args[0]) <= do(env, args[1])


def do_mul(env, args):
    assert len(args) == 2
    left = do(env, args[0])
    right = do(env, args[1])
    return left * right


def do_print(env, args):
    """Print values.
    ["print" ...values...] => None # print each value
    """
    args = [do(env, a) for a in args]
    print(*args)
    return None


def do_repeat(env, args):
    """Repeat instructions some number of times.
    ["repeat" N expr] => expr # last one of N
    """
    assert len(args) == 2
    count = do(env, args[0])
    for i in range(count):
        result = do(env, args[1])
    return result


def do_seq(env, args):
    assert len(args) > 0
    for item in args:
        result = do(env, item)
    return result


def do_set(env, args):
    assert len(args) == 2
    name = args[0]
    assert isinstance(name, str)
    value = do(env, args[1])
    env_set(env, name, value)
    return value


def do_while(env, args):
    """Repeat an action while a condition is satisfied."""
    assert len(args) == 2
    cond = do(env, args[0])
    if cond:
        _ = do(env, args[1])
        return do_while(env, args)
    else:
        return None


def do(env, expr):
    # Integers evaluate to themselves.
    if not isinstance(expr, list):
        return expr

    # Lists trigger function calls.
    assert expr[0] in OPS, f"Unknown operation {expr[0]}"
    func = OPS[expr[0]]
    return func(env, expr[1:])


def env_get(env, name):
    assert isinstance(name, str)
    if name in env:
        return env[name]
    assert False, f"Unknown variable {name}"


def env_set(env, name, value):
    assert isinstance(name, str)
    if name in env:
        env[name] = value
    else:
        env[name] = value


def main():
    assert len(sys.argv) == 2, "Usage: expr.py filename"
    with open(sys.argv[1], "r") as reader:
        program = json.load(reader)
    result = do(ChainMap(), program)
    print(f"=> {result}")


OPS = {
    name.replace("do_", ""): func
    for (name, func) in globals().items()
    if name.startswith("do_")
}


if __name__ == "__main__":
    main()
