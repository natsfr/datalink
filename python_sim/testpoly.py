from FSKModem import FSKModem as FMod
from FSKModem import Utils as FSKUtils

import numpy as np
import numpy.fft as fft
 
import matplotlib.pyplot as plt

poly0 = [1,0,1,0,1]
poly1 = [1,1,0,0,1]

print(len(poly0))

poly0.reverse()
poly1.reverse()

res = FSKUtils.polymul(poly0, poly1)
res.reverse()

res = FSKUtils.GF2poly(res)

modulo = FSKUtils.polymod(res, 5)

final_result = FSKUtils.GF2poly(modulo)