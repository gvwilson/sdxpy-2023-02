def env_get(env, name):
    assert name in env.keys(), f"Unknown variable {name}"
    return env[name]


def env_set(env, name, value):
    env[name] = value
    return value


def run_add(env, args):
    left, right = args[0], args[1]
    return run(env, left) + run(env, right)


def run_call(env, args):
    assert len(args) >= 1
    name = args[0]
    func = env_get(env, name)
    assert func[0] == "func", f"Unknown function {name}"
    params = func[1]
    body = func[2]
    assert len(args[1:]) == len(params), (f"{name} takes {len(func[1])}"
                                          f"arguments, but {len(args[1])}"
                                          "were provided")
    local_env = {}
    for arg, param in zip(args[1:], params):
        # Run with default env before passing to set
        run_set(local_env, [param, run(env, arg)])
    return run({**local_env, **env}, body)


def run_def(env, args):
    assert len(args) == 3
    name = args[0]
    params = args[1]
    body = args[2]
    env_set(env, name, ["func", params, body])
    return None


def run_get(env, args):
    assert len(args) == 1
    name = args[0]
    assert name in env.keys(), f"Unknown variable {name}"
    return env[name]


def run_if(env, args):
    cond = args[0]
    if_true = args[1]
    if_false = args[2]
    if run(env, cond):
        return run(env, if_true)
    else:
        return run(env, if_false)


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


# Could build using globals() and looking for functions that start with "run_",
# use the part after "run_" for key
FUNCS = {
    name.removeprefix("run_"): func
    for (name, func) in globals().items() if name.startswith("run_")
}


# dispatch function, finds operation and dispatches it to proper function
def run(env, expr):
    if isinstance(expr, int):
        return expr
    op = expr[0]
    args = expr[1:]
    assert op in FUNCS, f"Unknown operation {op}"
    func = FUNCS[op]
    return func(env, args)


program = [
    "seq",
    ["set", "test", 1],
    ["set", "other", 2],
    [
        "add",
        ["get", "test"],
        ["mul", ["get", "other"], 3]
    ]
]
# print(run({}, program))
test_if = ["if", 0, 100, -100]

test_func = [
    "seq",
    ["set", "a", 5],
    ["set", "b", 3],
    ["def", "self", ["val"], ["get", "val"]],
    ["call", "self",
     ["add",
      ["get", "a"],
      ["get", "b"]
      ]
     ]
]
print(run({}, test_func))
