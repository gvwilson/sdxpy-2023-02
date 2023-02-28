from collections import ChainMap

def do_add(env, args):
    assert len(args) == 2
    left = do(env, args[0])
    right = do(env, args[1])
    return left + right

def do_abs(env, args):
    assert len(args) == 1
    val = do(env, args[0])
    return abs(val)

# ["get", "name"]
def do_get(env, args):
    assert len(args) == 1
    name = args[0]
    assert isinstance(name, str)
    return env_get(env, name)
# ["set", "name", …expression…]
def do_set(env, args):
    assert len(args) == 2
    name = args[0]
    assert isinstance(name, str)
    value = do(env, args[1])
    env_set(env, name, value)
    return value

def do_mul(env, args):
    assert len(args) == 2
    left = do(env, args[0])
    right = do(env, args[1])
    return left * right

def do_seq(env, args):
    assert len(args) > 0
    result = None
    for expr in args:
        result = do(env, expr)
    return result

# lazy evaluation
def do_if(env, args):
    assert len(args) == 3
    cond = args[0]
    if_true = args[1]
    if_false = args[2]
    if do(env, cond):
        return do(env, if_true)
    else:
        return do(env, if_false)

# eager evaluation
def do_if(env, args):
    assert len(args) == 3
    cond = do(env, args[0])
    if_true = do(env, args[1])
    if_false = do(env, args[2])
    if cond:
        return if_true
    else:
        return if_false

# function definition

def do_def(env, args):
    assert len(args) == 3
    name = args[0]
    params = args[1]
    body = args[2]
    env_set(env, name, ["func", params, body])
    return None

def do_call(env, args):
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
    call_context = env.new_child()
    for param, value in zip(params, values):
        call_context[param] = value
    result = do(call_context, body)

    # Report.
    return result

OPS = {
    name.replace("do_", ""): func
    for (name, func) in globals().items()
    if name.startswith("do_")
}

def do(env, expr):
    # Integers evaluate to themselves.
    if not isinstance(expr, list):
        return expr
    op = expr[0]
    args = expr[1:]
    assert op in OPS, f"Unknown operation {op}"
    func = OPS[op]
    return func(env, args)


# function definition

def env_get(env, name):
    assert isinstance(name, str)
    
    return env[name]

def env_set(env, name, value):
    assert isinstance(name, str)

    env[name] = value

    return value

program = [
    "seq",
    ["set", "firas", 1],
    ["set", "jenna", 3],
    ["add", 
    ["get", "firas"], # 1
    ["mul", 2, 
     ["get", "jenna"]] # 3
    ]
]
print(do(ChainMap(), program))

another_program = ["if", False, "yes", "no"]
print(do(ChainMap(), another_program))

# x = y = 2

# ["if", z != 0, 1/z, None]

function_program = [
    "seq",
    ["def", "same", ["num"],
     ["get", "num"]
    ],
    ["call", "same", 3]
]

print(do(ChainMap(), function_program))
