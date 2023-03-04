from io import StringIO
import sys


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


def test2_raise_assert():
    """
    test:assert
    """
    assert False


def test2_raise_assert_skip():
    """
    test:assert
    """
    assert False


test2_raise_assert_skip.skip = True


def test2_raise_assert_fail():
    """
    test:assert
    """
    assert True


def test2_raise_assert_expected_fail():
    """
    test:assert
    """
    assert True


test2_raise_assert_expected_fail.fail = True


def test2_raise_assert_expected_fail_pass():
    """
    test:assert
    """
    assert False


test2_raise_assert_expected_fail_pass.fail = True


def test2_passing_test():
    assert True


def test2_failing_test():
    assert False


def test2_skipped_test():
    assert True


test2_skipped_test.skip = True


def test2_expected_failing_test():
    assert False


test2_expected_failing_test.fail = True


def test2_error_test():
    assert 12 / 0 == 0


def setup():
    print(f"Has setup been called: {setup.has_been_called}")
    print(f"Currently within setup: {setup.within_setup}")
    print(f"Within teardown test: {test_teardown_called.within_teardown_test}")
    if not (
        setup.has_been_called
        or setup.within_setup
        or test_teardown_called.within_teardown_test
    ):
        setup.has_been_called = True
        setup.within_setup = True
        print("Run setup\n")
        global mystdout
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        run_tests("test2_")
        sys.stdout = old_stdout
        setup.within_setup = False


setup.has_been_called = False
setup.within_setup = False


def teardown():
    if not (setup.within_setup or teardown.within_teardown):
        teardown.within_teardown = True
        print("\nRun teardown")
        teardown.has_been_called = True
    teardown.within_teardown = False


teardown.has_been_called = False


def test_setup_called():
    assert setup.has_been_called


def test_teardown_called():
    test_teardown_called.within_teardown_test = True
    run_tests("teardown_test")
    test_teardown_called.within_teardown_test = False
    assert teardown.has_been_called


test_teardown_called.within_teardown_test = False


test_teardown_called.fail = True
teardown.within_teardown = False


def test_pass_test():
    assert "pass: test2_passing_test" in mystdout.getvalue()


def test_fail_test():
    assert "fail: test2_failing_test" in mystdout.getvalue()


def test_skip_test():
    assert "skip: test2_skipped_test" in mystdout.getvalue()


def test_expected_fail_test():
    assert "pass (expected failure): test2_expected_failing_test" in mystdout.getvalue()


def test_error_in_test():
    assert "error: test2_error_test division by zero" in mystdout.getvalue()


def test_handle_assert():
    assert "pass (assert): test2_raise_assert" in mystdout.getvalue()


def test_handle_assert_skip():
    assert "skip: test2_raise_assert_skip" in mystdout.getvalue()


def test_handle_assert_fail():
    assert "fail (assert): test2_raise_assert_fail" in mystdout.getvalue()


def test_handle_assert_expected_fail():
    assert (
        "pass (assert expected failure): test2_raise_assert_expected_fail"
        in mystdout.getvalue()
    )


def test_results_output():
    assert "pass 4" in mystdout.getvalue()
    assert "fail 3" in mystdout.getvalue()
    assert "error 1" in mystdout.getvalue()
    assert "skip 2" in mystdout.getvalue()


def classify(func):
    if hasattr(func, "skip") and func.skip:
        return "skip"
    if hasattr(func, "fail") and func.fail:
        if (
            hasattr(func, "__doc__")
            and func.__doc__
            and ("test:assert" in func.__doc__)
        ):
            return "assert fail"
        else:
            return "fail"
    if hasattr(func, "__doc__") and func.__doc__ and ("test:assert" in func.__doc__):
        return "assert"
    return "run"


def run_tests(prefix):
    if "setup" in globals():
        setup()
    results = {"pass": 0, "fail": 0, "error": 0, "skip": 0}
    all_names = [n for n in globals() if n.startswith(prefix)]
    for name in all_names:
        func = globals()[name]
        kind = classify(func)
        try:
            if kind == "skip":
                print(f"skip: {name}")
                results["skip"] += 1
            elif kind == "assert":
                func()
                print(f"fail (assert): {name}")
                results["fail"] += 1
            elif kind == "assert fail":
                func()
                print(f"pass (assert expected failure): {name}")
                results["pass"] += 1
            else:
                func()
                print(f"pass: {name}")
                results["pass"] += 1
        except AssertionError as e:
            if kind == "fail":
                print(f"pass (expected failure): {name}")
                results["pass"] += 1
            elif kind == "assert":
                print(f"pass (assert): {name}")
                results["pass"] += 1
            else:
                print(f"fail: {name} {str(e)}")
                results["fail"] += 1
        except Exception as e:
            print(f"error: {name} {str(e)}")
            results["error"] += 1
    if "teardown" in globals():
        teardown()
    for result in results.keys():
        print(f"{result} {results[result]}")


run_tests("test_")
assert teardown.has_been_called
