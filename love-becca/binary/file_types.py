#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 09:40:42 2023

@author: beccalove
"""

import os
import sys

png_identifier = [137,80,78,71,13,10,26,10]

this_dir = os.getcwd()

def check_png(file):
        
    with open(file, "rb") as infile:
        first_8 = list(infile.read(8))
        
    return png_identifier == first_8

tests = {f"{this_dir}/Black_cat_looking_upwards.png" : True,
         f"{this_dir}/Gata_común_negra.png" : True,
         f"{this_dir}/Chat_mâle_adulte.png" : True,
         f"{this_dir}/Hauskatze_langhaar.jpg" : False}

def run_tests():
    
    for filename, expected_value in tests.items():
        
        assert check_png(filename) == expected_value, filename

if __name__ == "__main__":
    
    filename = sys.argv[1]
    print(f"{filename} is a .png? ", check_png(filename))
    run_tests()