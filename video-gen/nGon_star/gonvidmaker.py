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
final_n = 20
steps = 30
nam = 'gist_heat'
cmap=mp.pyplot.get_cmap(nam)
rand=True


#initialize shape
center=[sze/2,sze/2]

#setup vid
fourcc = cv2.VideoWriter_fourcc(*'MP42')
fps = float(30)
video_filename = './'+'ngon_simple_rand.avi'
out = cv2.VideoWriter(video_filename, fourcc, fps, (1200, 1200))
maxInd = (final_n-n_start)*steps

#define converter
def fig2data ( fig ):
    """
    @brief Convert a Matplotlib figure to a 4D numpy array with RGBA channels and return it
    @param fig a matplotlib figure
    @return a numpy 3D array of RGBA values
    """
    # draw the renderer
    fig.canvas.draw ( )
 
    # Get the RGBA buffer from the figure
    w,h = fig.canvas.get_width_height()
    buf = np.fromstring ( fig.canvas.tostring_rgb(), dtype=np.uint8 )
    buf.shape = ( w, h,3 )
 
    # canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
    buf = np.roll ( buf, 3, axis = 2 )
    return buf

#define plotter
def plotTheseCoords(coords,ind):
    #coords is (rowCoords,colCoords)
    pts = len(coords[0])
    
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
    for i in range(len(coords[0])):
        for j in np.arange(1,len(coords[0]),1):
            rowStart = coords[0][i]
            colStart = coords[1][i]
            rowEnd = coords[0][j]
            colEnd = coords[1][j]
            thck=1.5*ind/maxInd
            mp.pyplot.plot([rowStart,rowEnd],[colStart,colEnd],color= 'k',linewidth=2.5-thck,figure=fig)

    
    #mp.pyplot.savefig("gonvid prog/step" + '_' + str(ind) ,facecolor = 'k', dpi = 200)
    fig.savefig("gonvid prog/step" + '_' + str(ind) ,facecolor = 'w', dpi = 300)
    #arr = fig2data(fig)
#    canvas = FigureCanvas(fig)
#    canvas.draw()
#    # grab the pixel buffer and dump it into a numpy array
#    X = np.array(canvas.renderer.buffer_rgba())
    #a=notavar
    





#mp.pyplot.rcParams['axes.facecolor'] = 'black'
ind=0
#n is old number of sides
for n in np.arange(n_start, final_n+1):
    #previous side lengths
    old_rads = np.array((2*math.pi)*np.arange(n)/(n))
    old_rads=np.append(old_rads,old_rads[0])
    #new side lengths
    new_rads = np.array((2*math.pi)*np.arange(n+1)/(n+1))
    new_rads=np.append(new_rads,new_rads[0])
    
    prog_rads=np.append(old_rads[0],old_rads)
    #display current stationary
    if rand:
        np.random.shuffle(new_rads)
    #display moving
    for i in range(steps):
        
        new_rads[(new_rads-prog_rads)<0]=new_rads[(new_rads-prog_rads)<0]+2*math.pi
        
        current_rads = ((i+1)/steps)*new_rads +((steps-(i+1))/steps)*prog_rads
        rowCoords = np.round(center[0] + r * np.sin(current_rads)).astype(int)
        colCoords = np.round(center[1] + r * np.cos(current_rads)).astype(int)
        coords = (rowCoords,colCoords)
        
        plotTheseCoords(coords,ind)
        im = np.asarray(scipy.misc.imread("gonvid prog/step" + '_' + str(ind)+".png")[:,:,:3]).astype('uint8')
        out.write(im[:,:,[2,1,0]])
        ind+=1
        plt.close('all')
out.release()      

            
            
            
            
            
            