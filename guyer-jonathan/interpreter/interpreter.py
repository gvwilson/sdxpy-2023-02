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

def do_eq(env, args):
    assert len(args) == 2
    left = do(env, args[0])
    right = do(env, args[1])
    return left == right

def do_gt(env, args):
    assert len(args) == 2
    left = do(env, args[0])
    right = do(env, args[1])
    return left > right

def do_lt(env, args):
    assert len(args) == 2
    left = do(env, args[0])
    right = do(env, args[1])
    return left < right

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

# arrays

def do_array(env, args):
    # ["array", size]
    
    assert len(args) == 1
    size = args[0]
    assert isinstance(size, int)
    
    # initialize empty array
    return [None] * size

def do_array_get(env, args):
    # ["array_get", "var", …index…]
    
    assert len(args) == 2
    name = args[0]
    index = args[1]
    assert isinstance(index, int)
    
    array = do_get(env, [name])
    
    return array[index]

def do_array_set(env, args):
    # ["array_set", "var", …index…, …value…],

    assert len(args) == 3
    name = args[0]
    index = args[1]
    value = args[2]
    assert isinstance(index, int)
    
    array = do_get(env, [name])
    
    array[index] = value
    
    return value

# while

# # Python while
# def do_while(env, args):
#     # ["while", …condition…, …body…]
#     assert len(args) == 2
#     condition = args[0]
#     body = args[1]
    
#     while do(env, condition):
#         do(env, body)

# recursive
def do_while(env, args):
    # ["while", …condition…, …body…]
    assert len(args) == 2
    condition = args[0]
    body = args[1]
    
    if do(env, condition):
        do(env, body)
        do_while(env, args)

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

# tests

def test_seq():
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
    assert do(ChainMap(), program) == 7

def test_if_false():
    program = ["if", False, "yes", "no"]
    assert do(ChainMap(), program) == "no"

def test_if_true():
    program = ["if", True, "yes", "no"]
    assert do(ChainMap(), program) == "yes"

def test_function():
    program = [
        "seq",
        ["def", "same", ["num"],
         ["get", "num"]
        ],
        ["call", "same", 3]
    ]

    assert do(ChainMap(), program) == 3

def test_array_create():
    program = ["array", 10]
    
    array = do(ChainMap(), program)
    
    assert isinstance(array, list)
    assert len(array) == 10

def test_array_assign():
    program = [
        "seq",
        ["set", "var", 
         ["array", 10]
        ],
        ["get", "var"]
    ]
    
    array = do(ChainMap(), program)
    
    assert isinstance(array, list)
    assert len(array) == 10

def test_array_get_and_set():
    program = [
        "seq",
        ["set", "var", 
         ["array", 10]
        ],
        ["array_set", "var", 2, 7],
        ["array_get", "var", 2]
    ]
    
    assert do(ChainMap(), program) == 7
    
def test_while():
    program = [
        "seq",
        ["set", "counter", 10],
        ["while",
         ["gt", ["get", "counter"], 0],
         ["set", "counter",
          ["add", ["get", "counter"], -1]
         ]
        ],
        ["get", "counter"]
    ]
    
    assert do(ChainMap(), program) == 0

def run_tests():
    results = {
        "skipped": [], 
        "passed": [],
        "failed": [],
        "errored": []
    }

    for (name, test) in globals().items():
        if not name.startswith("test_"):
            continue
        if hasattr(test, "skip"):
            results["skipped"].append(name)
            continue
        try:
            test()
            results["passed"].append(name)
        except AssertionError as e:
            if test.__doc__ == "test:assert":
                results["passed"].append(name)
            elif hasattr(test, "fail"):
                results["passed"].append(name)
            else:
                results["failed"].append(name)
        except Exception as e:
            results["errored"].append(name)

    return results
    
if __name__ == "__main__":
    print(run_tests())
