# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 14:31:08 2020

@author: Matthew
"""
import numpy as np
import math, cv2
import matplotlib.pyplot as plt
import imageio
from scipy.ndimage import gaussian_filter as gfilt
import pointillism as poi, os

#params
sze = 1200
fps = 30
nprog = ''

readVidName = "facevid.mp4"
writeVidName = "facevid_point_"+str(nprog)

#load in video reader
cap = cv2.VideoCapture(readVidName)
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

#set up vid writer
#setup vid
fourcc = cv2.VideoWriter_fourcc(*'MP42')
fps = float(fps)
video_filename = './'+writeVidName+'.avi'
out = cv2.VideoWriter(video_filename, fourcc, fps, (800, 800))

for i in range(length):
    ret, im = cap.read()
    
    if (i%1)!=0:
        continue
    
    rows=np.arange(600)+100
    cols=np.arange(600)+325
    im=im[:,:,[2,1,0]][rows,:,:][:,cols,:]
    tempfil = 'pointprog'+str(nprog)+'/'+writeVidName+'_'+str(i)+'.png'
    poi.pointer(im, tempfil)
    im=imageio.imread(tempfil)
    out.write(im[:,:,[2,1,0]])
    
out.release()  
    