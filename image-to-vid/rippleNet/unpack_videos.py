# -*- coding: utf-8 -*-
"""
Created on Tue May  5 00:14:44 2020

@author: Matthew
"""

import os, cv2, glob
import scipy.misc
import numpy as np
import matplotlib.pyplot as plt

files=glob.glob("data/videos/*")

for i in range(len(files)):
    cap = cv2.VideoCapture(files[i])
   
    
    j=0
    while True:
        
        try:
             ret, im = cap.read()
        except:
            break
        try:
            #im=cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
            im=np.asarray(im)
            im=im[:,:,[2,1,0]]
            im=scipy.misc.imresize(im,(512,512,3))
             
             
            scipy.misc.imsave('data/images/%d_%5.5d.png' % (i,j) , im)
        except:
            break
        
        j+=1