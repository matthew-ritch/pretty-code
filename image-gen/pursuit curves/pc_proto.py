# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 23:49:33 2020

@author: Matthew
"""
import numpy as np
import math, cv2
import matplotlib.pyplot as plt

#params
n = 10
sze = 1200
r=1.2
dx = 2
dx2 = 1
fps = 30
length = 30 # seconds

#setup vid
fourcc = cv2.VideoWriter_fourcc(*'MP42')
fps = float(fps)
video_filename = './'+'pc_proto.avi'
out = cv2.VideoWriter(video_filename, fourcc, fps, (sze, sze))

#start with n evenly spaced points on circle
center  = np.floor(sze/2)
rads = 2*math.pi*(np.arange(n)/n)
locs=np.zeros((n,2))
locs[:,0] = center + np.cos(rads)*r*center
locs[:,1] = center + np.sin(rads)*r*center

#assign some other point to pursue
pursue = (np.arange(n)+2) % n
repelby = (np.arange(n)+3) % n

#iterate towards point of pursuit. positions stack along third dim
positions = np.expand_dims(np.copy(locs),2)


#get fig ready
fig=plt.figure(facecolor=(0,0,0),figsize=[4,4])
plt.xlim([0,sze])
plt.ylim([0,sze])
plt.axis('off')
plt.xlim([0,sze])
plt.ylim([0,sze])
plt.gca().axis('off')
ax = plt.axes([0,0,1,1], frameon=False)
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
plt.autoscale(tight=False)

newlocs = locs
prevlocs = locs

for i in range(int(fps) * length):
    #a=notavar
    #prevlocs = positions[:,:,i]
    prevlocs = newlocs #reassignt to previous
    newlocs  = np.copy(prevlocs)
    diffs = newlocs[pursue,:] - prevlocs
    mag = np.linalg.norm(diffs, axis=1)
    diffs[:,0] = dx * diffs[:,0] / mag
    diffs[:,1] = dx * diffs[:,1] / mag
    #print(mag)
    newlocs+=diffs
    
    # diffs = newlocs[repelby,:] - prevlocs
    # mag = np.linalg.norm(diffs, axis=1)
    # diffs[:,0] = dx * diffs[:,0] / mag
    # diffs[:,1] = dx * diffs[:,1] / mag
    # #print(mag)
    # newlocs-=diffs
    
    
    #positions[:,:,i+1] = newlocs
    for j in range(n):
        rowStart = prevlocs[j,0]
        colStart = prevlocs[j,1]
        rowEnd = newlocs[j,0]
        colEnd = newlocs[j,1]
        plt.plot([rowStart,rowEnd],[colStart,colEnd],color= 'w',linewidth=1.5,figure=fig)
        
    #plot figure
fig=plt.figure(facecolor=(.8,.8,.8),figsize=[4,4])
plt.xlim([0,sze])
plt.ylim([0,sze])
plt.axis('off')
plt.xlim([0,sze])
plt.ylim([0,sze])
plt.gca().axis('off')
ax = plt.axes([0,0,1,1], frameon=False)
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
plt.autoscale(tight=False)    

fig.savefig("pc_proto", facecolor = 'k', dpi = 200)
    
    
#out.write()   
out.release()

