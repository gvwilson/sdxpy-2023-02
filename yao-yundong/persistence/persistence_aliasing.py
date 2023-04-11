"""A very simple persistence framework."""

import io


def save_int(writer, thing, seen):
    assert isinstance(thing, int)
    print(f"int:{thing}:{id(thing)}", file=writer)

def save_list(writer, thing, seen):
    assert isinstance(thing, list)
    print(f"list:{len(thing)}:{id(thing)}", file=writer)
    for item in thing:
        save(writer, item, seen)

def save_str(writer, thing, seen):
    assert isinstance(thing, str)
    lines = thing.split("\n")
    print(f"str:{len(lines)}:{id(thing)}", file=writer)
    for ln in lines:
        print(ln, file=writer)

SAVE = {
    "int": save_int,
    "list": save_list,
    "str": save_str
}

def save(writer, thing, seen):
    thing_id = id(thing)
    if thing_id in seen:
        print(f"alias:'':{thing_id}", file=writer)
        return   
    typename = type(thing).__name__
    assert typename in SAVE, f"Unknown type {typename}"
    seen.add(thing_id)
    func = SAVE[typename]
    func(writer, thing, seen)


def load_int(reader, value, seen):
    return int(value)

def load_list(reader, value, seen):
    num_items = int(value)
    return [load(reader, seen) for _ in range(num_items)]

def load_str(reader, value, seen):
    num_lines = int(value)
    lines = [reader.readline().rstrip("\n") for _ in range(num_lines)]
    return "\n".join(lines)

LOAD = {
    "int": load_int,
    "list": load_list,
    "str": load_str
}

def load(reader, seen):
    kind, value, entid = reader.readline().split(":", maxsplit=2)
    if kind == "alias":
        assert entid in seen
        return seen[entid]
    
    assert kind in LOAD, f"Unknown kind {kind}"
    func = LOAD[kind]
    result = func(reader, value, seen)
    seen[entid] = result
    return result 

TESTS = [
    ("plain integer", 5),
    ("empty list", []),
    ("flat list", [88, 99, 100]),
    ("nested list", [17, 18, [19]]),
    ("plain string", "hello"),  
    ("multiline string", "hello\nthere\n"),
    ("everything", [17, "\nhello\n", ["there"]])
]

seen_save = set()
seen_load = {}

for (name, fixture) in TESTS:
    writer = io.StringIO()
    save(writer, fixture, seen_save)
    content = writer.getvalue()
    reader = io.StringIO(content)
    result = load(reader, seen_load)
    print(f"{name}\n{content}")
    assert result == fixture, f"Test failed: {name}"

def roundtrip(fixture):
    writer = io.StringIO()
    save(writer, fixture, seen_save)
    reader = io.StringIO(writer.getvalue())
    return load(reader, seen_load)

def test_aliasing_shared_child():
    shared = ["shared"]
    fixture = [shared, shared]
    result = roundtrip(fixture)
    assert result == fixture
    assert id(result[0]) == id(result[1])
    result[0][0] = "changed"
    assert result[1][0] == "changed"

test_aliasing_shared_child()