
# prepare some data
import numpy as np

def ctft(fs,xn):
    tmpT=1/fs
    T = len(xn)*tmpT
    t = np.linspace(-T*2,3*T,5*len(xn))
    signal = np.zeros(len(t))
    cnt=0
    for i,e in enumerate(t):
        # if e >=-T/2 and e <= T/2:
        if e >=0 and e <= T:
            signal[i]=xn[cnt]
            cnt+=1

    maxFreq = 1200
    maxW=maxFreq*2*np.pi
    Xw = []
    ws = np.linspace(-maxW,maxW,1000)
    ws2freq = ws/(2*np.pi)
    for w in ws:
        Xw.append( np.trapz(y=    signal * np.exp(-1j*w*t)  ,x=t) )
    mag = np.round(np.abs(Xw),7)
    phase=np.round(np.angle(Xw),7)
    

    # xt = (1/2pi)  integral w= -inf to inf (  X(w) * exp(jwt) dw )

    xt=[]
    for eacht in t:
        xt.append( 1/(2*np.pi)*np.trapz(y=    Xw * np.exp(1j*ws*eacht)  ,x=ws) )

    
    return {'t':t,'signal':signal,'mag':mag,'phase':phase,'ws':ws,'Xw':Xw, 'xt':xt}