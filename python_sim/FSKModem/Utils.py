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
