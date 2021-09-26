from bokeh.plotting import figure, show
from bokeh.layouts import column
# prepare some data

T = 12

def sinc(x):
    return np.sin(  3*(x-0.5*T ) )/(   3*(x-0.5*T) )*x

def sin(x):
    # return np.cos( 4*x*2*np.pi/T )
    #return (-x)**3-3*x**2-3*x+4
    return np.sinc( 2*np.pi/T *x) + np.cos( 2*np.pi/T *3*x)*x

import numpy as np
n=T*1000
t = np.linspace(0,T,n)
signal = np.array(list(map(sinc,t)))


def l2_ip(f,signal):
    # return np.inner( f, signal )* T/(n-1)
    return np.trapz(y= signal*np.conjugate(f)   ,x=t)

    return np.trapz(y= np.array(list(     map(np.inner,signal,f)  ))   ,x=t)
    
a0 = np.trapz(y= signal   ,x=t)/T
print(a0)
ak=[]
bk=[]
xp=np.zeros([11,n])

xp[0]=xp[0]+a0
for k in range(1,11):
    # ak.append(2./T * l2_ip( x, np.array(list(map(np.cos,t*2*np.pi/T*k ))))  )
    # bk.append(2./T * l2_ip( x, np.array(list(map(np.sin,t*2*np.pi/T*k ))))  )
    ak.append(2/T * l2_ip( np.array(list(map(np.cos,t*2*np.pi/T*k )))  ,signal)   )
    bk.append(2/T * l2_ip( np.array(list(map(np.sin,t*2*np.pi/T*k )))  ,signal)    )
    def fseries(a,b,k):
        return   a*np.array(list(map(np.cos,t*2*np.pi/T*k ))) +  b*np.array(list(map(np.sin,t*2*np.pi/T*k )))
    xp[k] = xp[k-1] + ak[-1]*np.array(list(map(np.cos,t*2*np.pi/T*k ))) +  bk[-1]*np.array(list(map(np.sin,t*2*np.pi/T*k )))

print(ak)
print(bk)
# create a new plot with a title and axis labels
p = figure(title="Simple line example", x_axis_label="x", y_axis_label="y",plot_width=800, plot_height=300)

# add a line renderer with legend and line thickness
p.line(t, signal, legend_label="x(t).", line_width=2)
import fseries
info=fseries.getall()
p.line(t, info['xp'][-1], legend_label="xp(t).", line_width=2,line_color='red')


p1 = figure(title="Simple line example", x_axis_label="x", y_axis_label="y",plot_width=800, plot_height=300)

# add a line renderer with legend and line thickness
p1.line(t, signal, legend_label="x(t).", line_width=2)

# show the results
show(column(p,p1))