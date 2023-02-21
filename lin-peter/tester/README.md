# A Testing Framework: Exercises

## Looping Over `globals`

What happens if you run:

```python
for name in globals():
    print(name)
```
You get:
```commandline
__name__
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
RuntimeError: dictionary changed size during iteration
```


What happens if you run:

```python
name = None
for name in globals():
    print(name)
```
You get:
```commandline
__name__
__doc__
__package__
__loader__
__spec__
__annotations__
__builtins__
name
```
Why?

- Python `globals()` method returns a dictionary with all global variables.
- Without declaring what `name` variable is before iterating over the key-value pairs in `globals()`, the `name` 
variable in for loop gets assigned dynamically and triggers the dictionary size change error when the for loop is executed.
- With `name` variable declared before iterating over the key-value pairs in `globals()`, the `name` 
variable in for loop behaves like a placeholder and gets assigned dynamically. 
However, the `name` variable at the `globals()` is already declared so it does not affect the `name` variable in the for loop.



## Counting Results

1.  Modify the test framework so that it reports which tests passed, failed, or had errors
    and also reports a summary of how many tests produced each result.

2.  Write unit tests to check that your answer to part 1 works correctly.

3.  Think of another plausible way to interpret part 1
    that *wouldn't* pass the tests you wrote for part 2.

## Failing on Purpose

Putting assertions into code to check that it is behaving correctly
is called __defensive programming__.
It's a good practice,
but we should make sure those assertions are failing when they're supposed to,
just as we should test our smoke detectors every once in a while.

Modify the tester so that
if a test function's docstring is `"test:assert"`,
the test passes if it raises an `AssertionError`
and fails if it does not.
Tests whose docstring don't contain `"test:assert"`
should behave as before.

---

class: exercise

## Setup and Teardown

Testing frameworks often allow programmers to specify a `setup` function
that is to be run before each test
and a corresponding `teardown` function
that is to be run after each test.
(`setup` usually re-creates complicated test fixtures,
while `teardown` functions are sometimes needed to clean up after tests,
e.g., to close database connections or delete temporary files.)

Modify the testing tool in this chapter so that
if a file of tests contains a function called `setup`
then the tool calls it exactly once before running each test in the file.
Add a similar way to register a `teardown` function.
