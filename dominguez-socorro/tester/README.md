# A Testing Framework: Exercises

## Looping Over `globals`

What happens if you run:

```python
for name in globals():
    print(name)
```

What happens if you run:

```python
name = None
for name in globals():
    print(name)
```

Why?

First, before running any `for` loop, I would like to take a look at what `globals()` is. `globals()` returns a dictionary with all the available variables. 

When you define `name` as None, you are basically doing:
globals()[name] = None, so you are appending that new variable into your `globals()` dictionary. Because of this, the for loop can run. 

When you run the `for` loop, without having defined `name=None`, you are grabing the `globals` dictionary and checking its length before iterating over it. Then, you proceed to print the name of each key. However, because you are creating a new "temporary" variable called `name` that is appended directly to `globals()[name]` in the first call, you are modifying the dictionary `globals()` and so, are not iterating over the "same" globals where your first iteration happened. 

Even if you did `name=None`, if you reran the `for` loop but now did `name2` instead of `name`, you would face the same problem.

## Counting Results

1.  Modify the test framework so that it reports which tests passed, failed, or had errors and also reports a summary of how many tests produced each result.

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
