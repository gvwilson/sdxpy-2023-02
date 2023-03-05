## Defining and Calling Functions

1.  Work through the explanation in the slides (and chapter)
    of how to define a function in our little language
    and then how to call one.
    
**ANS**

In order to define a function, we must store under a unique identifier for the function:
- the expected arguments for the function, 
- and the actions to take when the function is called

In order to call a function, we must:
- locate the stored function definition by name,
- assign values to the expected arguments,
- perform the stored actions, in a local context with the assigned argument values

2.  Look at the documentation for Python's `ChainMap` class
    and modify the implementation from the slides to use that
    to manage environments.

## Arrays

Implement fixed-size one-dimensional arrays:

1.  `["array", 10]` creates an array of 10 elements.
    (If you want to assign it to a variable you could use `["set", "var", ["array", 10]]`.)
2.  Other instructions that you design get and set array elements by index.

## While Loops

Implement a `while` loop instruction.
Your implementation can use either a Python `while` loop or recursion.
