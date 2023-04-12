def test_stats_test1():
    assert True

def test_stats_test2():
    assert True

def test_stats_test3():
    """this one doesn't have proper assert attr and will fail"""
    assert False

def test_stats_test4():
    raise Exception("Add 1 error exception to run_test return result.")
