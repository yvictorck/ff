#https://docs.bokeh.org/en/latest/docs/user_guide/interaction/callbacks.html
import numpy as np



from scipy.io.wavfile import write,read

from bokeh.layouts import column
from bokeh.models import ColumnDataSource, CustomJS, Slider
from bokeh.plotting import Figure, output_file, save
from bokeh.layouts import gridplot,layout

import itertools

from os import listdir
from os.path import isfile, isdir, join

from bokeh.palettes import Category10 as palette
from bokeh.palettes import turbo

mypath = "./"

files = listdir(mypath)

audionames = []


for f in files:
  fullpath = join(mypath, f)
  if isfile(fullpath) and '.wav' in f:
    audionames.append(f.split('.wav')[0])
    print("檔案：", f)

audionames=sorted(audionames,key=lambda x: int( x.split('Hz')[0] ) )
print(audionames)
# audionames=[audionames[1]]
colors = turbo(len(audionames))

numItems=len(audionames)
cols,rows = round(0.5+numItems**.5) , int(numItems**.5) 

figs=[]

mylay=[]
dlen=1000
cumdata=np.zeros([1,dlen])
alldata=[]
x1 =  np.linspace(0,dlen-1,dlen, endpoint=True)
fs=44100
bits_mag=16

import sys
sys.path.append('../ft')
import ctft

i = 0

# while len(colors)>3:
    # colors.pop()
# data['color'] = colors
# print(colors)
output_file("ftrans.html")

# x = [x*0.005 for x in range(0, 200)]
# y = x

# source = ColumnDataSource(data=dict(x=x, y=y))
for n in audionames:
  filename = n+'.wav'
  print(filename)
  fs,rawdata = read(filename)
  data=rawdata[0:dlen]
  cumdata = np.add(cumdata, data)  
  
info = ctft.ctft(fs,cumdata[0])
plot1 = Figure(title="original function", plot_width=800, plot_height=200)
plot1.line(x=info['t'],y=info['signal'],line_color='black',line_width=1,alpha=1)

plot2 = Figure(title="mag", plot_width=800, plot_height=200)
plot2.line(x=info['ws']/(2*np.pi),y=info['mag'],line_color='black',line_width=1,alpha=1)

plot3 = Figure(title="phase", plot_width=800, plot_height=200)
plot3.line(x=info['ws'],y=info['phase'],line_color='black',line_width=1,alpha=1)

plot4 = Figure(title="real Xw", plot_width=800, plot_height=200)
plot4.line(x=info['ws'],y=np.real(info['Xw']),line_color='black',line_width=1,alpha=1)

plot5 = Figure(title="img Xw", plot_width=800, plot_height=200)
plot5.line(x=info['ws'],y=np.round(np.imag(info['Xw']),7),line_color='black',line_width=1,alpha=1)

plot6 = Figure(title="inverse ctft abs", plot_width=800, plot_height=200)
plot6.line(x=info['t'],y=np.round(np.abs(info['xt']),7),line_color='black',line_width=1,alpha=1)

plot7 = Figure(title="inverse ctft real", plot_width=800, plot_height=200)
plot7.line(x=info['t'],y=np.round(np.real(info['xt']),7),line_color='black',line_width=1,alpha=1)

plot8 = Figure(title="inverse ctft phase", plot_width=800, plot_height=200)
plot8.line(x=info['t'],y=np.round(np.angle(info['xt']),7),line_color='black',line_width=1,alpha=1)

plot9 = Figure(title="inverse ctft imga", plot_width=800, plot_height=200)
plot9.line(x=info['t'],y=np.round(np.imag(info['xt']),7),line_color='black',line_width=1,alpha=1)

grid=gridplot([[plot1,plot6,plot7],[plot2,plot4,plot8],[plot3,plot5,plot9]], plot_width=500, plot_height=300)
# grid = gridplot([[plot1,slider,plot6],[plot2, plot4, plot7], [plot3, plot5,plot8] ], plot_width=500, plot_height=300)
save(grid)
# show(layout)