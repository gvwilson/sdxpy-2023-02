def sign(value):
    if value < 0:
        return -1
    else:
        return 1

def test_sign_negative():
    assert sign(-3) == -1
test_sign_negative.skip = True

def test_sign_negative_bis():
    """test:assert"""
    assert sign(-3) == 1

def test_sign_positive():
    assert sign(19) == 1
    
def test_sign_zero():
    assert sign(0) == 0
test_sign_zero.fail = True

def test_sign_error():
    assert sgn(1) == 1

def run_tests():
    skipped = []
    passed = []
    failed = []
    errored = []

    for (name, test) in globals().items():
        if not name.startswith("test_"):
            continue
        if hasattr(test, "skip"):
            print(f"skip: {name}")
            skipped.append(name)
            continue
        try:
            test()
            print(f"pass: {name}")
            passed.append(name)
        except AssertionError as e:
            print("docstring:", test.__doc__)
            if test.__doc__ == "test:assert":
                print(f"pass: {name}")
                passed.append(name)
            elif hasattr(test, "fail"):
                print(f"pass (expected failure): {name}")
                passed.append(name)
            else:
                print(f"fail: {name} {str(e)}")
                failed.append(name)
        except Exception as e:
            print(f"error: {name} {str(e)}")
            errored.append(name)

    print(f"{len(skipped)} tests skipped: {skipped}")
    print(f"{len(passed)} tests passed: {passed}")
    print(f"{len(failed)} tests failed: {failed}")
    print(f"{len(errored)} tests errored: {errored}")

    return skipped, passed, failed, errored

def meta_test_results():
    skipped, passed, failed, errored = run_tests()

    assert skipped == ["test_sign_negative"]
    assert passed == ["test_sign_positive", "test_sign_zero"]
    assert failed == []
    assert errored == ["test_sign_error"]

if __name__ == "__main__":
    run_tests()

    meta_test_results()
