# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 01:16:18 2022

@author: nats
"""

import numpy as np

class FSKModem:
    
    def __init__(self, nbTones, DR, toneSpacing, overSample, startSymbol, syncPattern, diffMode = 1):
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
        
        self.syncPattern = syncPattern
        self.syncSig = self.modulateDiff(syncPattern)
        
        # Init the size indicator of the brute force sequence
        self.refSeqSize = 0
        
        # Use the modem as differential encoding or free encoding
        # Used in BER Calculation
        self.diffMode = diffMode
        
    def createTonesTable(self):
        self.tones = []
        startToneFreq = -1 * self.toneSpacing * ((self.nbTones / 2 - 1) + 1/2)
        for i in np.arange(self.nbTones):
            s = np.exp(1j * 2 * np.pi * startToneFreq / self.FS * self.n)
            self.tones.append((s, startToneFreq))
            startToneFreq += self.toneSpacing
    
    def bitfield(self, n, len):
        return [int(digit) for digit in bin(n)[2:].zfill(len)]

    # Modulate some kind of differential FSK for treillis demod
    def modulateDiff(self, bitstream, shiftFreq = 0):
        stone, stoneFreq = self.tones[self.startSym]
        signal = np.empty(shape=(0,0), dtype='complex')
        tree = []
        runTime = 0
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
        if shiftFreq != 0:
            t = np.arange(0, len(signal))
            shiftSig = np.exp(1j * 2* np.pi * shiftFreq / self.FS * t)
            signal = signal * shiftSig
        self.SPow = np.sum(np.abs(signal)**2) / len(signal)
        return (signal,tree)
    
    def signalPower(self, signal):
        SPow = np.sum(np.abs(signal)**2)
        return SPow
    
    def demodAlignedCorr(self, signal):
        nbSym = int(len(signal)/self.symLen)
        symLen = int(self.symLen)
        sTones = [x[0] for x in self.tones]
        corrs = np.zeros((len(sTones), nbSym), dtype='complex')
        for s in np.arange(len(sTones)):
            for i in np.arange(nbSym):
                sigPart = signal[i*symLen:i*symLen+symLen]
                sigRef = sTones[s]
                corrs[s][i] = (np.correlate(sigPart, sigRef, 'valid'))
        return corrs
    
    def fillRefSeq(self, size):
        self.referenceSeqs = []
        self.refSeqSize = size
        for i in np.arange(2**size):
            self.referenceSeqs.append(self.modulateDiff(self.bitfield(i, size))[0])
        return
    
    def bruteForceSeq(self, signal):
        nbSym = int(len(signal)/self.symLen)
        symLen = int(self.symLen)
        seed = 0
        seqs = []
        detectSeq = []
        if nbSym != self.refSeqSize:
            for i in np.arange(2**nbSym):
                seqs.append(self.modulateDiff(self.bitfield(seed, nbSym))[0])
                seed = seed + 1
                detectSeq.append(np.correlate(signal, seqs[i], 'valid')[0])
        else:
            for i in np.arange(2**self.refSeqSize):
                detectSeq.append(np.correlate(signal, self.referenceSeqs[i], 'valid')[0])
        return detectSeq

    # Generate noise of right power corresponding to EB/NO ratio
    # SNR = Psig / Pnoise
    # Psig = Eb /Tb = Eb * DR
    # Pnoise = N0 * BW
    def ebno2np(self, ratio):
        # Modify the bitrate if you use the free mode
        if not self.diffMode:
            bitrate = self.DR * np.log2(self.nbTones)
        else:
            bitrate = self.DR
        Pnoise = (self.BW * self.SPow) / (ratio * bitrate)
        PnoiseInBW = Pnoise * (self.FS) / self.BW
        print("Noise Power: ", Pnoise, " Noise in Bandwidth: ", PnoiseInBW)
        return PnoiseInBW