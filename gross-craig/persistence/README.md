# Persistence

1.  Please use the code in this directory as a starting point for your exercises.

2.  Please do each exercise independently (i.e., don't put aliasing on top of `globals()` or vice versa).

## Using Globals

The lesson on unit testing introduced the function `globals`,
which can be used to look up everything defined at the top level of a program.

1.  Modify the persistence framework so that it looks for `save_` and `load_` functions using `globals`.

1.  Why is this a bad idea?

### Solution

1. This is implemented by the `type_mapping` function in `persistence_globals.py` by looking through the `globals()` dict for functions starting with the specified prefix (`save_` or `load_`), removing the prefix for the type name, and constructing the specified mapping.
2. 

## Aliasing

1.  Read the section on aliasing (https://third-bit.com/sdxpy/persistence/#persistence-aliasing).

2.  Modify the functions to handle aliases.
    (You may need to give the `save_*` and `load_*` functions another parameter
    to keep track of the objects seen so far.)

## Strings

Modify the framework so that strings are stored using escape characters like `\n`
instead of being split across several lines.
