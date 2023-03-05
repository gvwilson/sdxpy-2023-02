#! /usr/local/bin/python3

import sys
import json
from collections import ChainMap

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
    return env_get(env, args[0]) 

def do_set(env, args):
    assert len(args) == 2
    assert isinstance(args[0], str)
    value = do(env, args[1])
    env_set(env, args[0], value)
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
    env = env.new_child(dict(zip(params, values))) #changed to use chainmap
    result = do(env, body)
    env = env.parents # changed to use chainmap

    # Report.
    return result

def do_array(env, args):
    assert len(args) == 1
    array = [ None ] * args[0]
    return array

def do_array_get(env, args):
    assert len(args) == 2
    assert isinstance(args[0], str)
    name, position = args[0], args[1]
    array = do_get(env, name)
    return array[position]

def do_array_set(env, args):
    assert len(args) == 3
    assert isinstance(args[0], str)
    name , position, value = args[0], args[1], args[2]
    array = do_get(env, name)
    array[position] = value
    do_set(env,[name,array])
    return array

def do_print(env, args):
    result = do(env,args[0])
    print(result)
    return None

def do_repeat(env,args):
    assert len(args) == 2
    assert isinstance(args[0], int)
    for i in range(args[0]):
        do(env, args[1])
    return None

def do_while(env,args):
    assert len(args) == 2
    while do(env,args[0]):
        do(env, args[1])
    return None

# environment handling

def env_get(env, name):
    assert isinstance(name, str)
    if name in env.maps[-1]: # kollar i chainmap sist
        return env.maps[-1][name]
    if name in env.maps[0]: # och först
        return env.maps[0][name]
    assert False, f"Unknown variable {name}"

def env_set(env, name, value):
    assert isinstance(name, str)
    env[name] = value # lägg till i den sista i chainmap-en
    

# dictionary of all operations defined

#Change this to adding to a chain map? and change environment functions to work for chain map. finally, main must send empty chainmap. is that it? No, also need to update do_call

# Changed: main function
# Changed: environment functions
# Changed: do_call

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
    env = ChainMap()
    result = do(env, program)
    print(f"=> {result}")

if __name__ == "__main__":
    main()
