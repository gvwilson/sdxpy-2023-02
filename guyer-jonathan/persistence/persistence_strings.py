"""A very simple persistence framework."""

import io
from itertools import islice

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
    escaped = thing.replace("\\", "\\\\")
    escaped = escaped.replace("\n", "\\n")
    print(f"str:{len(escaped)}", file=writer)
    print(escaped, file=writer)

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
    # I can't figure out how to deal with escaped slashes and escaped newlines
    # with global search and replace.
    # I don't think it would be too hard with regexen,
    # but I'm not sure if that's in the spirit of the exercise.
    num_chars = int(value)
    escaped = reader.read(num_chars+1)
    assert escaped[-1] == "\n", "String ended without newline"
    char_iter = islice(escaped[:-1], None)
    parsed = ""
    for char in char_iter:
        if char == "\\":
            next_char = next(char_iter)
            assert next_char in ["\\", "n"], f"Unknown escape sequence \\{next_char}"
            if next_char == "\\":
                parsed += "\\"
            elif next_char == "n":
                parsed += "\n"
        else:
            parsed += char

    return parsed

LOAD = {
    "int": load_int,
    "list": load_list,
    "str": load_str
}

def load(reader):
    line = reader.readline()
    kind, value = line.split(":", maxsplit=1)
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
    ("slashed string", "hello\\there\\"),
    ("double-slashed string", "hello\\\\there\\\\"),
    ("slashed multiline string", "\nhello\\nthere\\\n"),
    ("everything", [17, "\nhello\\n", ["\\\nthere"]])
]

for (name, fixture) in TESTS:
    writer = io.StringIO()
    save(writer, fixture)
    content = writer.getvalue()
    reader = io.StringIO(content)
    result = load(reader)
    print(f"{name}\n{content}")
    assert result == fixture, f"Test failed: {name}"
