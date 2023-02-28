## Defining and Calling Functions

1.  Work through the explanation in the slides (and chapter)
    of how to define a function in our little language
    and then how to call one.
    
**Answer:**
Both of env and aug are required as input to define and call a function in our little language. 
    
There should be 3 parts of aug to define a function, first one is the name of function, the second is parameters the function will take (which could be None), the third is the body (instruction with operations in our little language) of the function. 
    
There should be at least one part of aug to call a function, which is the function name in global environment. If the function takes parameters, they should be included as the rest parts of aug.
    

2.  Look at the documentation for Python's `ChainMap` class
    and modify the implementation from the slides to use that
    to manage environments.
    
 ```python
from collections import ChainMap
import sys

def env_get(env, name):
    assert isinstance(name, str)
    if name in env:
        return env[name]
    assert False, f"Unknown variable {name}"
    
def env_set(env, name, value):
    assert isinstance(name, str)
    env[name] = value


def main():
    chain = ChainMap()
    result = do(chain, operations)
    print(f"=> {result}")
 ```

## Arrays

Implement fixed-size one-dimensional arrays:

1.  `["array", 10]` creates an array of 10 elements.
    (If you want to assign it to a variable you could use `["set", "var", ["array", 10]]`.)
2.  Other instructions that you design get and set array elements by index.

## While Loops

Implement a `while` loop instruction.
Your implementation can use either a Python `while` loop or recursion.
