# Persistence

1.  Please use the code in this directory as a starting point for your exercises.

2.  Please do each exercise independently (i.e., don't put aliasing on top of `globals()` or vice versa).

## Using Globals

The lesson on unit testing introduced the function `globals`,
which can be used to look up everything defined at the top level of a program.

1.  Modify the persistence framework so that it looks for `save_` and `load_` functions using `globals`.

- Modifications are in `persistence-globals.py`

1.  Why is this a bad idea?

- Using `globals()` violates the open-closed principle of object-oriented programming

## Aliasing

1.  Read the section on aliasing (https://third-bit.com/sdxpy/persistence/#persistence-aliasing).

2.  Modify the functions to handle aliases.
    (You may need to give the `save_*` and `load_*` functions another parameter
    to keep track of the objects seen so far.)

- Need some extra time to work on this question 

## Strings

Modify the framework so that strings are stored using escape characters like `\n`
instead of being split across several lines.

- Modifications are in `persistence-str.py`
