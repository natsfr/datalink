#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 01:36:28 2022

@author: nats
"""

from FSKModem import SeqUtils as SeqUtils
from FSKModem import FSKModem as FMod

import numpy as np

seqSize = 8

seq0 = 0x00
seq1 = 0x00

hamArray = np.zeros((2**seqSize, 2**seqSize))

for i in np.arange(2 ** seqSize):
    for j in np.arange(2 ** seqSize):
        hamArray[i,j] = SeqUtils.hamDist(seq0, seq1, seqSize)
        seq1 += 1
    seq0 += 1
    
modem = FMod.FSKModem(4, 10e3, 25e3, 2, 0)
nbSample = int(modem.symLen * seqSize)

modulatedArray = []
seqMod = 0x00

for i in np.arange(2 ** seqSize):
    seqList = [int(x) for x in "{:08b}".format(seqMod)]
    print(seqList)
    modulatedArray.append(modem.modulateDiff(seqList)[0])
    seqMod += 1
    
corrArray = np.zeros((2**seqSize,2**seqSize))
for i in np.arange(2 ** seqSize):
    for j in np.arange(2 ** seqSize):
        corr = np.correlate(modulatedArray[i], modulatedArray[j])
        corrArray[i,j] = corr[0] ** 2