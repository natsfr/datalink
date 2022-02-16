# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 01:16:18 2022

@author: nats
"""

import numpy as np

class FSKModem:
    
    def __init__(self, nbTones, DR, toneSpacing, overSample, startSymbol):
        self.nbTones = nbTones
        self.DR = DR
        self.toneSpacing = toneSpacing
        self.overSample = overSample
        
        # Calculate Bandwidth and Sampling Frequency
        self.BW = self.nbTones * self.toneSpacing
        self.FS = self.BW * self.overSample
        
        # Calculate symbol length in sample and second
        self.symLen = self.FS / self.DR
        self.Tsym = 1 / self.DR
        
        self.n = np.arange(self.symLen)
        
        self.createTonesTable()
        
        self.startSym = startSymbol
        
    def createTonesTable(self):
        self.tones = []
        startToneFreq = -1 * self.toneSpacing * ((self.nbTones / 2 - 1) + 1/2)
        for i in np.arange(self.nbTones):
            s = np.exp(-1j * 2 * np.pi * startToneFreq / self.FS * self.n)
            self.tones.append((s, startToneFreq))
            startToneFreq += self.toneSpacing
        
    # Modulate some kind of differential FSK for treillis demod
    def modulateDiff(self, bitstream):
        print("Type of bitstream: ", type(bitstream))
        stone, stoneFreq = self.tones[self.startSym]
        signal = np.array(stone)
        tree = [self.startSym]
        runTime = self.Tsym * stoneFreq
        currentSym = self.startSym
        for b in bitstream:
            if b == 1:
                currentSym += 1
                if currentSym == self.nbTones:
                    currentSym = 0
            elif b == 0:
                currentSym -= 1
                if currentSym == -1:
                    currentSym = self.nbTones - 1
            tone, toneFreq = self.tones[currentSym]
            relativePhase = runTime / toneFreq
            delay = np.exp(2 * np.pi * 1j * toneFreq * relativePhase)
            runTime = runTime + toneFreq * self.Tsym
            signal = np.append(signal, tone * delay)
            tree.append(currentSym)
        return (signal,tree)