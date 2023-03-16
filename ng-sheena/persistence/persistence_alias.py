"""A very simple persistence framework with added functions to handle aliases."""

import io

def save_int(writer, thing_id, thing):
    assert isinstance(thing, int)
    print(f"int:{thing_id}:{thing}", file=writer)

def save_list(writer, thing_id, thing):
    assert isinstance(thing, list)
    print(f"list:{thing_id}:{len(thing)}", file=writer)
    for item in thing:
        save(writer, item)

def save_str(writer, thing_id, thing):
    assert isinstance(thing, str)
    lines = thing.split("\n")
    print(f"str:{thing_id}:{len(lines)}", file=writer)
    for ln in lines:
        print(ln, file=writer)

SAVE = {
    "int": save_int,
    "list": save_list,
    "str": save_str
}

save_seen = set()

def save(writer, thing):
    thing_id = id(thing)
    if thing_id in save_seen:
        print(f"alias:{thing_id}:", file=writer)
    else:
        save_seen.add(thing_id)
        typename = type(thing).__name__
        assert typename in SAVE, f"Unknown type {typename}"
        func = SAVE[typename]
        func(writer, thing_id, thing)

def load_int(reader, thing_id, value):
    return int(value)

def load_list(reader, thing_id, value):
    num_items = int(value)
    return [load(reader) for _ in range(num_items)]

def load_str(reader, thing_id, value):
    num_lines = int(value)
    lines = [reader.readline().rstrip("\n") for _ in range(num_lines)]
    return "\n".join(lines)

LOAD = {
    "int": load_int,
    "list": load_list,
    "str": load_str
}

load_seen = {}

def load(reader):
    kind, thing_id, value = reader.readline().split(":", maxsplit=2)
    if kind == "alias":
        assert thing_id in load_seen
        return load_seen[thing_id]

    assert kind in LOAD, f"Unknown kind {kind}"
    func = LOAD[kind]
    res = func(reader, thing_id, value)
    load_seen[thing_id] = res
    return res

def test_alias():
    shared = "shared"
    fixture = [shared, shared]
    return fixture

def test_alias2():
    shared = [1,2,3]
    fixture = [shared, shared, 2]
    return fixture

TESTS = [
    ("plain integer", 5),
    ("empty list", []),
    ("flat list", [88, 99, 100]),
    ("nested list", [17, 18, [19]]),
    ("plain string", "hello"),
    ("multiline string", "hello\nthere\n"),
    ("everything", [17, "\nhello\n", ["there"]]),
    ("alias", test_alias()),
    ("alias2", test_alias2())
]

for (name, fixture) in TESTS:
    writer = io.StringIO()
    save(writer, fixture)
    content = writer.getvalue()
    reader = io.StringIO(content)
    result = load(reader)
    print(f"{name}\n{content}")
    assert result == fixture, f"Test failed: {name}"
