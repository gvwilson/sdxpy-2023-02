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
    assert sign(0) == 0
# Misspelled 'sign'
def test_sign_error():
    assert sgn(1) == 1
    
def test_self_one(results):
        
    assert len(results["pass"]) == 2
    assert len(results["fail"]) == 1
    assert len(results["error"]) == 1
    
def run_tests():
    results = {"pass": [], "fail": [], "error": []}
    for (name, test) in globals().items():
        if not name.startswith("test_"):
            continue
        
        if name.startswith("test_") and not name.startswith("test_self"):
            #print(f"found test! {name}")
            try:
                test()
                results["pass"].append(name)
            except AssertionError:
                results["fail"].append(name)
            except Exception:
                results["error"].append(name)
                
        if name.startswith("test_self"):
            #continue
            try:
                test(results)
                print("self-test working")
            except AssertionError:
                print("not passing own tests")
            except Exception:
                print(f"{name} self-test not working")
                
    return([(key, len(results[key]), results[key]) for key in results.keys()])
    
if __name__ == "__main__":
    run_tests()