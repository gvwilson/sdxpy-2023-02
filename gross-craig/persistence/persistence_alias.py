"""A very simple persistence framework."""

import io
import collections

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
    "int": save_int,
    "list": save_list,
    "str": save_str
}

writer_saved_ids = collections.defaultdict(set)

def save(writer, thing):
    thing_id = id(thing)
    saved_ids = writer_saved_ids[writer]
    if thing_id in saved_ids:
        print(f"alias:{thing_id}:", file=writer)
    else:
        typename = type(thing).__name__
        assert typename in SAVE, f"Unknown type {typename}"
        func = SAVE[typename]
        func(writer, thing)
        saved_ids.add(thing_id)

def load_int(reader, value):
    result = int(value)
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

reader_loaded_ids = collections.defaultdict(dict)

def load(reader):
    kind, value_id, value = reader.readline().split(":", maxsplit=2)
    loaded_ids = reader_loaded_ids[reader]
    if kind == "alias":
        assert reader in reader_loaded_ids.keys()
        assert value_id in loaded_ids.keys()
        result = loaded_ids[value_id]
    else:
        assert kind in LOAD, f"Unknown kind {kind}"
        func = LOAD[kind]
        result = func(reader, value)
        loaded_ids[value_id] = result
    return result

def alias_fixture():
    shared = ["shared"]
    fixture = [shared, shared]
    return fixture

TESTS = [
    ("plain integer", 5),
    ("empty list", []),
    ("flat list", [88, 99, 100]),
    ("nested list", [17, 18, [19]]),
    ("plain string", "hello"),
    ("multiline string", "hello\nthere\n"),
    ("everything", [17, "\nhello\n", ["there"]]),
    ("alias", alias_fixture())
]

for (name, fixture) in TESTS:
    writer = io.StringIO()
    save(writer, fixture)
    content = writer.getvalue()
    reader = io.StringIO(content)
    print(f"{name}\n{content}")
    result = load(reader)
    assert result == fixture, f"Test failed: {name}"
