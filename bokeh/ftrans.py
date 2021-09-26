
# prepare some data
import numpy as np

def getall():
    T = 2

    def decay(x):
        return np.exp(-1*abs(x))
        if (x>=0):return np.exp(-1*x)
        else: return 0
    def sinc(xx):
        tmpT=12
        x=xx-2
        # if (abs(x)>=0 and abs(x)<=tmpT) : return np.sin(  3*(x-0.5*tmpT ) )/(   3*(x-0.5*tmpT) )*x
        if ((x)>=0 and abs(x)<=tmpT) : return np.sin(  3*(x ) )/(   3*(x) ) 
        else : return 0

        return np.sin(  3*(x-0.5*10 ) )/(   3*(x-0.5*10) )*x

    def sin(x):
        tmpT=12
        return np.cos( 4*x*2*np.pi/tmpT )
        #return (-x)**3-3*x**2-3*x+4
        # return np.sinc( 2*np.pi/tmpT *x) + np.cos( 2*np.pi/tmpT *3*x)

    def square(x):
        # return 1
        if (abs(x)<=T/4) : return 1
        else : return -1

    n=T*1000
    t = np.linspace(-T/2,T/2,n)
    signal = np.array(list(map(square,t)))
    # signal = np.array(list(map(decay,t)))
    # signal = np.array(list(map(decay,t)))


    def l2_ip(f,signal):
        # return np.inner( f, signal )* T/(n-1)
        return np.trapz(y= signal*np.conjugate(f)   ,x=t)

        return np.trapz(y= np.array(list(     map(np.inner,signal,f)  ))   ,x=t)
        

    maxW=20
    Xw = []
    ws = np.linspace(-maxW,maxW,1000)
    for w in ws:
        # print(w)
        Xw.append( np.trapz(y=    signal * np.exp(-1j*w*t)  ,x=t) )

    mag = np.round(np.abs(Xw),7)
    phase=np.round(np.angle(Xw),7)
    

    # xt = (1/2pi)  integral w= -inf to inf (  X(w) * exp(jwt) dw )

    xt=[]
    for eacht in t:
        xt.append( 1/(2*np.pi)*np.trapz(y=    Xw * np.exp(1j*ws*eacht)  ,x=ws) )

    
    
    return {'t':t,'signal':signal,'mag':mag,'phase':phase,'ws':ws,'Xw':Xw, 'xt':xt}