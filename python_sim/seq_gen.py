# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 03:39:26 2022

@author: nats
"""

import numpy as np

def hammingDist(seqA, seqB):
    

seqSize = 8
nbValid = 16

distMap = np.zeros((2**seqSize,2**seqSize))

