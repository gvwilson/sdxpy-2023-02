# A Testing Framework: Exercises

## Looping Over `globals`

What happens if you run:

```python
for name in globals():
    print(name)
```

Alex: please see excercise_globals_py, it raises RuntimeError


What happens if you run:

```python
name = None
for name in globals():
    print(name)
```

Alex: please see excercise_globals_py2, it adds dictitem finally

Why? Some pre-agreed behaviour for target vars/dict entries with None content
No other info in python docs (looked definition of for loop and AST doc for AST.for)

## Counting Results

Alex: run_test code is in counting_setup_excercises

1. Modify the test framework so that x reports which tests passed, failed, or had errors
    and also reports a summary of how many tests produced each result.

    Alex: I have extracted a renderer function. But there is still some rendering TODO, if Greg would require
    order of functions, since function names are printed by groups, but actually were executed
    in the order they were in source file.

2. Write unit tests to check that your answer to part 1 works correctly.

    Alex: I've done this by introducing another function run_tests_stats_meta_test to hold test suite
    Actually, I had initially tried to put sample test functions into the same suite as test functions
    but gave up, because of recursions and other problems. For now I decided to call usual test functions and tester
    framework functions using different invocation techniques. Failed to test run_test with run_test :(
    May be Greg hasn't required it and I fell victim of my overinterpretation of requirements.
3. Think of another plausible way to interpret part 1
    that *wouldn't* pass the tests you wrote for part 2.

    Alex: If I just added one more test function, the assert would fail. There should be some way for smarter assert.

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


Alex: done, into test_find.py I added a marked function and adjusted run_tests() in counting_setup_excercises

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

Alex: done, adjusted run_tests() to check and call them exactly once.
Probably there might be a better way to invoke a nullable callable other than
```python
    if setup_func:
        setup_func()
```

