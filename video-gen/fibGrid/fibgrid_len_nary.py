# -*- coding: utf-8 -*-
"""
Created on Sun May 31 09:06:37 2020

@author: Matthew
"""

import matplotlib as mp
import matplotlib.pyplot as plt
import numpy as np
import math, cv2, scipy.misc
from matplotlib.backends.backend_agg import FigureCanvas

#params
sze = 1024
r = round(sze*.45)
n_start = 3
final_n = 25
steps = 900
nam = 'gist_heat'
cmap=mp.pyplot.get_cmap(nam)
rand=True
leng = 10


#make colormap
#h,v
start = np.array([268/2,64*2.55])
fin = np.array([172/2,77*2.55])

diff = (start - fin) / (leng-1)

colors = np.zeros((leng,2))
for i in range(leng):
    colors[i,:]=start+i*diff
colors=colors.astype(int)
sat = (2.55*np.arange(30, 100, (70/leng))).astype(int)



#initialize shape
center=[sze/2,sze/2]

#setup vid
fourcc = cv2.VideoWriter_fourcc(*'MP42')
fps = float(7)
video_filename = './'+'fibgrid_lengfill_leng10.avi'
out = cv2.VideoWriter(video_filename, fourcc, fps, (1200, 1200))
maxInd = (final_n-n_start)*steps


#define plotter
fib_prev=0
fib_now=1
ind=0
maxVal=(leng**(leng+1)) -1

first=True


nSquares = np.zeros(leng)
while fib_now< maxVal:
    im = np.zeros((leng,leng,3)).astype('uint8')
    rem = 1*fib_now
    
    if rem !=0:
        for i in range(leng):
            ind1 = (leng-1)-i #index from back
            val = int(np.floor_divide(rem, (leng**ind1) ))
            nSquares[ind1]=val
            rem = rem % (leng**ind1)
            
            im[ind1,:val,0] = colors[ind1,0]
            im[ind1,:val,2] = colors[ind1,1]
            im[ind1,:val,1] = sat[:val]
    
    im = cv2.cvtColor(im, cv2.COLOR_HSV2BGR)
        
    
    
    fig=mp.pyplot.figure(facecolor=(0,0,0),figsize=[4,4])
    mp.pyplot.xlim([0,sze])
    mp.pyplot.ylim([0,sze])
    mp.pyplot.axis('off')
    mp.pyplot.xlim([0,sze])
    mp.pyplot.ylim([0,sze])
    mp.pyplot.gca().axis('off')
    ax = plt.axes([0,0,1,1], frameon=False)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    mp.pyplot.autoscale(tight=False)
    mp.pyplot.imshow(im,figure=fig)
    fig.savefig("fibgrid_proto prog/step" + '_' + str(ind) ,facecolor = 'w', dpi = 300)
    im = np.asarray(scipy.misc.imread("fibgrid_proto prog/step" + '_' + str(ind)+".png")[:,:,:3]).astype('uint8')
    out.write(im[:,:,[2,1,0]])
    ind+=1
    plt.close('all')
    
    temp = fib_prev
    
    fib_prev = fib_now
    fib_now = fib_now + temp
    
    if nSquares[-1]==leng:
        break
    
    if first:
        first = False
        fib_now = 1
    
out.release()      

            
            
            
            
            
            