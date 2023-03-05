import sys
import json

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
    return env_get(env, args[0])

def do_set(env, args):
    assert len(args) == 2
    name = args[0]
    value = do(env, args[1])
    env_set(env, name, value)
    return value

def do_seq(env, args):
    assert len(args) > 0
    for item in args:
        result = do(env, item)
    return result

def do_comment(env, args):
    """Ignore instructions.
    ["comment" "text"] => None
    """
    return None

def do_if(env, args):
    """Make a choice: only one sub-expression is evaluated.
    ["if" C A B] => A if C else B
    """
    assert len(args) == 3
    cond = do(env, args[0])
    choice = args[1] if cond else args[2]
    return do(env, choice)

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

def env_get(env, name):
    assert isinstance(name, str)
    if name in env[-1]:
        return env[-1][name]
    if name in env[0]:
        return env[0][name]
    assert False, f"Unknown variable {name}"

def env_set(env, name, value):
    assert isinstance(name, str)
    if name in env[-1]:
        env[-1][name] = value
    elif name in env[0]:
        env[0][name] = value
    else:
        env[-1][name] = value

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
    env.append(dict(zip(params, values)))
    result = do(env, body)
    env.pop()

    # Report.
    return result

OPS = {
    name.replace("do_", ""): func
    for (name, func) in globals().items()
    if name.startswith("do_")
}

def do(env, expr):
    # Integers evaluate to themselves.
    if isinstance(expr, int):
        return expr

    # Lists trigger function calls.
    assert isinstance(expr, list)
    assert expr[0] in OPS, f"Unknown operation {expr[0]}"
    func = OPS[expr[0]]
    return func(env, expr[1:])

def main():
    assert len(sys.argv) == 2, "Usage: func.py filename"
    with open(sys.argv[1], "r") as reader:
        program = json.load(reader)
    result = do([{}], program)
    print(f"=> {result}")

if __name__ == "__main__":
    main()