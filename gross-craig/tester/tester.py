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


def pass_test(name, results):
    print(f"pass: {name}")
    results["pass"] += 1


def fail_test(name, results):
    print(f"fail: {name}")
    results["fail"] += 1


def run_tests(prefix):
    results = {"pass": 0,
               "fail": 0,
               "error": 0,
               "total": 0}

    if "setup" in globals():
        globals()["setup"]()

    for (name, test) in globals().items():
        if not name.startswith(prefix):
            continue

        results["total"] += 1

        try:
            test()
            if assert_test(test):
                fail_test(name, results)
            else:
                pass_test(name, results)

        except AssertionError as e:
            if assert_test(test):
                pass_test(name, results)
            else:
                fail_test(name, results)

        except Exception as e:
            print(f"error: {name} {str(e)}")
            results["error"] += 1

    if "teardown" in globals():
        globals()["teardown"]()

    print("\n--- Summary ---")
    print(f"{results['pass']}/{results['total']} tests passed")
    print(f"{results['fail']}/{results['total']} tests failed")
    print(f"{results['error']}/{results['total']} tests had errors")


if __name__ == "__main__":
    run_tests("test_")
