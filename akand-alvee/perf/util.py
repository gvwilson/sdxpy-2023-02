def all_eq(*values):
    """Check that all values in a list are the same."""
    return (not values) or all(v == values[0] for v in values)

def dict_match(d, prototype):
    """Check that all dictionaries match a prototype dictionary.

    Two dictionaries match if they have the same keys and if the
    types of the values associated with each key are the same.
    (The values themselves don't have to be the same, just the types.)
    """
    if set(d.keys()) != set(prototype.keys()):
        return False
    return all(type(d[k]) == type(prototype[k]) for k in d)
