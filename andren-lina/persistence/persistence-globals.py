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

SAVE = {
    "int": save_int,
    "list": save_list,
    "str": save_str
}

# changing this to use globals instead of SAVE
# Why is this a bad idea?
# I'm not sure, but I'm a little uncomfortable with the dynamic lookup. Can't come up with an example that would cause a problem though. Could there be standard functions called things with save and load in some libraries? At least, I kind of loose control of what functions can be included.
def save(writer, thing):
    typename = 'save_'+ type(thing).__name__
    assert typename in globals(), f"Unknown type {typename}"
    func = globals()[typename]
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

LOAD = {
    "int": load_int,
    "list": load_list,
    "str": load_str
}

# changing load to read from globals() rather than LOAD in the same way as I changed save(). The answer to why this may be a bad idea remains the same.

def load(reader):
    kind, value = reader.readline().split(":", maxsplit=1)
    kindname = 'load_'+ kind 
    assert kindname in globals(), f"Unknown kind {kind}"
    func = globals()[kindname]
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
