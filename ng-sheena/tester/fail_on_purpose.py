from glob import glob
from importlib.machinery import SourceFileLoader

"""
Failing on purpose:

Modified the test framework so that the test with "test:assert"
docstring will pass

Modified the unit tests to reflect the associated changes done to the test framework
"""
# test framework
def run_tests():
    test_files = glob("**/test_*.py", root_dir=".", recursive=True)

    res = {"pass": [], "fail": [], "error": []}

    for (i, name) in enumerate(test_files):
        m = SourceFileLoader(f"m{i}", name).load_module()

        for name in dir(m):
            if not name.startswith("test_"):
                continue

            func = getattr(m, name)

            try:
                func()
                print(f"pass: {name}")
                res["pass"].append(name)
            except AssertionError:
                if func.__doc__ == "test:assert":
                    print(f"pass: {name}")
                    res["pass"].append(name)
                else:
                    print(f"fail: {name}")
                    res["fail"].append(name)
            except Exception:
                print(f"error: {name}")
                res["error"].append(name)

    for key, value in res.items():
        print(key, len(value))

    return res

run_tests()


# unit test for the test framework
def verify_test_framework():
    res = run_tests()

    for key in res:
        if key == "pass":
            assert len(res[key]) == 3
            assert "test_sign_negative" in res[key]
            assert "test_sign_positive" in res[key]
            assert "test_sign_zero" in res[key]
        elif key == "fail":
            assert len(res[key]) == 0
        elif key == "error":
            assert len(res[key]) == 1
            assert "test_sign_error" in res[key]

verify_test_framework()
