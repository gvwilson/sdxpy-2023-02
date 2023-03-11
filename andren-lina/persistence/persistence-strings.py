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

# modified save_str so that strings are saved as one string but with \n inserted instead of newlines 
# note: this solution doesnt work if string contains literally '\\n'. escaping escaping escaping. 
def save_str(writer, thing):
    assert isinstance(thing, str)
    lines = thing.split("\n")
    string_to_save = lines[0]
    for ln in lines[1:]:
        string_to_save = string_to_save + '\\n' + ln
    print("str:",string_to_save, sep='', file=writer)

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

# modified load_str to work with long string including newlines below
def load_str(reader, value):
    lines = "\n".join(str(value.rstrip("\n")).split("\\n"))
    return lines

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
    #    ("daniels dumma test", "hello\\nhello")
]

for (name, fixture) in TESTS:
    writer = io.StringIO()
    save(writer, fixture)
    content = writer.getvalue()
    reader = io.StringIO(content)
    result = load(reader)
    print(f"{name}\n{content}")
    assert result == fixture, f"Test failed: {name}"
