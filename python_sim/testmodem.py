from FSKModem import FSKModem as FMod
from FSKModem import Utils as FSKUtils

import numpy as np
import numpy.fft as fft
 
import matplotlib.pyplot as plt

modem = FMod.FSKModem(4, 10e3, 25e3, 2, 0)
bitstream = [0,1,1,1,0,1,1,1,1,0,0,1,1,0,1,0]
signal,tree = modem.modulateDiff(bitstream)

tones = modem.tones
T0, T0freq = tones[0]
T3, T3freq = tones[modem.nbTones - 1]
scale = np.linspace(T0freq * modem.overSample, T3freq * modem.overSample, int((len(bitstream)+1)*modem.symLen))/1000
spectre = 20*np.log10(fft.fftshift(np.abs(fft.fft(signal))))
fig, ax = plt.subplots()
ax.plot(scale,spectre)
ax.grid(True)
plt.show()

noise = FSKUtils.CAWGN(0.5, (len(bitstream)+1)*modem.symLen)

signoise = noise + signal

spectre = 20*np.log10(fft.fftshift(np.abs(fft.fft(signoise))))
fig, ax = plt.subplots()
ax.plot(scale,spectre)
ax.grid(True)
plt.show()