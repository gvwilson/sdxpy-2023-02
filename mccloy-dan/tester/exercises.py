"""
Looping over `globals`
======================
In a fresh python interpreter, this:

    for name in globals():
        print(name)

fails with a `RuntimeError` (dictionary changed size during iteration), because
when running the first line, `globals()` is executed first, then the variable
`name` is assigned to point to the first key in `globals()`. When that second
step occurs, `name` is itself added to `globals()`, thereby changing the
dictionary size. Pre-assigning something to the variable `name` (as in the
second example) puts `name` into `globals()` *before* `globals()` is evaluated
during loop initialization, so the loop runs fine (the *value* of `name`
changes on each iteration, but the *existence of the key `name`* is there from
the start, so the dictionary size doesn't change).
"""


# Counting results
# ================


def sign(value):
    """This function intentionally handles zero incorrectly."""
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


def test_sign_error():
    """This test intentionally calls an undefined function `sgn`."""
    assert sgn(1) == 1  # noqa F821


test_sign_negative.skip = True
test_sign_zero.fail = True


def classify(func):
    if hasattr(func, "skip") and func.skip:
        return "skip"
    if hasattr(func, "fail") and func.fail:
        return "fail"
    return "run"


# Counting results, part 1
# ------------------------

def report_test_results(results):
    summary = dict()
    pad = max(len(x) for x in list(results) + ['summary'])
    # sort by key so we can test accurate reporting while being agnostic about
    # the order in which tests are run
    sorted_results = dict(sorted(results.items()))
    for key, val in sorted_results.items():
        print(f"{key:>{pad}}: {val}")
        summary[key] = len(val)
    print(f"summary: {summary}")


# Counting results, part 2
# ------------------------

def test_reporting():
    from contextlib import redirect_stdout
    from io import StringIO

    result_kinds = ['pass', 'fail', 'skip', 'xfail', 'error']
    pad = max(len(x) for x in result_kinds + ['summary'])
    fake_results = {kind: list() for kind in sorted(result_kinds)}
    fake_summary = {kind: 0 for kind in fake_results}
    expected = "\n".join(f"{kind:>{pad}}: []" for kind in fake_results)
    expected += f"\n{'summary':<{pad}}: {repr(fake_summary)}\n"
    actual = StringIO()
    with redirect_stdout(actual):
        report_test_results(fake_results)
    assert actual.getvalue() == expected


# Counting results, part 3
# ------------------------
"""
If the reporting step were, say, generating an HTML report, then presumably it
wouldn't be going to stdout, so its content wouldn't be captured for comparison
with `expected`. Moreover, even if the HTML report *were* sent to stdout, the
test would still fail because of how `expected` is defined.
"""


# Failing on purpose
# ==================

def test_docstring():
    """test:assert"""
    raise AssertionError


# Setup and teardown
# ==================

def run_tests(prefix):
    from collections import defaultdict

    # cache setup/teardown
    def default_setup():
        pass

    def default_teardown():
        pass

    setup = globals().get("setup", default_setup)
    teardown = globals().get("teardown", default_teardown)

    # find tests
    all_names = [n for n in globals() if n.startswith(prefix)]
    # init results
    results = defaultdict(list)
    # run tests
    for name in all_names:
        func = globals()[name]
        kind = classify(func)
        try:
            if kind == "skip":
                results['skip'] += [name]
            else:
                setup()
                func()
                results['pass'] += [name]
                teardown()
        except AssertionError as e:
            if func.__doc__ == "test:assert":
                results['pass'] += [name]
            elif kind == "fail":
                results['xfail'] += [name]
            else:
                results['fail'] += [f"{name} ({str(e)})"]
        except Exception as e:
            results['error'] += [f"{name} ({str(e)})"]
    # show results
    report_test_results(results)
    return results


if __name__ == "__main__":
    results = run_tests("test_")
