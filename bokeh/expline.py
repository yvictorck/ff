from bokeh.plotting import figure, show
from bokeh.layouts import column
# prepare some data
import numpy as np

T = 12

def sinc(x):
    return np.sin(  3*(x-0.5*T ) )/(   3*(x-0.5*T) )*x


def sin(x):
    # return np.cos( 4*x*2*np.pi/T ) 
    return np.sinc( 2*np.pi/T *x) + np.cos( 2*np.pi/T *3*x)*x


n=T*1000
t = np.linspace(0,T,n)
signal = np.array(list(map(sinc,t)))
#signal = np.cos( 4*t*2*np.pi/T )#np.array(list(map(sin,t)))

# t=np.linspace(0,1,1000)
#x=(np.cos( 4*t*2*np.pi/T ) *np.exp(-1j*2*np.pi*4*t) )
# x=(0.5-np.exp(-1j*2*np.pi*8*t)/2)
# np.trapz(y= x   ,x=t)
# ans=0.5

def l2_ip(f,signal):

    # return sum(  signal * np.conjugate(f) * T/(n-1)                )
    return np.trapz(y= signal*np.conjugate(f )  ,x=t)

    # return np.inner(  signal,f )* T/(n-1)
    # return np.trapz(y= np.array(list(     map(np.inner,signal,f)  ))   ,x=t)
    
a0 = np.trapz(y= signal   ,x=t)/T
print(a0)
ak=[]
bk=[]
ck=[]
xp=np.zeros(n)
for k in np.arange(-10,11):
    ck.append(1/T * l2_ip( np.exp(1j*2*(np.pi/T)*k*t) ,signal)   )
    ck[-1]=np.round(ck[-1], 7) 


    # ak.append(2./T * l2_ip( x, np.array(list(map(np.cos,t*2*np.pi/T*k ))))  )
    # bk.append(2./T * l2_ip( x, np.array(list(map(np.sin,t*2*np.pi/T*k ))))  )
    # ak.append(2/T * l2_ip( np.array(list(map(np.cos,t*2*np.pi/T*k )))  ,signal)   )
    # bk.append(2/T * l2_ip( np.array(list(map(np.sin,t*2*np.pi/T*k )))  ,signal)    )
    # def fseries(a,b,k):
    #     return   a*np.array(list(map(np.cos,t*2*np.pi/T*k ))) +  b*np.array(list(map(np.sin,t*2*np.pi/T*k )))
    xp = xp + ck[-1]*np.array(list(map(np.exp,1j*t*2*np.pi/T*k ))) 
print(np.round(xp,7))
# exit()
# create a new plot with a title and axis labels
p = figure(title="Simple line example", x_axis_label="x", y_axis_label="y",plot_width=800, plot_height=300)

# add a line renderer with legend and line thickness
p.line(t, signal, legend_label="x(t).", line_width=2)


p.line(t, np.real(xp), legend_label="xp(t).", line_width=2,line_color='red')


p1 = figure(title="Simple line example", x_axis_label="x", y_axis_label="y",plot_width=800, plot_height=300)

# add a line renderer with legend and line thickness
p1.line(t, signal, legend_label="x(t).", line_width=2)

# show the results
show(column(p,p1))