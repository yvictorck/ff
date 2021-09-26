
# prepare some data
import numpy as np

def getall():
    T = 2

    def sinc(x):
        if x < -T/4 or x > T/4:
            return -1
        return 1
        # return np.sin(  3*(x-0.5*T ) )/(   3*(x-0.5*T) )*x

    def sin(x):
        # return np.cos( 4*x*2*np.pi/T )
        #return (-x)**3-3*x**2-3*x+4
        return np.sinc( 2*np.pi/T *x) + np.cos( 2*np.pi/T *3*x)*x

    n=T*1000
    t = np.linspace(-T/2,T/2,n)
    signal = np.array(list(map(sinc,t)))

    def l2_ip(f,signal):
        # return np.inner( f, signal )* T/(n-1)
        return np.trapz(y= signal*np.conjugate(f)   ,x=t)
        return np.trapz(y= np.array(list(     map(np.inner,signal,f)  ))   ,x=t)

    maxKval = 19
    a0 = np.trapz(y= signal *1  ,x=t)/T
    ak=[a0]
    bk=[0]
    xp=np.zeros([maxKval+1,n])
    xp[0]=xp[0]+ak[0]+0
    for k in range(1,maxKval+1):
        # ak.append(2./T * l2_ip( x, np.array(list(map(np.cos,t*2*np.pi/T*k ))))  )
        # bk.append(2./T * l2_ip( x, np.array(list(map(np.sin,t*2*np.pi/T*k ))))  )
        ak.append(2/T * l2_ip( np.array(list(map(np.cos,t*2*np.pi/T*k )))  ,signal)   )
        bk.append(2/T * l2_ip( np.array(list(map(np.sin,t*2*np.pi/T*k )))  ,signal)    )
        def fseries(a,b,k):
            return   a*np.array(list(map(np.cos,t*2*np.pi/T*k ))) +  b*np.array(list(map(np.sin,t*2*np.pi/T*k )))
        xp[k] = xp[k-1] + ak[-1]*np.array(list(map(np.cos,t*2*np.pi/T*k ))) +  bk[-1]*np.array(list(map(np.sin,t*2*np.pi/T*k )))

    # to show individual sin/cos
    akt=[t*0+ak[0]]
    bkt=[t*0]

    for k in range(1,maxKval+1):
        akt.append(ak[k]*np.cos(t*2*np.pi/T*k ) )
        bkt.append(bk[k]*np.cos(t*2*np.pi/T*k ) )

    ck=[]
    cxp=[]
    for k in np.arange(-maxKval,maxKval+1):
        ck.append(1/T * l2_ip( np.exp(1j*2*(np.pi/T)*k*t) ,signal)   )
        ck[-1]=np.round(ck[-1], 7) 


        # ak.append(2./T * l2_ip( x, np.array(list(map(np.cos,t*2*np.pi/T*k ))))  )
        # bk.append(2./T * l2_ip( x, np.array(list(map(np.sin,t*2*np.pi/T*k ))))  )
        # ak.append(2/T * l2_ip( np.array(list(map(np.cos,t*2*np.pi/T*k )))  ,signal)   )
        # bk.append(2/T * l2_ip( np.array(list(map(np.sin,t*2*np.pi/T*k )))  ,signal)    )
        # def fseries(a,b,k):
        #     return   a*np.array(list(map(np.cos,t*2*np.pi/T*k ))) +  b*np.array(list(map(np.sin,t*2*np.pi/T*k )))
        
        cxp.append(ck[-1]*np.array(list(map(np.exp,1j*t*2*np.pi/T*k ))) )

    cxppair=[]

    for k in range(0,maxKval+1):
        pos = k+maxKval
        neg = maxKval-k
        cxppair.append( cxp[pos] + cxp[neg] )
    cxppair[0]=cxppair[0]/2

    ccxp=[cxppair[0]]
    for k in range(1,maxKval+1):
        ccxp.append(  ccxp[-1]+cxppair[k] )

    
    cxreal=np.real(ck)
    cximg=np.imag(ck)
    cxmag=np.abs(ck)
    cxphase=np.angle(ck)

    return {'t':t,'signal':signal,'ak':ak,'bk':bk,'xp':xp,'ck':ck,'cxp':np.real(ccxp),'akt':akt,'bkt':bkt, 'cxreal':cxreal,
    'cximg':cximg,
    'cxmag':cxmag,
    'cxphase':cxphase}