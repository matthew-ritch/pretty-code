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
leng = 8


#make colormap
#h,v
start = np.array([50/2,50*2.55])
fin = np.array([200/2,80*2.55])

diff = (fin - start) / (leng-1)

colors = np.zeros((leng+1,2))
for i in range(leng+1):
    colors[i,:]=start+i*diff
colors=colors.astype(int)
sat = (2.55*np.arange(30, 100, (70/leng))).astype(int)



#initialize shape
center=[sze/2,sze/2]

#setup vid
fourcc = cv2.VideoWriter_fourcc(*'MP42')
fps = float(8)
video_filename = './'+'binary_color.avi'
out = cv2.VideoWriter(video_filename, fourcc, fps, (900, 900))
maxInd = (final_n-n_start)*steps


#define plotter
nBits = leng**2
fib_prev=0
fib_now=1
ind=0
maxVal=(2**(nBits)) -1

first=True


nSquares = np.zeros(leng)
while fib_now< maxVal:
      
       
    curr_bin_fib = format(fib_now, 'b')[-1::-1]
    #pad trailing zeros
    im=np.zeros((1,nBits,3))
    for i in range(len(curr_bin_fib)):
        if curr_bin_fib[i]=='1':
            #nada
            try:
                im[0,i,0]=colors[math.floor(i/leng),0]
                im[0,i,2]=colors[math.floor(i/leng),1]
                im[0,i,1]=sat[i%leng]
                #nade
            except:
                #do nothing
                print()
        #nada
    im=np.reshape(im,(leng,leng,3)).astype('uint8')
    
    

    im = cv2.cvtColor(im, cv2.COLOR_HSV2BGR)
        
    
    
    fig=mp.pyplot.figure(facecolor=(0,0,0),figsize=[3,3])
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
    
    temp = np.copy(fib_prev).astype(np.int64)
    
    fib_prev = np.copy(fib_now).astype(np.int64)
    fib_now = fib_now + temp.astype(np.int64)
    print(fib_now)
    if nSquares[-1]==leng:
        break
    #a=notavar
    if first:
        first = False
        fib_now = 1
    if ind>fps*20:
        break
    
out.release()      

            
            