#https://docs.bokeh.org/en/latest/docs/user_guide/interaction/callbacks.html

from bokeh.layouts import column
from bokeh.models import ColumnDataSource, CustomJS, Slider
from bokeh.plotting import Figure, output_file, show,save
from bokeh.layouts import gridplot

from bokeh.palettes import Category20 as palette
import itertools

import fseries

info=fseries.getall()
maxKval=len(info['ak'])-1

colors = palette[maxKval+1]
# while len(colors)>3:
    # colors.pop()
# data['color'] = colors
# print(colors)
output_file("fs.html")

# x = [x*0.005 for x in range(0, 200)]
# y = x

# source = ColumnDataSource(data=dict(x=x, y=y))

import numpy as np

ts=[]
xp=[]
cxp=[]


for i in range(0,maxKval+1):
    ts.append(info['t'])
    xp.append(info['xp'][i])
    cxp.append(info['cxp'][i])


alphas=np.zeros(maxKval+1)
alphas[0]=1

widths=np.ones(maxKval+1)*3


akt=[]
bkt=[]
for i in range(0,maxKval+1):
    akt.append(info['akt'][i])
    bkt.append(info['bkt'][i])
alphas2=np.zeros(len(ts))
alphas2[0]=1




source = ColumnDataSource(data=dict(
    ts=ts,

    xp=xp,
    color=colors,
    alpha=alphas,
    width=widths,
 
    akt=akt,
    bkt=bkt,
    alpha2=alphas2,
    width2=widths,

    cxp=cxp,


))



plot1 = Figure(title="original function vs sin/cos fourier series",plot_width=800, plot_height=200)
plot1.line(x=info['t'],y=info['signal'],line_color='black',line_width=8,alpha=0.2)
plot1.multi_line(xs='ts', ys='xp', source=source,line_color='color',line_alpha='alpha',line_width='width')

plot2 = Figure(title="ak with cos", x_axis_label="x", y_axis_label="y",plot_width=800, plot_height=200)
plot2.multi_line(xs='ts', ys='akt', source=source,line_color='color',line_alpha='alpha2',line_width='width2')

plot3 = Figure(title="bk with sin", x_axis_label="x", y_axis_label="y",plot_width=800, plot_height=200)
plot3.multi_line(xs='ts', ys='bkt', source=source,line_color='color',line_alpha='alpha2',line_width='width2')

plot4 = Figure(title="ak", plot_width=800, plot_height=200)
plot4.circle(x=np.arange(0,maxKval+1),y=info['ak'],line_color=colors,line_width=8,alpha=1)

plot5 = Figure(title="bk", plot_width=800, plot_height=200)
plot5.circle(x=np.arange(0,maxKval+1),y=info['bk'],line_color=colors,line_width=8,alpha=1)

plot6 = Figure(title="original function vs complex fourier series", plot_width=800, plot_height=200)
plot6.line(x=info['t'],y=info['signal'],line_color='black',line_width=8,alpha=0.2)
plot6.multi_line(xs='ts', ys='cxp', source=source,line_color='color',line_alpha='alpha',line_width='width')


cxcolor=[]
i=len(colors)-1
while i >=0:
    cxcolor.append(colors[i])
    i-=1
i=1
while i<len(colors):
    cxcolor.append(colors[i])
    i+=1 

plot7 = Figure(title="complex fourier series Magnitude", plot_width=800, plot_height=200)
plot7.circle(x=np.arange(-maxKval,maxKval+1),y=info['cxmag'],line_color=cxcolor,line_width=8,alpha=1)

plot8 = Figure(title="complex fourier series Phase", plot_width=800, plot_height=200)
plot8.circle(x=np.arange(-maxKval,maxKval+1),y=info['cxphase'],line_color=cxcolor,line_width=8,alpha=1)

callback = CustomJS(args=dict(source=source), code="""
    var data = source.data;
    var index = cb_obj.value
    for (var i = 0; i < data.xp.length; i++) {
       data.alpha[i]=0
    }
    data.alpha[index]=1
    for (var i = 0; i < data.akt.length; i++) {
        if (i<=index) {data.alpha2[i]=1}
        else { data.alpha2[i]=0}
    }
        


    source.change.emit();
""")

slider = Slider(start=0, end=maxKval, value=0, step=1, title="k")
slider.js_on_change('value', callback)

layout = column(slider, plot1,plot2,plot3,plot4)

grid = gridplot([[plot1,slider,plot6],[plot2, plot4, plot7], [plot3, plot5,plot8] ], plot_width=500, plot_height=300)
save(grid)
# show(layout)