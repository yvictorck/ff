import numpy as np
from scipy.linalg import dft as dftmat

def dft(bits_mag=0,fs=1,xn=[0]):
    N=len(xn)
    wn = np.exp(-1j*2*np.pi/N)
    normalizedxn = [(ele/2**bits_mag) for ele in xn]
    bks = dftmat(N) @ normalizedxn
    mag = np.round(np.abs(bks),7)
    phase=np.round(np.angle(bks),7)
    omegas=np.array([])
    freqs = np.array([])
    for k in range(N):
        omegas=np.append(omegas,(2*np.pi/N)*k)
        freqs=np.append(freqs,(fs/N)*k)

    return {'freqs':freqs,'omegas': omegas, 'bks':bks, 'mag':mag, 'phase':phase }


