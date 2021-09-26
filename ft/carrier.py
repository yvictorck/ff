import numpy as np

def carrierCos(fc,fs,xn):
    xcn =[]
    # normalizedxn = [(ele/2**bits_mag) for ele in xn]
    T=1/fs
    for i,x in enumerate(xn):
        t = T*i
        xcn.append( x * np.cos( 2*np.pi*fc* t)  )
    xcn = np.asarray(xcn)
    return xcn

