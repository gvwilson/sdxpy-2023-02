from count_results import run_test


def verify_test_output():
    test_results = run_test()

    assert test_results["pass"] == 2
    assert test_results["fail"] == 1
    assert test_results["error"] == 1
    assert test_results["total"] == 4


verify_test_output()
