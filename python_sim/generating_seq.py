#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 00:02:03 2022

@author: nats
"""
from threading import Thread, Event

import numpy as np

event = Event()

seqSize = 16

# Global matrice beurk
seqham = np.zeros((2**16, 2**16), dtype='uint16')

def hamcalc(a, b):
    c = a ^ b
    #return int(c).bit_count() # Valid in python 3.10
    return bin(c).count("1")

def hamstore(index):
    for i in np.arange(2**seqSize):
        seqham[index, i] = hamcalc(index, i)
        if event.is_set():
            break

nbThread = 0
thLim = 12
tList = [0] * thLim
for i  in np.arange(2**seqSize):
    # print("Sequence: ", i)
    # print("nbThread: ", nbThread)
    tList[nbThread] = Thread(target=hamstore, args=(i, ))
    nbThread = nbThread + 1
    tList[nbThread-1].start()
    if nbThread == thLim:
        for j in np.arange(thLim):
            tList[j].join()
        nbThread = 0
        print("Sequence: ", i)

nbValidSeq = 2**8
bestSeqs = np.zeros(2**8)

testSeq = np.zeros(2**seqSize)

for i in np.arange(2**seqSize-1,0):
    for j in np.arange(2**seqSize):
        testSeq[j] = seqham[i,j]
        print("test: ", seqham[i,j])