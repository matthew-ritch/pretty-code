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
    
maxScaled = .005*2
minScaled = .001*2
nNeighbors = 3


def pointer(image, fname):
    
    image=np.mean(np.asarray(image).astype(float),axis=2)
    image=image-np.min(image)
    image=image/np.max(image)
    sze=np.asarray(image.shape)#[::-1]
    maxScale = maxScaled*np.mean(sze)
    minScale = minScaled*np.mean(sze)
    
    #seed somewhere
    startpoint=np.floor(sze/2).astype(int)
    #startpoint = [np.argmax(np.sum(image,axis=0)),np.argmax(np.sum(image,axis=1))]
    #define all points as tree, new points come off in evenly spaced directions 
    #at distance based on local intensity, preventing repeat points at too small of a distance
    #TODO figure out how long this needs to run. max time needed in minScale^-1 in one direction, dunno how that translates
    
    #outer loop for each additional time around the existing points
    queue  =[]
    queue.append(startpoint)
    
    #add many points in grid to queue
    gn=5
    for i in range(gn):
        for j in range(gn):
            queue.append(np.asarray([sze[0]*(i/gn),sze[1]*(j/gn)]).astype(int))
    
    existingpoints = []
    existingpoints.append(startpoint)
    dists = []
    dists.append(minScale+image[startpoint[0],startpoint[1]]*(maxScale-minScale))
    #TODO orient according to local gradient?
    rads=2*math.pi*np.arange(nNeighbors)/nNeighbors
    while queue:
        #rads=(rads+np.random.rand()*math.pi)%math.pi
        #get next seed point
        center = queue.pop(0).astype(int)
        dist=minScale+image[center[0],center[1]]*(maxScale-minScale)
        newpointsR=center[0]+dist*np.sin(rads)
        newpointsC=center[1]+dist*np.cos(rads)
        exarray=np.asarray(existingpoints)
        distarray=np.asarray(dists)
        #a=notaver
        for i in range(len(newpointsR)):
            newpt=np.asarray([newpointsR[i],newpointsC[i]]).astype(int)
            #check if off edge of image
            check=(newpt[0]<0) | (newpt[1]<0) | (newpt[0]>=sze[0]) | (newpt[1]>=sze[1])
            if check:
                continue
            dist=minScale+image[newpt[0],newpt[1]]*(maxScale-minScale)
            #check for being too close to existing point
            check=np.linalg.norm(exarray-newpt,axis=1) <.6*distarray
            if np.any(check):
                continue
            #else add to queue of points to add
            queue.append(newpt)
            existingpoints.append(newpt)
            dists.append(dist)
    # #get fig ready
    fig=plt.figure(facecolor=(.8,.8,.8),figsize=[4,4])
    plt.xlim([0,sze[1]])
    plt.ylim([0,sze[0]])
    plt.axis('off')
    plt.gca().axis('off')
    ax = plt.axes([0,0,1,1], frameon=False)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    plt.autoscale(tight=False)
    
    
    plt.scatter(sze[1]-exarray[:,1],sze[0]-exarray[:,0],c='k',s =.4)
    fig.savefig(fname, dpi=200)