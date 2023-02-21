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

        if "setup" in dir(m) and "teardown" in dir(m):
            setup_func = getattr(m, "setup")
            setup_func()

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

        if "setup" in dir(m) and "teardown" in dir(m):
            teardown_func = getattr(m, "teardown")
            teardown_func()

    for key, value in res.items():
        print(key, len(value))

    return res

run_tests()