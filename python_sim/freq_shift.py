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

modem = FMod.FSKModem(4, 25e3, 25e3, 5, 0, [0, 1, 0, 1, 1, 1 ,0], 1)
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
freqShift = 80000 # Hz

# Generate all sequences in advance
sigList = []
for i in np.arange(256):
    bs = modem.bitfield(i, 8)
    sig,tree = modem.modulateDiff(bs, shiftFreq=freqShift)
    sigList.append(sig)
    
# spectre = 20*np.log10(fft.fftshift(np.abs(fft.fft(sigList[85]))))
spectre = fft.fftshift(np.abs(fft.fft(sigList[125])))

fig, ax = plt.subplots()
plt.ion()
ax.plot(spectre)

ax.grid(b=True, which='major', color='b', linestyle='-')
ax.grid(b=True, which='minor', color='r', linestyle='--')
plt.show()