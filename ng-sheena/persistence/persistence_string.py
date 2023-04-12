"""A very simple persistence framework with modified save_str and load_str functions."""

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
    lines = thing.replace("\n", "\\n")
    print(f"str:{lines}", file=writer)

    # assert isinstance(thing, str)
    # lines = thing.split("\n")
    # print(f"str:{len(lines)}", file=writer)
    # for ln in lines:
    #     print(ln, file=writer)

SAVE = {
    "int": save_int,
    "list": save_list,
    "str": save_str
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
    lines = value.rstrip("\n").split("\\n")
    return "\n".join(lines)

    # num_lines = int(value)
    # lines = [reader.readline().rstrip("\n") for _ in range(num_lines)]
    # return "\n".join(lines)

LOAD = {
    "int": load_int,
    "list": load_list,
    "str": load_str
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
