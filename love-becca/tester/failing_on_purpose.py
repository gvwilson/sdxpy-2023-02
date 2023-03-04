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
    assert sign(-3) == -1
def test_sign_positive():
    assert sign(19) == 1
def test_sign_zero():
    '''test:assert'''
    assert sign(0) == 0
# Misspelled 'sign'
def test_sign_error():
    assert sgn(1) == 1
    
def run_tests():
    results = {"pass": [], "fail": [], "error": []}
    for (name, test) in globals().items():
        if not name.startswith("test_"):
            continue
        
        if test.__doc__ and "test:assert" in test.__doc__:
            try:
                test()
                results["error"].append(name)
            except AssertionError:
                results["pass"].append(name)
        
        if not test.__doc__ or not "test:assert" in test.__doc__:
            try:
                test()
                results["pass"].append(name)
            except AssertionError:
                results["fail"].append(name)
            except Exception:
                results["error"].append(name)
                                
    return([(key, len(results[key]), results[key]) for key in results.keys()])
    
if __name__ == "__main__":
    run_tests()