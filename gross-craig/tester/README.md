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

### Solution:

In the first case, there is a `RuntimeError`. 
Before the loop, the variable `name` did not exist and is therefore not in `globals()`.
However, after starting, `name` is defined and `globals()` (which is being iterated over) grows to include it.
This changes the size of the dictionary which results in the runtime error.

In the second case, `name` is already defined and added to `globals()` before starting the loop. Thus, `globals()` does not change and continues printing all of the variable names in `globals()` as desired.

I didn't know that modifying dictionaries while iterating over them resulted in a `RuntimeError`.
I can't quite figure out though why I can append to a list in that I'm looping over (even though I know you're not supposed to!) without error, while the same thing errors out with a dictionary. 

## Counting Results

1.  Modify the test framework so that it reports which tests passed, failed, or had errors
    and also reports a summary of how many tests produced each result.

2.  Write unit tests to check that your answer to part 1 works correctly.

3.  Think of another plausible way to interpret part 1
    that *wouldn't* pass the tests you wrote for part 2.

### Solution:

The code for (1) is in `tester.py` (in addition to subsequent modifications).
The code for (2) is in `test_tester.py` and should be run using `pytest` via `pytest test_tester.py`.

As for (3), we could consider a test that had multiple assert statements (like `fixture_test_negative_wrong` in `test_tester.test_summary_pass_fail_error`).
Currently, the whole test is considered failing if only one assert failed.
But the summary could count each of the tests separate assertions' passes, fails, or errors separately.

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


### Solution

The code is contained in `tester.py`.
In particular the `test_negative_wrong_test_assert` test passes, despite the same test without `"test:assert"` as its docstring (`test_negative_wrong`) failing.

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

### Solution

The code is contained in `tester.py`.
In particular, the `numbers` fixture is created in the `setup` function which is used in the `test_setup` test.
The `teardown` function prints `tearing down!` rather than doing anything interesting.
