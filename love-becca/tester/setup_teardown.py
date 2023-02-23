#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 16:59:16 2023

@author: beccalove
"""

# Should return 0 when given 0
def sign(value):
    if value < 0:
        return -1
    else:
        return 1
    
def test_sign_negative():
    test_sign_negative.test = True
    assert sign(-3) == -1
    
def test_sign_positive():
    test_sign_positive.test = True
    assert sign(19) == 1
    
def test_sign_zero():
    test_sign_zero.test = True
    assert sign(0) == 0
    
def test_sign_error():
    test_sign_error.test = True
    assert sgn(1) == 1
    
def setup():
    continue

def teardown():
    continue
    
def run_tests():
#def run_tests(path_to_tests):
    ##couldn't get this working with module namespace when imported from a file
    #import(path_to_tests) as my_tests
    
    results = {"pass": [], "fail": [], "error": []}
    
    for (name, test) in globals().items():
        if not name.startswith("test_"):
            continue
                
        try:
            if "setup" in globals().keys():
                globals()["setup"]()
                
            test()
                            
            results["pass"].append(name)
        except AssertionError:
            results["fail"].append(name)
        except Exception:
            results["error"].append(name)
            
            if "teardown" in globals().keys():
                globals()["teardown"]()
                
    return([(key, len(results[key]), results[key]) for key in results.keys()])
    
if __name__ == "__main__":
    run_tests()