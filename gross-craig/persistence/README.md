# Persistence

1.  Please use the code in this directory as a starting point for your exercises.

2.  Please do each exercise independently (i.e., don't put aliasing on top of `globals()` or vice versa).

## Using Globals

The lesson on unit testing introduced the function `globals`,
which can be used to look up everything defined at the top level of a program.

1.  Modify the persistence framework so that it looks for `save_` and `load_` functions using `globals`.

1.  Why is this a bad idea?

### Solution

1. This is implemented by the `type_mapping` function in
   `persistence_globals.py` by looking through the `globals()` dict for
   functions starting with the specified prefix (`save_` or `load_`), removing
   the prefix for the type name, and constructing the specified mapping.
2. Any function in scope starting with `save_` or `load_` (which would be pretty
   common function prefixes) would be registered with the global `save`/`load`
   functions. In particular, an overzealous `from module import *` could result
   in inadvertent, non-functioning save/load capabilities.

   However, upon reflection, I'm not sure how likely this would be to cause
   bugs. I'm having some trouble finding the answer to what "scope" is
   considered in `globals`, but it's just the things defined/imported in the
   file `persistence_globals.py` and nothing else (e.g., a file that imports
   `persistence_globals` wouldn't pollute the persistence version of `globals`),
   then this would theoretically be avoidable, so long as intra-file imports and
   the titling of functions with `save_` and `load_` are carefully managed.

   That said, it's still probably better to explicitly register functions so
   that future contributors will be more alert to this and not add an errant
   `save_*` helper function by mistake.

## Aliasing

1.  Read the section on aliasing (https://third-bit.com/sdxpy/persistence/#persistence-aliasing).

2.  Modify the functions to handle aliases.
    (You may need to give the `save_*` and `load_*` functions another parameter
    to keep track of the objects seen so far.)

### Solution

This is implemented in `persistence_alias.py`. I chose to use a global
(default)dict to store the `id`s of variables that have been previously seen in
the saving or loading processes, where each reader/writer used has its own
store of aliased variables. This mimics the OOP-design in the text (which I
would prefer in a real implementation) without changing the API used in the
tests at the end.

## Strings

Modify the framework so that strings are stored using escape characters like `\n`
instead of being split across several lines.

### Solution

This is implemented in `persistence_string`. By replacing all `\n` with `\\n`
in the save step (and vice versa in the load step) for strings, newlines are
only printed to separate lines as necessary by the persistence framework.
