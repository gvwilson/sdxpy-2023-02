
def test_sampletest():
    pass


def test_failing_on_purpose():
    """test:assert"""
    raise AssertionError("This should fail nicely and get marked as passed")


def setup():
    print("setup has been called")


def teardown():
    print("teardown has been called")

