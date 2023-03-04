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


# def setup():
#     print("setup")

# def teardown():
#     print("teardown")

def run_tests(verbose=True):
    results = {"pass": [], "fail": [], "error": []}
    for (name, test) in globals().items():
        if not name.startswith("test_"):
            continue
        test_assert = test.__doc__ == "test:assert"
        try:
            if setup := globals().get("setup", False):
                setup()
            test()
            results["fail"].append(test.__name__) if test_assert else results[
                "pass"
            ].append(test.__name__)
        except AssertionError:
            results["pass"].append(test.__name__) if test_assert else results[
                "fail"
            ].append(test.__name__)
        except Exception:
            results["error"].append(test.__name__)
        finally:
            if teardown := globals().get("teardown", False):
                teardown()

    if not verbose:
        return results
    else:
        print(f"pass ({len(results['pass'])}): {[name for name in results['pass']]}.")
        print(f"fail ({len(results['fail'])}): {[name for name in results['fail']]}.")
        print(
            f"error ({len(results['error'])}): {[name for name in results['error']]}."
        )

run_tests()


def meta_test():
    assert run_tests(verbose=False) == {
        "pass": ["test_sign_negative", "test_sign_positive"],
        "fail": ["test_sign_zero"],
        "error": ["test_sign_error"],
    }

meta_test()
