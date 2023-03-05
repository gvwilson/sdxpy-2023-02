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
The first raises a RunTime error because the dictionary* is updated WITH NEW KEYS during the for-loop. In the second snippet, the dict's keys are kept constant during iteration and thus no error is thrown. As dicts are unordered, adding new keys would make it possible to have an non-exhaustive traversal of the keys.

*(or dictionarish? I haven't yet understood the parenthesis on slide 13. I checked and type(globals()) is a dict, but this is just the return of the method call and not the inner workings.)
## Counting Results

1.  Modify the test framework so that it reports which tests passed, failed, or had errors
    and also reports a summary of how many tests produced each result.

2.  Write unit tests to check that your answer to part 1 works correctly.

3.  Think of another plausible way to interpret part 1
    that *wouldn't* pass the tests you wrote for part 2.
To be honest, the returning of the dict is a bit of a hack implemented for the meta_test to pass, so my default implementation - which would just print the results - would already fail. The same would be true were the results dict implemented differently - e.g. with a tuple or set instead of a list.
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
