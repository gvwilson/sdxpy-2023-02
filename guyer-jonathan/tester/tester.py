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

def run_tests():
    for (name, test) in globals().items():
        if not name.startswith("test_"):
            continue
        if hasattr(test, "skip"):
            print(f"skip: {name}")
            continue
        try:
            test()
            print(f"pass: {name}")
        except AssertionError as e:
            if hasattr(test, "fail"):
                print(f"pass (expected failure): {name}")
            else:
                print(f"fail: {name} {str(e)}")
        except Exception as e:
            print(f"error: {name} {str(e)}")

if __name__ == "__main__":
    run_tests()
