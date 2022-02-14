#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 02:30:00 2022

@author: nats
"""

import numpy as np

def hamDist(seq0, seq1, bitsize):
    hd = 0
    bytexor = seq0 ^ seq1
    for i in np.arange(bitsize):
        #xored = ((seq0 >> i) & 1) ^ ((seq1 >> i) & 1)
        #hd += xored
        hd += (bytexor >> i) & 1
    return hd
    