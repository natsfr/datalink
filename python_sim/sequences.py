#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 01:36:28 2022

@author: nats
"""

from FSKModem import SeqUtils as SeqUtils

import numpy as np

seqSize = 8

seq0 = 0x00
seq1 = 0x00

hamArray = np.zeros((2**seqSize, 2**seqSize))
peakCorrArray = np.zeros((2**seqSize, 2**seqSize))
absCorrArray = np.zeros((2**seqSize, 2**seqSize))

for i in np.arange(2 ** seqSize):
    for j in np.arange(2 ** seqSize):
        hamArray[i,j] = SeqUtils.hamDist(seq0, seq1, seqSize)
        #peakCorrArray[i,j] = peakCorr(seq0, seq1, seqSize)
        #absCorrArray[i,j] = absCorr(seq0, seq1, seqSize)
        seq1 += 1
    seq0 += 1