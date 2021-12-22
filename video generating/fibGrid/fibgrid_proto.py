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


#initialize shape
center=[sze/2,sze/2]

#setup vid
fourcc = cv2.VideoWriter_fourcc(*'MP42')
fps = float(10)
video_filename = './'+'fibgrid_proto.avi'
out = cv2.VideoWriter(video_filename, fourcc, fps, (1200, 1200))
maxInd = (final_n-n_start)*steps

leng = 10

#define plotter
fib_prev=0
fib_now=1
ind=0
nBits = leng**2

first=True

while fib_now< 2**(nBits):
    curr_bin_fib = format(fib_now, 'b')[-1::-1]
    #pad trailing zeros
    im=np.zeros((1,nBits,3))
    for i in range(len(curr_bin_fib)):
        im[0,i,:]=int(curr_bin_fib[i])
    
    im=np.reshape(im,(leng,leng,3))
    
    
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
    fig.savefig("fibgrid_proto prog/step" + '_' + str(ind) ,facecolor = 'w', dpi = 150)
    im = np.asarray(scipy.misc.imread("fibgrid_proto prog/step" + '_' + str(ind)+".png")[:,:,:3]).astype('uint8')
    out.write(im[:,:,[2,1,0]])
    ind+=1
    plt.close('all')
    
    temp = fib_prev
    
    fib_prev = fib_now
    fib_now = fib_now + temp
    
    if first:
        first = False
        fib_now = 1
    
out.release()      

            
            
            
            
            
            