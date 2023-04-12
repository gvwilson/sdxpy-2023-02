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

```python
def do_array(env, args):
    """Create fixed-size array.
    ["array", 3] => [None, None, None]
    """
    assert len(args) == 1
    assert isinstance(args[0], int)
    return [None] * args[0]

def do_get(env, args):
    """Get the value of a variable from the most recent environment
    or the global environment.
    ["get" name] => env{name}
    """
    assert len(args) == 1 or len(args) == 2
    if len(args) == 1:
        return env_get(env, args[0])
    else:
        index = args[0]
        return env_get(env, args[1][index])
        
 def do_set(env, args):
    """Assign to a variable.
    ["seq" name expr] => expr # and env{name} = expr
    """
    assert len(args) == 2 or len(args) == 3
    
    name = args[0]
    
    if len(args) == 2:       
        value = do(env, args[1])
        env_set(env, name, value)
    else:
        assert name in env
        index = args[1]
        value = do(env, args[2])
        env_set(env, name, value, index)

def env_get(env, name, index=None):
    assert isinstance(name, str)
    if name in env:
        if not index:
            return env[name]
        else:
            assert isinstance(index, int)
            assert name in env
            assert 0 < index < len(env[name])
            return env[name][index]
    assert False, f"Unknown variable {name}"
    
def env_set(env, name, value, index=None):
    assert isinstance(name, str)
    if not index:
        env[name] = value
    else:
        assert isinstance(index, int)
        assert name in env
        assert 0 < index < len(env[name])
        env[name][index] = value
```

## While Loops

Implement a `while` loop instruction.
Your implementation can use either a Python `while` loop or recursion.

```python
def do_while(env, args):
    """While loop.
    ["while", A, B] => while A then B
    """   
    assert len(args) == 2
    cond = args[0]
    loop = args[1]
    while do(env, cond):        
        value = do(env, loop)
        
    return value
```
