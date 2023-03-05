---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.4
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Week 1 Exercises

+++ {"tags": []}

## Looping Over `globals`

What happens if you run:

```python
for name in globals():
    print(name)
```

+++

> The first time I run it in a Jupyter Notebook (before running any cells), I get the following message:

```{code-cell} ipython3
for name in globals():
    print(name)
```

What happens if you run:

```python
name = None
for name in globals():
    print(name)
```

+++

> The second time I run it, or if I set `name = None`, I get:

```{code-cell} ipython3
name = None
for name in globals():
    print(name)
```

Why?

+++

> I think this is happening because `globals()` is empty (and doesn't contain `name`), but during the loop, name gets created and thus changes `globals()`. This makes sense because `globals()` is accessed first, then `name` gets created and then `globals()` is iterated over.
> 
> Interestingly, if you do the same in a list comprehension, the error doesn't happen, presumably because `name` gets created first (or gets assigned a Null value) and then globals gets created.

```{code-cell} ipython3
del name

[name for name in globals()]
```

> According to the [Python docs](https://docs.python.org/3/library/stdtypes.html#dictionary-view-objects), the objects returned with `.items()` are "view objects" and "iterating views while adding or deleting entries in the dictionary may raise a RuntimeError or fail to iterate over all entries."

## Counting Results

1. Modify the test framework so that it reports which tests passed, failed, or had errors and also reports a summary of how many tests produced each result.

```{code-cell} ipython3
# Should return 0 when given 0


def sign(value):
    if value < 0:
        return -1
    else:
        return 1


def test_sign_negative():
    assert sign(-3) == -1


def test_sign_positive():
    assert sign(19) == 1


def test_sign_zero():
    assert sign(0) == 0


# Misspelled 'sign'
def test_sign_error():
    assert sgn(1) == 1


def process_results(results):

    # Reformat every element of each list (pass, fail, error) of tests

    return {k: [f"\n\t- {l}" for l in v] for k, v in results.items()}


def run_tests(all_tests):
    results = {"pass": [], "fail": [], "error": []}
    for test in all_tests:
        try:
            test()
            results["pass"].append(test.__name__)
        except AssertionError:
            results["fail"].append(test.__name__)
        except Exception:
            results["error"].append(test.__name__)

    p_results = process_results(results)

    for res in p_results.keys():
        print(f"{len(p_results[res])} tests {res}ed:" + "".join(p_results[res]))

    # Is it a good idea to return the results dictionary in the `run_tests` function?

    return results


TESTS = [test_sign_negative, test_sign_positive, test_sign_zero, test_sign_error]

run_tests(TESTS)
```

2. Write unit tests to check that your answer to part 1 works correctly.

> I had to refactor my answer to #1 so that it returned the `results` dictionary and I could compare the output in the unit test.
> I didn't think it would be a good idea to match string formatting as part of the unit test to check if the `run_tests()` function is running correctly.

```{code-cell} ipython3
def test_run_tests(all_tests):

    res_dict = {
        "pass": ["test_sign_negative", "test_sign_positive"],
        "fail": ["test_sign_zero"],
        "error": ["test_sign_error"],
    }

    assert res_dict == run_tests(all_tests)


test_run_tests(TESTS)
```

3. Think of another plausible way to interpret part 1 that *wouldn't* pass the tests you wrote for part 2.

+++

> Hmm, I had a hard time with this question. I suppose if there was one fewer, or one additional test added to `TESTS`, then the test I wrote would fail.

+++

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

```{code-cell} ipython3
def test_check_assert():
    """
    test:assert
    """

    assert sign(19) == 0


def run_tests(all_tests):
    results = {"pass": [], "fail": [], "error": []}
    for test in all_tests:
        try:
            test()
            results["pass"].append(test.__name__)
        except AssertionError:

            # TODO: I don't understand why `getattr(test_sign_negative, "__doc__", "NA")` returns a `NoneType`!

            doc = test.__doc__

            if doc and "test:assert" in doc:
                results["pass"].append(test.__name__)
            else:
                results["fail"].append(test.__name__)
        except Exception:
            results["error"].append(test.__name__)

    p_results = process_results(results)

    for res in p_results.keys():
        print(f"{len(p_results[res])} tests {res}ed:" + "".join(p_results[res]))

    # Is it a good idea to return the results dictionary in the `run_tests` function?

    return results


TESTS = [
    test_check_assert,
    test_sign_negative,
    test_sign_positive,
    test_sign_zero,
    test_sign_error,
]

results = run_tests(TESTS)
```

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

+++

### Attempt 1: local tests

```{code-cell} ipython3
def setup():

    print("I have done some complicated setup!")


def teardown():
    print("I have undone the complicated teardown!")


def run_tests(all_tests):
    results = {"pass": [], "fail": [], "error": []}

    # Check to see if `setup()` and `teardown()` exist
    setup_chk = [test for test in all_tests if test.__name__ == "setup"]
    teardown_chk = [test for test in all_tests if test.__name__ == "teardown"]

    for test in all_tests:

        if setup_chk:
            setup()

        try:
            test()
            results["pass"].append(test.__name__)
        except AssertionError:

            doc = test.__doc__

            if doc and "test:assert" in doc:
                results["pass"].append(test.__name__)
            else:
                results["fail"].append(test.__name__)
        except Exception:
            results["error"].append(test.__name__)

        if teardown_chk:
            teardown()

    p_results = process_results(results)

    for res in p_results.keys():
        print(f"{len(p_results[res])} tests {res}ed:" + "".join(p_results[res]))

    # Is it a good idea to return the results dictionary in the `run_tests` function?

    return results


TESTS = [
    setup,
    teardown,
    test_check_assert,
    test_sign_negative,
    test_sign_positive,
    test_sign_zero,
    test_sign_error,
]

results = run_tests(TESTS)
```

### Attempt 2: tests from a file

```{code-cell} ipython3
import pathlib
from importlib.machinery import SourceFileLoader

for (i, file) in enumerate(pathlib.Path("./").glob("test*.py")):

    m = SourceFileLoader(f"m{i}", str(file)).load_module()

    # Check to see if `setup()` and `teardown()` exist
    setup_chk = [t for t in dir(m) if t == "setup"]
    teardown_chk = [t for t in dir(m) if t == "teardown"]

    results = {"pass": [], "fail": [], "error": []}

    for name in dir(m):

        if not name.startswith("test_"):
            continue

        test = getattr(m, name)

        if setup_chk:
            setup = getattr(m, setup_chk[0])
            setup()

        try:
            test()
            results["pass"].append(test.__name__)
        except AssertionError:

            # TODO: I don't understand why `getattr(test_sign_negative, "__doc__", "NA")` returns a `NoneType`!

            doc = test.__doc__

            if doc and "test:assert" in doc:
                results["pass"].append(test.__name__)
            else:
                results["fail"].append(test.__name__)
        except Exception:
            results["error"].append(test.__name__)

        if teardown_chk:
            teardown = getattr(m, teardown_chk[0])
            teardown()

    p_results = process_results(results)

    for res in p_results.keys():
        print(f"{len(p_results[res])} tests {res}ed:" + "".join(p_results[res]))
```
