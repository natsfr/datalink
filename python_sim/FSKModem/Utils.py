#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 14:54:01 2022

@author: mk
"""

import numpy as np
import numpy.random as rnd

def CAWGN(power, length):
    return np.sqrt(power) * np.sqrt(2)/2 *(rnd.randn(int((length))) + 1j * rnd.randn(int(length)));

def polymul(poly0, poly1):
    a = poly1
    b = poly0
    if(len(poly0) >= len(poly1)):
        a = poly0
        b = poly1
    result = [0] * (len(a)+len(b))
    for i in np.arange(len(b)): # Shorter Poly
        for j in np.arange(len(a)): # Longer Poly
            if a[j] != 0 and b[i] != 0: # X^(i+j) = a[j] * b[i]
                result[i+j] += a[j] * b[i]
    return result

def GF2poly(poly):
    gf2poly = []
    for i in np.arange(len(poly)):
        gf2poly.append(np.mod(poly[i], 2))
    return gf2poly

def polymod(poly, mod):
    remainder = []
    for i in np.arange(mod,len(poly)):
        remainder.append(poly[i])
    mlen = min(len(remainder), mod)
    final = []
    for i in np.arange(mlen):
        final.append(remainder[i] + poly[i])
    return final

# Coef need to be set in the LSB first
def binarypolymul(poly0, poly1, polysize, modulo):
    # Dumb method
    p0 = np.zeros(polysize);
    p1 = np.zeros(polysize);
    for i in np.arange(len(poly0)):
        p0[i] = poly0[i]
    for i in np.arange(len(poly1)):
        p1[i] = poly1[i]
    arbmul = polymul(p0, p1)
    arbmul = GF2poly(arbmul)
    return GF2poly(polymod(arbmul, modulo))