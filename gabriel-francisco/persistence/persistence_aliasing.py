"""A very simple persistence framework."""

import io

# the set and dict below are in the wrong place. I should think more about it but am inclined to using a class to hold the state, as seen in 8.2
seen_save = set()
seen_load = {}

def save_int(writer, thing):
    assert isinstance(thing, int)
    print(f"int:{thing}:{id(thing)}", file=writer)

def save_list(writer, thing):
    assert isinstance(thing, list)
    print(f"list:{len(thing)}:{id(thing)}", file=writer)
    for item in thing:
        save(writer, item)

def save_str(writer, thing):
    assert isinstance(thing, str)
    lines = thing.split("\n")
    print(f"str:{len(lines)}:{id(thing)}", file=writer)
    for ln in lines:
        print(ln, file=writer)

def save_alias(writer, thing_id):
    print(f"alias::{thing_id}", file=writer)

SAVE = {
    "int": save_int,
    "list": save_list,
    "str": save_str
}

def save(writer, thing):
    thing_id = id(thing)
    if thing_id in seen_save:
        save_alias(writer,thing_id)
        return
    seen_save.add(thing_id)
    typename = type(thing).__name__
    assert typename in SAVE, f"Unknown type {typename}"
    func = SAVE[typename]
    func(writer, thing)

def load_int(reader, value, thing_id):
    return int(value)

def load_list(reader, value, thing_id):
    num_items = int(value)
    return [load(reader) for _ in range(num_items)]

def load_str(reader, value, thing_id):
    num_lines = int(value)
    lines = [reader.readline().rstrip("\n") for _ in range(num_lines)]
    return "\n".join(lines)

LOAD = {
    "int": load_int,
    "list": load_list,
    "str": load_str,
    "alias": lambda _, __, thing_id: seen_load[thing_id]
}

def load(reader):
    kind, value, thing_id = reader.readline().split(":", maxsplit=2)
    assert kind in LOAD, f"Unknown kind {kind}"
    func = LOAD[kind]
    answer = func(reader, value, thing_id)
    seen_load[thing_id] = answer
    return answer

def alias_test_fixture():
    a = [1,2,3]
    return [a,1,a]

TESTS = [
    ("plain integer", 5),
    ("empty list", []),
    ("flat list", [88, 99, 100]),
    ("nested list", [17, 18, [19]]),
    ("plain string", "hello"),
    ("multiline string", "hello\nthere\n"),
    ("everything", [17, "\nhello\n", ["there"]]),
    ("alias", alias_test_fixture())
]

for (name, fixture) in TESTS:
    # writer = None
    writer = io.StringIO()
    save(writer, fixture)
    content = writer.getvalue()
    reader = io.StringIO(content)
    result = load(reader)
    print(f"{name}\n{content}")
    assert result == fixture, f"Test failed: {name}"

# with open("a.txt", mode="a") as writer:
#     for (name, fixture) in TESTS:
#         save(writer, fixture)
