# -*- coding: utf-8 -*-
"""
Created on Sun Dec 19 14:25:36 2021

@author: Matthew Ritch matt.ritch.33@gmail.com
"""

import cv2, glob, skimage.io
import numpy as np


fourcc = cv2.VideoWriter_fourcc(*'MP4V')
fps = float(15)
video_filename = './'+'collapse.mp4'
out = cv2.VideoWriter(video_filename, fourcc, fps, (660, 660))

files = glob.glob("out-2/*.png")
for i in range ( len (files)):
    
    im = np.asarray(skimage.io.imread("out-2\\step_"+str(i)+".png")).astype('uint8')
    im = np.pad (im, ((8, 8), (0, 0), (0, 0)))
    out.write(im[:,:,[2,1,0]])
    if i > len(files)-5:
        out.write(im[:,:,[2,1,0]])
    
for i in range(15):
    out.write(im[:,:,[2,1,0]])

out.release()      
