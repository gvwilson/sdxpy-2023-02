"""A very simple persistence framework."""

import io

def save_int(writer, thing):
    assert isinstance(thing, int)
    print(f"int:{thing}", file=writer)

def save_list(writer, thing):
    assert isinstance(thing, list)
    print(f"list:{len(thing)}", file=writer)
    for item in thing:
        save(writer, item)

def save_str(writer, thing):
    assert isinstance(thing, str)
    lines = thing.split("\n")
    print(f"str:{len(lines)}", file=writer)
    for ln in lines:
        print(ln, file=writer)

# SAVE = {
#     "int": save_int,
#     "list": save_list,
#     "str": save_str
# }

SAVE = {
    name.replace("save_", ""): func
    for (name, func) in globals().items()
    if name.startswith("save_")
}

def save(writer, thing):
    typename = type(thing).__name__
    assert typename in SAVE, f"Unknown type {typename}"
    func = SAVE[typename]
    func(writer, thing)

def load_int(reader, value):
    return int(value)

def load_list(reader, value):
    num_items = int(value)
    return [load(reader) for _ in range(num_items)]

def load_str(reader, value):
    num_lines = int(value)
    lines = [reader.readline().rstrip("\n") for _ in range(num_lines)]
    return "\n".join(lines)

# LOAD = {
#     "int": load_int,
#     "list": load_list,
#     "str": load_str
# }

LOAD = {
    name.replace("load_", ""): func
    for (name, func) in globals().items()
    if name.startswith("load_")
}

def load(reader):
    kind, value = reader.readline().split(":", maxsplit=1)
    assert kind in LOAD, f"Unknown kind {kind}"
    func = LOAD[kind]
    return func(reader, value)

TESTS = [
    ("plain integer", 5),
    ("empty list", []),
    ("flat list", [88, 99, 100]),
    ("nested list", [17, 18, [19]]),
    ("plain string", "hello"),
    ("multiline string", "hello\nthere\n"),
    ("everything", [17, "\nhello\n", ["there"]])
]

for (name, fixture) in TESTS:
    writer = io.StringIO()
    save(writer, fixture)
    content = writer.getvalue()
    reader = io.StringIO(content)
    result = load(reader)
    print(f"{name}\n{content}")
    assert result == fixture, f"Test failed: {name}"

'''
Why is this a bad idea?

Answer:
The method of looking for save_ and load_ functions using
globals() may result in:
- performance degradation if the search space is big (ie.
many functions to iterate through find save_ and load_

- there might be many other functions that could start with the same
prefixes. This could result in finding variables or other functions
named save_ and/or load_ that are not related to our persistence
framework.

However, I think if we manage the function naming well, I don't
think this would necessarily be a bad idea.
'''