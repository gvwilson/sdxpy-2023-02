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


def test_sign_error():
    assert sgn(1) == 1


test_sign_negative.skip = True
test_sign_zero.fail = True


def classify(func):
    if hasattr(func, "skip") and func.skip:
        return "skip"
    if hasattr(func, "fail") and func.fail:
        return "fail"
    return "run"


def run_tests(prefix):
    all_names = [n for n in globals() if n.startswith(prefix)]
    for name in all_names:
        func = globals()[name]
        kind = classify(func)
        try:
            if kind == "skip":
                print(f"skip: {name}")
            else:
                func()
                print(f"pass: {name}")
        except AssertionError as e:
            if kind == "fail":
                print(f"pass (expected failure): {name}")
            else:
                print(f"fail: {name} {str(e)}")
        except Exception as e:
            print(f"error: {name} {str(e)}")


if __name__ == "__main__":
    run_tests("test_")
