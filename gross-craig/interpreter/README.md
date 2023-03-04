## Defining and Calling Functions

1.  Work through the explanation in the slides (and chapter)
    of how to define a function in our little language
    and then how to call one.
2.  Look at the documentation for Python's `ChainMap` class
    and modify the implementation from the slides to use that
    to manage environments.

### Solution

1. The function to define a function is given in `interpreter.run_def` and the function to call a function is given in `interpreter.run_call`.
The idea is that a `run_def` registers the function and its parameters with the environment given.
To call `run_call` takes the arguments and sets them to the parameters of the given function *in a new environment*.
This environment along with all previously defined ones (see next solution) is used to run the body of the registered function.
2. My solution using `ChainMap` makes a different choice than is specified in the slides.
Rather than only using a local environment and a global environment to run a function in, I collect all previously defined environments in a `ChainMap`.
These `ChainMap`-ed environments are disposed of at the end of a function's run with only the global environment remaining as a standard dictionary.
As a consequence, I can run things like `test_non_global_non_local_variable` that define a variable in a function that a subsequent function call uses.
This doesn't seem like good practice necessarily, but does seem a little simpler of an implementation.
My original implementation that did something similar without using `ChainMap` failed for recursive functions, but the `ChainMap` resolved that issue.
I'm also not sure if there would be a more efficient way to globally manage all environments in a single `ChainMap` rather than discarding nested versions at the end of each function call.

## Arrays

Implement fixed-size one-dimensional arrays:

1.  `["array", 10]` creates an array of 10 elements.
    (If you want to assign it to a variable you could use `["set", "var", ["array", 10]]`.)
2.  Other instructions that you design get and set array elements by index.


### Solution

1. Array creation is implemented in `interpreter.run_array`.
I have made the choice that all arrays contain only integers since that seems to be the most "atomic" thing we've used.
But I don't think it should be too hard to extend to other types.
2. I chose to implement getting and setting array elements under the existing `interpreter.run_get` and `interpreter.run_set` functions.
The way call signature is different though: `["get", "arr", i]` gets `arr[i]` and `["set", "arr", i, val]` sets `arr[i] = val`.
I think the tradeoff here is a slight increase in implementation complexity for a more consistent user experience.
Though I could also see an argument that a separate way to call getting and setting for arrays would reduce bugs.

## While Loops

Implement a `while` loop instruction.
Your implementation can use either a Python `while` loop or recursion.


### Solution
1. I have implemented `while` loops in `interpreter.run_while`.
I decided to use a Python while loop.
Though, as you say, function recursion could do the job, and we have all of the necessary elements built up in our language at this point.
At what point would it make sense to start writing new functionality for our language in our language rather than in Python?
Is there ever a time?
I imagine the performance tradeoffs would be a strong limiting factor.
