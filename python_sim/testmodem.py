from FSKModem import FSKModem as FMod
from FSKModem import Utils as FSKUtils

import numpy as np
import numpy.fft as fft
 
import matplotlib.pyplot as plt

modem = FMod.FSKModem(4, 15e3, 25e3, 1, 0)
bitstream = [0,1,1,1,0,1,1,1,1,0,0,1,1,0,1,0]
signal,tree = modem.modulateDiff(bitstream)

tones = modem.tones
T0, T0freq = tones[0]
T3, T3freq = tones[modem.nbTones - 1]
scale = np.linspace(T0freq * modem.overSample, T3freq * modem.overSample, int((len(bitstream)+1)*modem.symLen))/1000
# spectre = 20*np.log10(fft.fftshift(np.abs(fft.fft(signal))))
# fig, ax = plt.subplots()
# ax.plot(scale,spectre)
# ax.grid(True)
# plt.show()

# noise = FSKUtils.CAWGN(0.5, (len(bitstream)+1)*modem.symLen)

# signoise = noise + signal

# spectre = 20*np.log10(fft.fftshift(np.abs(fft.fft(signoise))))
# fig, ax = plt.subplots()
# ax.plot(scale,spectre)
# ax.grid(True)
# plt.show()

Pnoise = modem.ebno2np(10)
noise = FSKUtils.CAWGN(Pnoise, len(signal))

# Create circle
x = np.linspace(-1.0, 1.0, 100)
y = np.linspace(-1.0, 1.0, 100)

X, Y = np.meshgrid(x,y)

F = X**2 + Y**2 - 1.0

demodsig = modem.demodAligned(signal+noise)
nsig = signal + noise
fig, ax = plt.subplots()
plt.ion()
ax.contour(X,Y,F,[0])
ax.scatter(signal.real, signal.imag, label="All signal points")
ax.scatter(nsig.real, nsig.imag, label="All noisy signal points")
ax.scatter(demodsig.real, demodsig.imag, marker="v", label="Symbol Centered Points")
ax.grid(True)
ax.legend()
plt.show()



input()
