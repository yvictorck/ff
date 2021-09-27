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
output_file("audio.html")

mypath = "./"

files = listdir(mypath)

audionames = []



for f in files:
  fullpath = join(mypath, f)
  if isfile(fullpath) and '.wav' in f:
    audionames.append(f.split('.wav')[0])
    print("檔案：", f)

audionames=sorted(audionames,key=lambda x: int( x.split('Hz')[0] ) )
# audionames=[audionames[3]]
colors = turbo(len(audionames))

numItems=len(audionames)
cols,rows = round(0.5+numItems**.5) , int(numItems**.5) 

figs=[]

mylay=[]
dlen=1024
cumdata=np.zeros([1,dlen])
alldata=[]
x1 =  np.linspace(0,dlen-1,dlen, endpoint=True)
fs=44100
bits_mag=16

import sys
sys.path.append('../ft')
import dft

i = 0

while i<len(audionames):
  filename = audionames[i]+'.wav'
  fs,rawdata  = read(filename)
  data=rawdata[0:dlen]

  alldata.append([data])
  cumdata = np.add(cumdata, data)  
  fig = Figure(title=audionames[i], plot_width=300, plot_height=200)
  fig.circle(x=x1,y=data,line_color=colors[i],line_width=0.5,alpha=1)
  fig.line(x=x1,y=data,line_color=colors[i],line_width=1,alpha=1)
  mylay.append(fig)

  fig = Figure(title=audionames[i]+' mag', plot_width=600, plot_height=200)
  fig.circle(x=dft.dft(bits_mag,fs,data)['freqs'],y=dft.dft(bits_mag,fs,data)['mag'],line_color=colors[i],line_width=0.5,alpha=1)
  fig.line(x=dft.dft(bits_mag,fs,data)['freqs'],y=dft.dft(bits_mag,fs,data)['mag'],line_color=colors[i],line_width=1,alpha=1)
  mylay.append(fig)

  fig = Figure(title=audionames[i]+' phase', plot_width=300, plot_height=200)
  fig.circle(x=dft.dft(bits_mag,fs,data)['freqs'],y=dft.dft(bits_mag,fs,data)['phase'],line_color=colors[i],line_width=0.5,alpha=1)
  fig.line(x=dft.dft(bits_mag,fs,data)['freqs'],y=dft.dft(bits_mag,fs,data)['phase'],line_color=colors[i],line_width=1,alpha=1)
  mylay.append(fig)
  i=i+1




fig = Figure(title='total data', plot_width=300, plot_height=200)
fig.circle(x=x1,y=cumdata[0],line_color=colors[-1],line_width=1,alpha=1)
mylay.append(fig)    

fig = Figure(title='total data'+' mag', plot_width=600, plot_height=200)
fig.circle(x=dft.dft(bits_mag,fs,cumdata[0])['freqs'],y=dft.dft(bits_mag,fs,cumdata[0])['mag'],line_color=colors[-1],line_width=.5,alpha=1)
fig.line(x=dft.dft(bits_mag,fs,cumdata[0])['freqs'],y=dft.dft(bits_mag,fs,cumdata[0])['mag'],line_color=colors[-1],line_width=1,alpha=1)
mylay.append(fig)

fig = Figure(title='total data'+' phase', plot_width=300, plot_height=200)
fig.circle(x=dft.dft(bits_mag,fs,cumdata[0])['freqs'],y=dft.dft(bits_mag,fs,cumdata[0])['phase'],line_color=colors[-1],line_width=.5,alpha=1)
fig.line(x=dft.dft(bits_mag,fs,cumdata[0])['freqs'],y=dft.dft(bits_mag,fs,cumdata[0])['phase'],line_color=colors[-1],line_width=1,alpha=1)
mylay.append(fig)

# i = 0
# while i<len(audionames):
#   filename = audionames[i]+'.wav'
#   fs,rawdata = read(filename)
#   data=rawdata[0:dlen]
#   fig = Figure(title=audionames[i], plot_width=300, plot_height=200)
#   fig.circle(x=x1,y=data,line_color=colors[i],line_width=0.5,alpha=1)
#   fig.line(x=x1,y=data,line_color=colors[i],line_width=1,alpha=1)
#   mylay.append(fig)

#   fig = Figure(title=audionames[i]+' mag', plot_width=600, plot_height=200)
#   fig.circle(x=dft.dft(bits_mag,fs,data)['freqs'],y=dft.dft(bits_mag,fs,data)['mag'],line_color=colors[i],line_width=0.5,alpha=1)
#   fig.line(x=dft.dft(bits_mag,fs,data)['freqs'],y=dft.dft(bits_mag,fs,data)['mag'],line_color=colors[i],line_width=1,alpha=1)
#   mylay.append(fig)

#   fig = Figure(title=audionames[i]+' phase', plot_width=300, plot_height=200)
#   fig.circle(x=dft.dft(bits_mag,fs,data)['freqs'],y=dft.dft(bits_mag,fs,data)['phase'],line_color=colors[i],line_width=0.5,alpha=1)
#   fig.line(x=dft.dft(bits_mag,fs,data)['freqs'],y=dft.dft(bits_mag,fs,data)['phase'],line_color=colors[i],line_width=1,alpha=1)
#   mylay.append(fig)


g=gridplot(mylay, ncols=3)
save(g,title='audio')






