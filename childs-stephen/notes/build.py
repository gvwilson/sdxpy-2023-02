# first goal: figure out what depends on what

dependencies = {
    "final.txt": ["left.txt", "right.txt"],
    "right.txt": ["start.txt"],
    "left.txt": ["start.txt"],
    "start.txt": [],
}


def check_dependencies(deps):
    pass
