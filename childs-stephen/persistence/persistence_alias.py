"""A very simple persistence framework."""

import io


def save_int(writer, thing, seen):
    assert isinstance(thing, int)
    thing_id = id(thing)
    print(f"int:{thing_id}:{thing}", file=writer)


def save_list(writer, thing, seen):
    assert isinstance(thing, list)
    thing_id = id(thing)
    print(f"list:{thing_id}:{len(thing)}", file=writer)
    for item in thing:
        save(writer, item, seen)


def save_str(writer, thing, seen):
    assert isinstance(thing, str)
    thing_id = id(thing)
    lines = thing.split("\n")
    print(f"str:{thing_id}:{len(lines)}", file=writer)
    for ln in lines:
        print(ln, file=writer)


SAVE = {"int": save_int, "list": save_list, "str": save_str}


def save(writer, thing, seen):
    thing_id = id(thing)
    if thing_id in seen:
        print(f"alias:{thing_id}:", file=writer)
        return
    seen.add(id(thing))
    typename = type(thing).__name__
    assert typename in SAVE, f"Unknown type {typename}"
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


LOAD = {"int": load_int, "list": load_list, "str": load_str}


def load(reader, seen):
    kind, ident, value = reader.readline().split(":", maxsplit=2)
    if kind == "alias":
        assert ident in seen
        return seen[ident]
    assert kind in LOAD, f"Unknown kind {kind}"
    func = LOAD[kind]
    result = func(reader, value, seen)
    seen[ident] = result
    return result


test_list = [17, 18, 19]

TESTS = [
    ("plain integer", 5),
    ("empty list", []),
    ("flat list", [88, 99, 100]),
    ("nested list", [17, 18, [19]]),
    ("plain string", "hello"),
    ("multiline string", "hello\nthere\n"),
    ("everything", [17, "\nhello\n", ["there"]]),
    ("same int twice", [17, 17, 18]),
    ("same string twice", ["shared", "shared"]),
    ("same list twice", [test_list, test_list, [17, 18, 20]]),
]

for name, fixture in TESTS:
    save_seen = set()
    load_seen = {}
    writer = io.StringIO()
    save(writer, fixture, save_seen)
    content = writer.getvalue()
    reader = io.StringIO(content)
    result = load(reader, load_seen)
    print(f"{name}\n{content}")
    assert result == fixture, f"Test failed: {name}"
