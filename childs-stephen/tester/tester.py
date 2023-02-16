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


def classify(func):
    if hasattr(func, "skip") and func.skip:
        return "skip"
    if hasattr(func, "fail") and func.fail:
        return "fail"
    return "run"


def run_tests(prefix):
    results = {"pass": 0, "fail": 0, "error": 0, "skip": 0}
    all_names = [n for n in globals() if n.startswith(prefix)]
    for name in all_names:
        func = globals()[name]
        kind = classify(func)
        try:
            if kind == "skip":
                print(f"skip: {name}")
                results["skip"] += 1
            else:
                func()
                print(f"pass: {name}")
                results["pass"] += 1
        except AssertionError as e:
            if kind == "fail":
                print(f"pass (expected failure): {name}")
                results["pass"] += 1
            else:
                print(f"fail: {name} {str(e)}")
                results["fail"] += 1
        except Exception as e:
            print(f"error: {name} {str(e)}")
            results["error"] += 1
    for result in results.keys():
        print(f"{result} {results[result]}")


run_tests("test_")
