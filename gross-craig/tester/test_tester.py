from tester import run_tests


def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


def test_summary_pass():
    result_string = ""

    def fixture_test_positive():
        assert sign(1) == 1

    result_string += "pass: fixture_test_positive \n"

    summary_string = "--- Summary ---\n"
    summary_string += "1/1 tests passed\n"
    summary_string += "0/1 tests failed\n"
    summary_string += "0/1 tests had errors"

    # We have to pass in the locals() so fixture tests are found in run_tests
    out_string = run_tests("fixture_test_", **locals())
    assert out_string == result_string + summary_string


def test_summary_pass_fail():
    result_string = ""

    def fixture_test_positive():
        assert sign(1) == 1

    result_string += "pass: fixture_test_positive \n"

    def fixture_test_negative_wrong():
        assert sign(-1) == 1

    result_string += "fail: fixture_test_negative_wrong \n"

    summary_string = "--- Summary ---\n"
    summary_string += "1/2 tests passed\n"
    summary_string += "1/2 tests failed\n"
    summary_string += "0/2 tests had errors"

    # We have to pass in the locals() so fixture tests are found in run_tests
    out_string = run_tests("fixture_test_", **locals())
    assert out_string == result_string + summary_string


def test_summary_pass_fail_error():
    result_string = ""

    def fixture_test_positive():
        assert sign(1) == 1

    result_string += "pass: fixture_test_positive \n"

    def fixture_test_negative_wrong():
        assert sign(-2) == -1
        assert sign(-1) == 1

    result_string += "fail: fixture_test_negative_wrong \n"

    def fixture_test_zero_error():
        assert sgn(0) == 0

    result_string += ("error: fixture_test_zero_error "
                      "name 'sgn' is not defined\n")

    summary_string = "--- Summary ---\n"
    summary_string += "1/3 tests passed\n"
    summary_string += "1/3 tests failed\n"
    summary_string += "1/3 tests had errors"

    # We have to pass in the locals() so fixture tests are found in run_tests
    out_string = run_tests("fixture_test_", **locals())
    assert out_string == result_string + summary_string
