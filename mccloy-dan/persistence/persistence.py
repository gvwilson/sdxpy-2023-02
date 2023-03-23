"""A very simple persistence framework."""

import io

SEEN = dict()

def save_alias(writer, thing):
    assert id(thing) in SEEN
    print(f"alias:{id(thing)}:", file=writer)

def save_int(writer, thing):
    assert isinstance(thing, int)
    print(f"int:{id(thing)}:{thing}", file=writer)

def save_list(writer, thing):
    assert isinstance(thing, list)
    print(f"list:{id(thing)}:{len(thing)}", file=writer)
    for item in thing:
        save(writer, item)

def save_str(writer, thing):
    assert isinstance(thing, str)
    lines = thing.split("\n")
    print(f"str:{id(thing)}:{len(lines)}", file=writer)
    for ln in lines:
        print(ln, file=writer)

SAVE = {
    "alias": save_alias,
    "int": save_int,
    "list": save_list,
    "str": save_str
}

def save(writer, thing):
    thing_id = id(thing)
    if thing_id in SEEN:
        typename = "alias"
    else:
        typename = type(thing).__name__
    assert typename in SAVE, f"Unknown type {typename}"
    SEEN[thing_id] = thing
    func = SAVE[typename]
    func(writer, thing)

def load_alias(reader, ident, value):
    return SEEN[ident]

def load_int(reader, ident, value):
    SEEN[ident] = int(value)
    return SEEN[ident]

def load_list(reader, ident, value):
    result = []
    SEEN[ident] = result
    num_items = int(value)
    for _ in range(num_items):
        result.append(load(reader))
    return result

def load_str(reader, ident, value):
    lines = []
    num_lines = int(value)
    for _ in range(num_lines):
        lines.append(reader.readline().rstrip("\n"))
    SEEN[ident] = "\n".join(lines)
    return SEEN[ident]

LOAD = {
    "alias": load_alias,
    "int": load_int,
    "list": load_list,
    "str": load_str
}

def load(reader):
    line = reader.readline()
    kind, ident, value = line.split(":", maxsplit=2)
    ident = int(ident)
    assert kind in LOAD, f"Unknown kind {kind}"
    if kind != "alias":
        SEEN[id(value)] = value
    func = LOAD[kind]
    return func(reader, ident, value)

something = "something"
empty_list = []
empty_list.append(empty_list)

TESTS = [
    ("plain integer", 5),
    ("empty list", []),
    ("flat list", [88, 99, 100]),
    ("nested list", [17, 18, [19]]),
    ("plain string", "hello"),
    ("multiline string", "hello\nthere\n"),
    ("everything", [17, "\nhello\n", ["there"]]),
    ("simple alias", [something, something]),
    ("recursive alias", empty_list)
]

for (name, fixture) in TESTS:
    writer = io.StringIO()
    save(writer, fixture)
    content = writer.getvalue()
    reader = io.StringIO(content)
    result = load(reader)
    print(f"{name}\n{content}")
    assert result == fixture, f"Test failed: {name}"
