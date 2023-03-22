"""A very simple persistence framework."""

import io

def save_int(writer, thing, seen):
    assert isinstance(thing, int)
    print(f"int:{id(thing)}:{thing}", file=writer)

def save_list(writer, thing, seen):
    assert isinstance(thing, list)
    print(f"list:{id(thing)}:{len(thing)}", file=writer)
    for item in thing:
        save(writer, item, seen)

def save_str(writer, thing, seen):
    assert isinstance(thing, str)
    lines = thing.split("\n")
    print(f"str:{id(thing)}:{len(lines)}", file=writer)
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
        print(f"alias:{thing_id}:", file=writer)
        return

    seen.add(thing_id)
    typename = type(thing).__name__
    assert typename in SAVE, f"Unknown type {typename}"
    func = SAVE[typename]
    func(writer, thing, seen)

def load_int(reader, ident, value, seen):
    result = int(value)
    seen[ident] = result
    return result

def load_list(reader, ident, value, seen):
    result = []
    seen[ident] = result
    num_items = int(value)
    for _ in range(num_items):
        result.append(load(reader, seen))
    return result

def load_str(reader, ident, value, seen):
    num_lines = int(value)
    lines = [reader.readline().rstrip("\n") for _ in range(num_lines)]
    result = "\n".join(lines)
    seen[ident] = result
    return result

LOAD = {
    "int": load_int,
    "list": load_list,
    "str": load_str
}

def load(reader, seen):
    kind, ident, value = reader.readline().split(":", maxsplit=2)

    if kind == "alias":
        assert ident in seen
        return seen[ident]
    
    assert kind in LOAD, f"Unknown kind {kind}"
    func = LOAD[kind]
    return func(reader, ident, value, seen)

TESTS = [
    ("plain integer", 5),
    ("empty list", []),
    ("flat list", [88, 99, 100]),
    ("nested list", [17, 18, [19]]),
    ("plain string", "hello"),
    ("multiline string", "hello\nthere\n"),
    ("everything", [17, "\nhello\n", ["there"]]),
    ("aliased list", [17, 17, [17]]),    
]

for (name, fixture) in TESTS:
    saved_seen = set()
    loaded_seen = dict()

    writer = io.StringIO()
    save(writer, fixture, saved_seen)
    content = writer.getvalue()
    reader = io.StringIO(content)
    result = load(reader, loaded_seen)
    print(f"{name}\n{content}")
    assert result == fixture, f"Test failed: {name}"

# manually test self-referential list

saved_seen = set()
loaded_seen = dict()

name = "self-referential list"
fixture = []
fixture.append(fixture)

writer = io.StringIO()
save(writer, fixture, saved_seen)
content = writer.getvalue()
reader = io.StringIO(content)
result = load(reader, loaded_seen)
print(f"{name}\n{content}")
# comparison of result to fixture results in recursion error
assert id(result[0]) == id(result), f"Test failed: {name}"
