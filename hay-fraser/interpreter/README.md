## Defining and Calling Functions

1.  Work through the explanation in the slides (and chapter)
    of how to define a function in our little language
    and then how to call one.

> 🙋‍♂️ **Answer:**
>
> To define, we have to use `"def"`, provide a name, a parameter name, and an instruction (only one). 
> To call, we have to use `"call"`, the name of the function, and the arguments (to match the parameter needed).
    
2.  Look at the documentation for Python's `ChainMap` class
    and modify the implementation from the slides to use that
    to manage environments.

> 🙋‍♂️ **Answer:**
>
> Struggling with this... also running out of available time... I see that `ChainMap` helps update dictionaries... So something like so? (Haven't run)
```python
def env_set(env, name, value):
    assert isinstance(name, str)
    if name in env[0]:
        ChainMap({name: str}, env[0])
    else:
        ChainMap({name: str}, env[-1])
```


## Arrays

Implement fixed-size one-dimensional arrays:

1.  `["array", 10]` creates an array of 10 elements.
    (If you want to assign it to a variable you could use `["set", "var", ["array", 10]]`.)

2.  Other instructions that you design get and set array elements by index.

> 🙋‍♂️ **Answer:**
> 
> Sorry, I've spent a few hours on this and I don't have any remaining. 
>
> Basically I would need to make something like `do_array` that would allow you to specify how big the array would be. It would then initialize an empty array (`[]`) and use a `for` loop to `append` additional empty positions within it, so it ended up the appropriate size. 
>
> I suppose we'd need to make two additional helper functions:
> - `do_array_get` would take two arguments: the array name, and the index you want returned. It would locate the array (`do_get`?) and return the indexed value.
> - `do_array_set` would take three arguments: the array name, the index you want, and the value to encode. It would set that as the value.
> Both would have to ensure that the array named exists (as an array) before making any array-specific commands on it, as well as controlling for index values that don't fit. I suppose in theory you'd be able to encode 'little-language command calls' into such arrays, which is interesting.
    

## While Loops

Implement a `while` loop instruction.
Your implementation can use either a Python `while` loop or recursion.

> 🙋‍♂️ **Answer:**
> 
> Sorry, I've spent a few hours on this and I don't have any remaining. 
>
> This (`do_while`) would take two arguments: the condition (`cond = do(env, args[0]`) to await, and the command(s) to complete for each iteration (`do(env, args[1]`). Probably I'd use a Python loop since I'm still wrapping my head around recursion.
