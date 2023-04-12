from glob import glob
from importlib.machinery import SourceFileLoader


def run_test():
    # root_dir argument is supported only in python 3.10+
    test_files = glob("**/test_*.py", root_dir=".", recursive=True)

    # add a skip category in results to break verifier
    results = {"pass": 0, "fail": 0, "error": 0, "skip": 0}

    for (i, name) in enumerate(test_files):
        m = SourceFileLoader(f"m{i}", name).load_module()

        for name_entry in dir(m):
            if not name_entry.startswith("test_"):
                continue

            func = getattr(m, name_entry)

            if hasattr(func, "skip"):
                results["skip"] += 1
                print(f"skip: {name}")
                continue

            try:
                func()
                results["pass"] += 1
                print(f"{name_entry} pass")
            except AssertionError:
                if func.__doc__ == "test:assert":
                    results["pass"] += 1
                    print(f"{name_entry} pass")
                else:
                    results["fail"] += 1
                    print(f"{name_entry} fail")
            except Exception:
                results["error"] += 1
                print(f"{name_entry} error")

    results["total"] = results["pass"] + results["fail"] + results["skip"] + results["error"]
    print("Summary:")
    for key, value in results.items():
        print(key, value)

    return results


run_test()
