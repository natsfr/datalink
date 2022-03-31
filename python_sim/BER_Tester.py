#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 02:26:36 2022

@author: nats
"""
from FSKModem import FSKModem as FMod
from FSKModem import Utils as FSKUtils

import numpy as np
import numpy.fft as fft
 
import matplotlib.pyplot as plt

def BERDiff(bs, rxbs):
    if len(bs) == len(rxbs):
        errCount = 0
        for i in np.arange(len(bs)):
            if bs[i] != rxbs[i]:
                errCount = errCount + 1
        return errCount
    return 0

modem = FMod.FSKModem(4, 25e3, 25e3, 1, 0, [0, 1, 0, 1, 1, 1 ,0], 1)
print("FSK Modem:")
print("Tones: ", modem.nbTones)
print("Tone Spacing: ", modem.toneSpacing)
print("Bandwidth: ", modem.BW)
print("Datarate: ", modem.DR)
print("Tones frequency: ", [x[1] for x in modem.tones])
print("Symbol length: ", modem.symLen)
print("Starting symbol: ", modem.startSym)
print("Sampling frequency: ", modem.FS)


perList = []
berList = []

# Activte frequency shift
shift = True
freqShift = 500 # Hz

# Generate all sequences in advance
sigList = []
for i in np.arange(256):
    bs = modem.bitfield(i, 8)
    sig,tree = modem.modulateDiff(bs, freqShift)
    sigList.append(sig)
    
# Generate same sequences in Modem object
modem.fillRefSeq(8)

for i in np.arange(0, 15):
    dBRatio = i
    linRatio = 10 ** (dBRatio / 10)
    print("dB ratio: ", dBRatio, "linear ratio: ", linRatio)
    
    nbPERErr = 0
    nbBERErr = 0
    nbIter = 5000
    
    ebno_level = modem.ebno2np(linRatio)
    
    for j in np.arange(0, nbIter):
        bsbin = np.random.randint(0,255,dtype=np.uint8)
        sig = sigList[bsbin]
        
        noise = FSKUtils.CAWGN(ebno_level, len(sig))
        sig  = sig + noise
        
        outModem = modem.bruteForceSeq(sig)
        seqRX = outModem.index(max(outModem))
        
        bs = modem.bitfield(bsbin, 8)
        bsout = modem.bitfield(seqRX, 8)
        
        if seqRX != bsbin:
            nbPERErr = nbPERErr + 1
        nbBERErr = nbBERErr  + BERDiff(bs, bsout)
        
    perList.append((dBRatio, nbPERErr/nbIter))
    berList.append((dBRatio, nbBERErr/(nbIter*8)))
    
fig, ax = plt.subplots()
plt.ion()
ax.scatter(*zip(*perList))
ax.scatter(*zip(*berList))
ax.set_yscale('log')
ax.set_ylim([1e-7, 1])
ax.grid(b=True, which='major', color='b', linestyle='-')
ax.grid(b=True, which='minor', color='r', linestyle='--')
plt.show()