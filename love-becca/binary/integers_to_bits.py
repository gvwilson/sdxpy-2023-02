#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 10:18:12 2023

@author: beccalove
"""

##Limiting to 32-bit numbers

##right-shifting an integer by a value produces the quotient 
##when the integer is divided by 2^value
##or in colloquial terms, right-shifting chops off the right-most digit each time
##we can use this to "access" each digit from left to right
## and we can use "& 1" to see if this digit is 0 or 1

def to_binary(test_int):
    
    answer = []
    
    for i in range(32):
        answer.append((test_int >> i) & 1)
        
    return "0b" + "".join([str(x) for x in answer[::-1]])

def from_binary(test_val):
    
    answer = 0
    
    for i, val in enumerate(reversed(test_val)):
        answer += int(val) * (2 ** i)
        
    return answer

tests = {"1011" : 11,
                "111" : 7,
                "1" : 1,
                "10" : 2,
                "101111" : 47}

def run_tests():
    
    for key, value in tests.items():
        
        assert from_binary(key) == value, key
        assert to_binary(value) == "0b" + key.zfill(32), value

