# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 23:49:33 2020

@author: Matthew
"""
import numpy as np
import math, cv2
import matplotlib.pyplot as plt
import imageio
from scipy.ndimage import gaussian_filter as gfilt

#params
imageName = "../base-images/flanface_small.jpg"
maxScale = .01
minScale = .003
nNeighbors = 8
#ni=2/np.max(minScale,maxScale)
#read in image
image=np.mean(np.asarray(imageio.imread(imageName)).astype(float),axis=2)
image=image-np.min(image)
image=image/np.max(image)


sze=np.asarray(image.shape)#[::-1]
maxScale = maxScale*np.mean(sze)
minScale = minScale*np.mean(sze)


#seed somewhere
startpoint=np.floor(sze/2).astype(int)
#startpoint = [np.argmax(np.sum(image,axis=0)),np.argmax(np.sum(image,axis=1))]
#define all points as tree, new points come off in evenly spaced directions 
#at distance based on local intensity, preventing repeat points at too small of a distance
#TODO figure out how long this needs to run. max time needed in minScale^-1 in one direction, dunno how that translates

#outer loop for each additional time around the existing points
queue  =[]
queue.append(startpoint)

#add many points in grid to queue. This ensures every area gets seeded- does not span otherwise
gn=5
for i in range(gn):
    for j in range(gn):
        queue.append(np.asarray([sze[0]*(i/gn),sze[1]*(j/gn)]).astype(int))

maxindr = image.shape[0]*10
maxindc = image.shape[1]*10
existingpoints = np.zeros([maxindr, maxindc]) == 1
pts=[]
#TODO orient according to local gradient?
rads=2*math.pi*np.arange(nNeighbors)/nNeighbors
while queue:
    if len(queue)%500==0:
        print(len(queue))
    #get next seed point
    center = queue.pop(0).astype(int)
    #check for being too close to existing point
    check = existingpoints[np.floor(10*center[0]).astype(int), np.floor(10*center[1]).astype(int)]  
    if check:
        #if true skip this point
        continue
    dist=minScale+image[center[0],center[1]]*(maxScale-minScale)
    
    
    
    newpointsR=center[0]+dist*np.sin(rads)
    newpointsC=center[1]+dist*np.cos(rads)
    
    #a=notaver
    for i in range(len(newpointsR)):
        newpt=np.asarray([newpointsR[i],newpointsC[i]]).astype(int)
        
        #check if off edge of image
        check=(newpt[0]<0) | (newpt[1]<0) | (newpt[0]>=sze[0]) | (newpt[1]>=sze[1])
        if check:
            continue
        
        
        dist=minScale+image[newpt[0],newpt[1]]*(maxScale-minScale)
        
        #check for being too close to existing point
        check = existingpoints[np.floor(10*newpt[0]).astype(int), np.floor(10*newpt[1]).astype(int)]
        
        if check:
            #if true skip this point
            continue
        
        
        #else add to queue of points to add and paint existingpoints
        pts.append(newpt)
        queue.append(newpt)
        #change to existingpt dimensions
        newpt = 10* newpt
        slatdim = (2*np.floor(10*dist)+1).astype(int)
        cent = ((slatdim - 1)/2).astype(int)
        slatrow, slatcol = np.meshgrid(np.arange(slatdim), np.arange(slatdim), indexing='ij') - cent
        slat = np.concatenate((np.expand_dims(slatrow, axis=2), np.expand_dims(slatcol, axis=2)),axis=2)
        check = np.linalg.norm(slat, axis=2) < 10 * dist - 1
        rs, re, cs, ce = max(newpt[0]-cent, 0), min(newpt[0]+cent+1, maxindr), max(newpt[1]-cent,0), min(newpt[1]+cent+1, maxindc)
        corr_rs = rs - (newpt[0]-cent)
        corr_re = -(re - (newpt[0]+cent+1))
        corr_cs = cs - (newpt[1]-cent)
        corr_ce = -(ce - (newpt[1]+cent+1))
        existingpoints[rs:re, cs:ce] = check[corr_rs:slatdim-corr_re, corr_cs:slatdim-corr_ce]


# #get fig ready
fig=plt.figure(facecolor=(.8,.8,.8),figsize=[8,8*1])
plt.xlim([0,sze[0]])
plt.ylim([0,sze[1]])
plt.axis('off')
plt.gca().axis('off')
ax = plt.axes([0,0,1,1], frameon=False)
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
plt.autoscale(tight=False)

pts = np.asarray(pts)
plt.scatter(sze[1]-pts[:,1],sze[0]-pts[:,0],c='k',s =.30)
plt.show()
fig.savefig("curr-opt.png", dpi=400)
