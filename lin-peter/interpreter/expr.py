import json
import sys
from collections import ChainMap


def do_add(env, args):
    assert len(args) == 2
    left = do(env, args[0])
    right = do(env, args[1])
    return left + right


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


def do_abs(env, args):
    assert len(args) == 1
    val = do(env, args[0])
    return abs(val)


def do_comment(env, args):
    """Ignore instructions.
    ["comment" "text"] => None
    """
    return None


def do_print(env, args):
    assert len(args) == 1
    # if args[0] is an object in env
    if args[0] in env:
        print(env[args[0]])
    # print args[0] like any string
    else:
        print(args[0])


def do_array(env, args):
    assert len(args) == 1
    assert isinstance(int(args[0]), int)
    array_created = [None] * args[0]
    env["array_size" + str(args[0])] = array_created
    return array_created


# ["array_set", "name_of_array", "index", "value_to_be_added_to_index"]
def do_array_set(env, args):
    assert len(args) == 3
    assert args[0] in env  # make sure that the array is present
    assert isinstance(int(args[1]), int)
    env[args[0]][args[1]] = args[2]


# ["array_get", "name_of_array", "index"]
def do_array_get(env, args):
    assert len(args) == 2
    assert args[0] in env  # make sure that the array is present
    assert isinstance(int(args[1]), int)
    return env[args[0]][args[1]]


def env_get(env, name):
    assert isinstance(name, str)
    if name in env:
        return env[name]
    assert False, f"Unknown variable {name}"


def env_set(env, var_name, var_value):
    assert isinstance(var_name, str)
    if var_name not in env:
        env[var_name] = var_value
    else:
        raise TypeError(f"object {var_name} already exists in {env}")


def do_def(env, args):
    assert len(args) == 3
    name = args[0]
    params = args[1]
    body = args[2]
    env_set(env, name, ["func", params, body])
    return None


def do_if(env, args):
    """Make a choice: only one sub-expression is evaluated.
    ["if" C A B] => A if C else B
    """
    assert len(args) == 3
    cond = do(env, args[0])
    choice = args[1] if cond else args[2]
    return do(env, choice)


# from Greg's implementation
def do_leq(env, args):
    """Less than or equal.
    ["leq" A B] => A <= B
    """
    assert len(args) == 2
    return do(env, args[0]) <= do(env, args[1])


# ["while", "condition_to_eval", "perform_operation"]
def do_while(env, args):
    assert len(args) == 2
    condition = do(env, args[0])
    while condition:
        # perform operation
        result = do(env, args[1])
        # re-evaluate condition
        condition = do(env, args[0])
    return result


OPS = {
    name.replace("do_", ""): func
    for (name, func) in globals().items()
    if name.startswith("do_")
}

# use python's built-in ChainMap to unify globals and OPS
tll_env = ChainMap(OPS, globals())


def do(env, expr):
    # Integers evaluate to themselves.
    if isinstance(expr, int):
        return expr
    # debug print to show call stack
    # print(expr[0])
    assert expr[0] in OPS, f"Unknown operation {expr[0]}"
    func = OPS[expr[0]]
    return func(env, expr[1:])


def main():
    assert len(sys.argv) == 2, "Usage: expr.py filename"
    with open(sys.argv[1], "r") as reader:
        program = json.load(reader)
    result = do(tll_env, program)
    print(f"=> {result}")


if __name__ == "__main__":
    main()
