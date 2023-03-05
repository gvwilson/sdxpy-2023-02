from sign import sign
import os
import shutil


def setup():
    original = r'/Users/peterlin/Sheena/Projects/Python/GregSoftwareDesign/GregSoftwareDesign-2023/ng-sheena/tester/README.md'
    target = r'/Users/peterlin/Sheena/Projects/Python/GregSoftwareDesign/GregSoftwareDesign-2023/ng-sheena/tester/README_copy.md'

    shutil.copyfile(original, target)

    print("README copy is created")

def test_sign_negative():
    assert sign(-5) == -1

def test_sign_positive():
    assert sign(20) == 1

def test_sign_zero():
    """test:assert"""
    assert sign(0) == 0

def test_sign_error():
    assert sgn(-5) == -1

def teardown():
    if os.path.exists('/Users/peterlin/Sheena/Projects/Python/GregSoftwareDesign/GregSoftwareDesign-2023/ng-sheena/tester/README_copy.md'):
        os.remove('/Users/peterlin/Sheena/Projects/Python/GregSoftwareDesign/GregSoftwareDesign-2023/ng-sheena/tester/README_copy.md')

        print("README copy is deleted")