# Persistence

1.  Please use the code in this directory as a starting point for your exercises.

2.  Please do each exercise independently (i.e., don't put aliasing on top of `globals()` or vice versa).

## Using Globals

The lesson on unit testing introduced the function `globals`,
which can be used to look up everything defined at the top level of a program.

1.  Modify the persistence framework so that it looks for `save_` and `load_` functions using `globals`.

1.  Why is this a bad idea?

For several reasons: someone could use the modified framework to execute malicious code by calling it a name starting with "save" or "load"; if the modified framework looks for functions in globals in addition to using the existing LOAD and SAVE dictionaries, a function in globals could potentially clobber one of the existing functions; if the modified framework replaces the existing dictionaries and relies entirely on checking globals, you might not have defined all the functions you need for the various types of data you're trying to load and save; and, simply finding a relevant function in globals doesn't indicate the type of data it is intended to hold (though you could specify the intended type in the documentation and check for that if you insisted on going this route).

## Aliasing

1.  Read the section on aliasing (https://third-bit.com/sdxpy/persistence/#persistence-aliasing).

2.  Modify the functions to handle aliases.
    (You may need to give the `save_*` and `load_*` functions another parameter
    to keep track of the objects seen so far.)

## Strings

Modify the framework so that strings are stored using escape characters like `\n`
instead of being split across several lines.
