from glob import glob
from importlib.machinery import SourceFileLoader

"""
Counting Results - Part 1
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
                print(f"fail: {name}")
                res["fail"].append(name)
            except Exception:
                print(f"error: {name}")
                res["error"].append(name)

    for key, value in res.items():
        print(key, len(value))

    return res

run_tests()


"""
Counting Results - Part 2
"""
# unit test for the test framework
def verify_test_framework():
    res = run_tests()

    for key in res:
        if key == "pass":
            assert len(res[key]) == 2
            assert "test_sign_negative" in res[key]
            assert "test_sign_positive" in res[key]
        elif key == "fail":
            assert len(res[key]) == 1
            assert "test_sign_zero" in res[key]
        elif key == "error":
            assert len(res[key]) == 1
            assert "test_sign_error" in res[key]

verify_test_framework()
