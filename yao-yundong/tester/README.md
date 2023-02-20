# A Testing Framework: Exercises

## Looping Over `globals`

What happens if you run:

```python
for name in globals():
    print(name)
```

**Answer:**
```
RuntimeError: dictionary changed size during iteration
```

What happens if you run:

```python
name = None
for name in globals():
    print(name)
```

Why?

**Answer:**
If you has not defined the variable **name** before looping the dictionary **globals()**, it would define (create) **name** at the first step of for looping, that could change the size of **global()** dictionary and cause error.
So defining (creating) the variable **name** as *None* at the beginning could fix the size of dictionary and avoid this error.

## Counting Results

1.  Modify the test framework so that it reports which tests passed, failed, or had errors
    and also reports a summary of how many tests produced each result.
    
    
**Function and Tests:**
```python
def sign(value):
    if value < 0:
        return -1
    else:
        return 1

def test_sign_negative():
    assert sign(-3) == -1
test_sign_negative.skip = True

def test_sign_positive():
    assert sign(19) == 1

def test_sign_zero():
    assert sign(0) == 0
test_sign_zero.fail = True

def test_sign_error():
    assert sgn(1) == 1
```

**Test framework:**
```python
def classify(func):
    if hasattr(func, "skip") and func.skip:
        return "skip"
    if hasattr(func, "fail") and func.fail:
        return "fail"
    return "run"
    
 
def run_tests(prefix):
    all_names = [n for n in globals() if n.startswith(prefix)]
    results = {"pass": 0, "fail": 0, "error": 0}
    for name in all_names:
        func = globals()[name]
        kind = classify(func)
        try:
            if kind == "skip":
                print(f"skip: {name}")
            else:
                func()
                results["pass"] += 1
                print(f"pass: {name}")
        except AssertionError as e:
            results["fail"] += 1
            if kind == "fail":
                print(f"pass (expected failure): {name}")
            else:
                print(f"fail: {name} {str(e)}")
        except Exception as e:
            results["error"] += 1
            print(f"error: {name} {str(e)}")
    for (kind, count) in results.items():
        print(f"{kind}: {count}")
        
    return results    

run_tests("test_")
```

**Output:**
```
skip: test_sign_negative
pass: test_sign_positive
pass (expected failure): test_sign_zero
error: test_sign_error name 'sgn' is not defined
pass: 1
fail: 1
error: 1
```

2.  Write unit tests to check that your answer to part 1 works correctly.

```python
def check_test_frame():
    results = run_tests("test_")
    
    assert results['pass'] == 1
    assert results['fail'] == 1
    assert results['error'] == 1
    
    
check_test_frame()
```

3.  Think of another plausible way to interpret part 1
    that *wouldn't* pass the tests you wrote for part 2.
    
```python
def run_tests(prefix):
    all_names = [n for n in globals() if n.startswith(prefix)]
    results = {"pass": 1, "fail": 2, "error": 3}  # Modified line
    for name in all_names:
        func = globals()[name]
        kind = classify(func)
        try:
            if kind == "skip":
                print(f"skip: {name}")
            else:
                func()
                results["pass"] += 1
                print(f"pass: {name}")
        except AssertionError as e:
            results["fail"] += 1
            if kind == "fail":
                print(f"pass (expected failure): {name}")
            else:
                print(f"fail: {name} {str(e)}")
        except Exception as e:
            results["error"] += 1
            print(f"error: {name} {str(e)}")
    for (kind, count) in results.items():
        print(f"{kind}: {count}")
        
    return results
 ```

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
```python
TEST_ASSERT = "test:assert"

def test_sign_negative():
    "test:skip"
    assert sign(-3) == -1

def test_sign_positive():
    assert sign(19) == 1

def test_sign_zero():
    "test:assert"
    assert sign(0) == 0

def test_sign_error():
    """Expect an error."""
    assert sgn(1) == 1
    
def run_tests(prefix):
    all_names = [n for n in globals() if n.startswith(prefix)]
    for name in all_names:
        func = globals()[name]
        try:
            func()
            print(f"pass: {name}")
        except AssertionError as e:
            if TEST_ASSERT in func.__doc__:
                print(f"pass (expected assert): {name}")
            else:
                print(f"fail: {name} {str(e)}")
        except Exception as e:
            doc = f"/{func.__doc__}" if func.__doc__ else ""
            print(f"error: {name}{doc} {str(e)}")

run_tests("test_")
```

**Output:**
```
pass: test_sign_negative
pass: test_sign_positive
pass (expected assert): test_sign_zero
error: test_sign_error/Expect an error. name 'sgn' is not defined
```
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

```python
def run_tests(prefix):
    if "setup" in globals():  # check setup function
        setup()
    all_names = [n for n in globals() if n.startswith(prefix)]
    for name in all_names:
        func = globals()[name]
        try:
            func()
            print(f"pass: {name}")
        except AssertionError as e:
            if TEST_ASSERT in func.__doc__:
                print(f"pass (expected assert): {name}")
            else:
                print(f"fail: {name} {str(e)}")
        except Exception as e:
            doc = f"/{func.__doc__}" if func.__doc__ else ""
            print(f"error: {name}{doc} {str(e)}")
            
    if "teardown" in globals(): # check teardown function:
        teardown()

run_tests("test_")
```
