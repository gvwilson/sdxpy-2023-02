# A Testing Framework: Exercises

## Looping Over `globals`

What happens if you run:

```python
for name in globals():
    print(name)
```
> 🙋‍♂️ **Answer:**
>
> Python (well, at least, my install) will seemingly error out: `RuntimeError: dictionary changed size during iteration`.

What happens if you run:

```python
name = None
for name in globals():
    print(name)
```
> 🙋‍♂️ **Answer:**
>
> Python lists all the objects in the global environment, including a `name` variable.

Why?

> 🙋‍♂️ **Answer:**
>
> In the first case, this is because we've asked Python to list all the objects in the global environment, but as soon as we start iterating, we've changed the system. Kind of like quantum physics, I guess. As soon as you run it, and the error is thrown, `name` shows up in my environment, since it was assigned in the first iteration. In the second case, we've already adjusted the global environment to include `name`, so no changes are registered, and the loop proceeds.

## Counting Results

1.  Modify the test framework so that it reports which tests passed, failed, or had errors
    and also reports a summary of how many tests produced each result.


> 🙋‍♂️ **Answer:**
```
def classify(func):
    if hasattr(func, "skip") and func.skip:
        return "skip"
    if hasattr(func, "fail") and func.fail:
        return "fail"
    return "run"
def run_tests(prefix):
    all_names = [n for n in globals() if n.startswith(prefix)]
    passed = 0
    fail = 0
    error = 0
    for name in all_names:
        func = globals()[name]
        kind = classify(func)
        try:
            if kind == "skip":
                print(f"skip: {name}")
            else:
                func()
                print(f"pass: {name}")
                passed += 1
        except AssertionError as e:
            if kind == "fail":
                print(f"pass (expected failure): {name}")
                fail += 1  # Though unsure if this should count if it's expected?
            else:
                print(f"fail: {name} {str(e)}")
                fail += 1
        except Exception as e:
            print(f"error: {name} {str(e)}")
            error += 1
    print(f"\nTest Summary:\n--------------\nPass: {str(passed)}\nFail: {str(fail)}\nError: {str(error)}")
```

2.  Write unit tests to check that your answer to part 1 works correctly.


> 🙋‍♂️ **Answer:**
```
def test_sign_positive2():
    assert sign(2) == 1
def test_sign_positive3():
    assert sign(21) == 1
def test_sign_random(): # Live dangerously! Possibly a bad idea though since I won't know what it was *supposed* to be...
    import random
    assert sign(random.randrange(-1,1)) == 1
```

3.  Think of another plausible way to interpret part 1
    that *wouldn't* pass the tests you wrote for part 2.

> 🙋‍♂️ **Answer:**
>
> I'm struggling with this one... I mean I could break the code any number of ways - removing the pass condition, making it check for a non-existent attribute, etc. I can't think of a way of doing it that would be productive...

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


> 🙋‍♂️ **Answer:**
```
def run_tests(prefix):
    all_names = [n for n in globals() if n.startswith(prefix)]
    passed = 0
    fail = 0
    error = 0
    for name in all_names:
        func = globals()[name]
        kind = classify(func)
        else:    
            try:
                if kind == "skip":
                    print(f"skip: {name}")
                else:
                    func()
                    if help(func) == "test:assert":
                        print(f"fail (expected assertion error but did not return): {name} {str(e)}")
                        fail += 1
                    else:
                        print(f"pass: {name}")
                        passed += 1
            except AssertionError as e:
                if help(func) == "test:assert":
                    print(f"pass (assertion error expected and returned): {name}")
                    passed += 1
                elif kind == "fail":
                    print(f"pass (expected failure): {name}")
                    passed += 1
                else:
                    print(f"fail: {name} {str(e)}")
                    fail += 1
            except Exception as e:
                print(f"error: {name} {str(e)}")
                error += 1
    print(f"\nTest Summary:\n--------------\nPass: {str(passed)}\nFail: {str(fail)}\nError: {str(error)}")
```
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

> 🙋‍♂️ **Answer:**
>
> (Going to describe rather than code due to time constraints) The testing function would allow you to specify a file, which it would attempt to load. I'm assuming that loading the file enumerates the contained functions into either the `locals` or `globals` environment, which we can then check to see if there was a `setup` function. If so, we would give it a run before proceeding. Same idea at the end of the line with `teardown`.
