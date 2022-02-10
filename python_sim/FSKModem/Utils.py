#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 14:54:01 2022

@author: mk
"""

import numpy as np
import numpy.random as rnd

def CAWGN(power, length):
    return power * np.sqrt(2)/2 *(rnd.randn(int((length))) + 1j * rnd.randn(int(length)));

def polymul(poly0, poly1):
    a = poly1
    b = poly0
    print(a)
    if(len(poly0) >= len(poly1)):
        a = poly0
        b = poly1
    result = [0] * (len(a)+len(b))
    for i in np.arange(len(b)): # Shorter Poly
        for j in np.arange(len(a)): # Longer Poly
            if a[j] != 0 and b[i] != 0: # X^(i+j) = a[j] * b[i]
                result[i+j] += a[j] * b[i]
    return result
