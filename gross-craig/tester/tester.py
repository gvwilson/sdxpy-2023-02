def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


def test_positive():
    assert sign(1) == 1


def test_negative_wrong():
    assert sign(-1) == 1


def test_negative_wrong_test_assert():
    '''test:assert'''
    assert sign(-1) == 1


def test_negative():
    assert sign(-2) == -1


def test_zero_error():
    assert sgn(0) == 0


def test_zero():
    assert sign(0) == 0


def test_setup():
    assert sign(numbers["positive"]) == 1
    assert sign(numbers["negative"]) == -1
    assert sign(numbers["zero"]) == 0


def setup():
    print("setting up!")
    numbers = {"positive": 10,
               "negative": -10,
               "zero": 0}


def teardown():
    print("tearing down!")


def assert_test(func):
    return func.__doc__ == "test:assert"


def record_test(result, name, results, *extras):
    results[result] += 1
    return f"{result}: {name} {' '.join(extras)}\n"


def generate_summary(results):
    summary = "--- Summary ---\n"
    summary += f"{results['pass']}/{results['total']} tests passed\n"
    summary += f"{results['fail']}/{results['total']} tests failed\n"
    summary += f"{results['error']}/{results['total']} tests had errors"
    return summary


def run_tests(prefix, **extra_tests):
    '''Runs and records all tests defined in globals() or extra_tests
    starting with prefix'''

    results = {"pass": 0,
               "fail": 0,
               "error": 0,
               "total": 0}

    all_tests = globals() | extra_tests

    if "setup" in all_tests:
        all_tests["setup"]()

    out_string = ""
    for (name, test) in all_tests.items():
        if not name.startswith(prefix):
            continue

        results["total"] += 1

        try:
            test()
            if assert_test(test):
                out_string += record_test("fail", name, results)
            else:
                out_string += record_test("pass", name, results)

        except AssertionError as e:
            if assert_test(test):
                out_string += record_test("pass", name, results)
            else:
                out_string += record_test("fail", name, results)

        except Exception as e:
            out_string += record_test("error", name, results, str(e))

    out_string += generate_summary(results)
    print(out_string)

    if "teardown" in all_tests:
        all_tests["teardown"]()

    return out_string


if __name__ == "__main__":
    run_tests("test_")
