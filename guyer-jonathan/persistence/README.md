# Persistence

1.  Please use the code in this directory as a starting point for your exercises.

2.  Please do each exercise independently (i.e., don't put aliasing on top of `globals()` or vice versa).

## Using Globals

The lesson on unit testing introduced the function `globals`,
which can be used to look up everything defined at the top level of a program.

1.  Modify the persistence framework so that it looks for `save_` and `load_` functions using `globals`.

1.  Why is this a bad idea?

**This approach finds everything starting with `save_` and `load_`, whether or not they're related to this
task and whether or not they're even functions. For instance, any injudicious imports of anything named 
`save_` and `load_` will be included.**

## Aliasing

1.  Read the section on aliasing (https://third-bit.com/sdxpy/persistence/#persistence-aliasing).

2.  Modify the functions to handle aliases.
    (You may need to give the `save_*` and `load_*` functions another parameter
    to keep track of the objects seen so far.)

## Strings

Modify the framework so that strings are stored using escape characters like `\n`
instead of being split across several lines.
