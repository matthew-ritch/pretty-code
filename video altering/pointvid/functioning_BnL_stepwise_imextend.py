# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 11:15:57 2020

@author: Matthew
first pass of algorithmically stitching videos together

look into:
    https://ieeexplore.ieee.org/document/723451 The problem of defining the Fourier transform of a colour image
    https://www.researchgate.net/publication/260670459_A_comparison_study_of_image_spatial_entropy
    
    
    
current idea: fourier shift for each frame, average in where best possibility is
questions: 
    how to get the part of the frame we actually want?
        -gaussian mix on all pixels/intensities/locations?
        -previously used kmeans to split into two degments, relying on black background. can make faster.
            -subsampling for speed, seems to work ok. can speed up
        -currently using color bounds filter to establish circle, as in fundus_circularfilter.py
            -testing how this works. more regular could be good
        
    compare new frame relative to what?
        -currently using have tried first image used
        -have tried running composite image
            -these two give roughly the same results
        -try comparing to previous image? every tenth?
        -compare every frame to every other frame? 
            -could be extremely noisy but give better metric
    
    method of shift comparison?
        -currently using fourier phase comparison
            -https://en.wikipedia.org/wiki/Phase_correlation
        -autocorrelation?
        -
    
    how to add in?
        -running average by number of times pixel is updated?
            -doing this with imtot and imupdates
        -only update when has not yet been updated?
            -doing this with im_extend
        
    how to find best images?
    -currently using TJ's method
    -https://arxiv.org/ftp/arxiv/papers/1609/1609.01117.pdf     
        
        
    hypothetical flow:
        1. sort by quality. best first
            -smooth first? entropy measures will find noisiest images first. can assume all are equally noisey?
        2. add next best quality image by extending and not averaging. maybe tweak adding algo to be near-perfect
        
   
#TODO add in rotation check. see that paper I was reading
        
        
        
use brown+Lowe method https://www.pyimagesearch.com/2018/12/17/image-stitching-with-opencv-and-python/
"""

##debug moving
import os
os.chdir(r'C:\Users\Matthew\Desktop\io\my code')

import numpy as np, glob, os, matplotlib as mp, time, cv2
import matplotlib.pyplot as plt
import sklearn.cluster as clu
from PIL import Image
import data, brown_lowe, scipy.signal as sig, math
from scipy import ndimage
import pyr_blend as pyr
import scipy.signal
import scipy.misc
import imageio
import use_frame_classifier as ufc
import pickle
import skimage.transform

# %% params
f= 1 #1 out of f are sampled for the clustering. speeds everything up
pad=300

# %% setup
rot=cv2.rotate

modfilename = 'finalized_frameclass_model_06252020.sav'
loaded_model = pickle.load(open(modfilename, 'rb'))
sze=512


# navigate to files

os.chdir("..")
filesHome= "video data/Fundus Videos-20200211T160552Z-001/Fundus Videos"
fileNames=['Test_01','Test_02','Test_03','Test_03','Test_04','Test_05','Test_06','Test_07','Test_08','Test_09']
#fileNames=['Test_03']

os.chdir(filesHome)


for fileName in fileNames:
    # Open the video and initialize arrays
    cap = cv2.VideoCapture(fileName+'.mov')
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    
    # %%get sharpness metric for each frame
    if not os.path.exists(fileName+'_sharpness.npy'):
        frame_sharpness, blocks_number, frames = data.assess_sharpness(cap)
        np.save(fileName+'_sharpness',frame_sharpness)
    else:
        frame_sharpness = np.load(fileName+'_sharpness.npy')
    #frame_sharpness=frame_sharpness 
    
    
    order=np.flip(np.argsort(frame_sharpness))
    order = [*range(0, length, f)] 
    cap.set(cv2.CAP_PROP_POS_FRAMES, order[0]) 
    
    # %% get first image as basis
    
    
    # %% iterate through remaining frames, calculate offset, and add to the updating images
    
    
    first=True
    for j in range(len(order)):
        print(j)
        cap.set(cv2.CAP_PROP_POS_FRAMES, order[j])
         # read in next frame
        try:
             ret, im = cap.read()
        except:
            print("frame not able to be read")
            continue
        #a=notavar
        im=rot(im, 0)
        #print(j)
        try:
             label = ufc.classify(im[:,:,[2,1,0]])
        except:
            print("frame not able to be classified")
            continue
        
        #%% do labeling
        #cats= Blurry, Cont, Dark/Black, External, Good, obs
        
        print(label)
        if not label==4:
            continue
        # else:
        #     print("good")
            
            
        if first:
            #initialize updating variables
            im0=np.copy(im)
            im0, mask=data.makecrop_circle(im0)
            im0 = np.pad(im0,((pad,pad),(pad,pad),(0,0)),mode='constant')
            mask = np.logical_not(np.sum(im0,2)==0)
            im_extend=np.copy(im0)
            mask_extend=np.copy(mask)
            
            first=False
            continue
        
        
        try:
            im, mask = data.makecrop_circle(im)
        except:
            print("frame not able to be cropped")
            continue
        im = np.pad(im,((pad,pad),(pad,pad),(0,0)),mode='constant')
        mask = np.pad(mask,((pad,pad),(pad,pad)),mode='constant')
    
        try:
            im, mask = brown_lowe.adjust_new_image(im,im_extend, (1*mask).astype('uint8'))
        except: 
            #a=notavar
            print("frame not able to be b+l'd")
            continue
        
        mask = mask>0
        if not np.any(mask):
            print("no new areas")
            continue
        newParts = mask & np.logical_not(mask_extend)
        oldParts = mask_extend & np.logical_not(mask)
        overlap  = mask & mask_extend
        
        # if np.sum(newParts)>.2*np.sum(oldParts):
        #     print("too large update")
        #     continue
        
        #gain compensation
        closeToNew = (scipy.signal.convolve2d(1*newParts,np.ones((20,20)),'same')>0) & overlap
        
        meansOld = np.asarray(  [np.mean(im_extend[:,:,0][closeToNew]), np.mean(im_extend[:,:,1][closeToNew]), np.mean(im_extend[:,:,2][closeToNew])]  )
        meansNew = np.asarray(  [np.mean(im[:,:,0][newParts]), np.mean(im[:,:,1][newParts]), np.mean(im[:,:,2][newParts])]  )
        ratios = meansOld/meansNew
        for i in range(3):
            im[:,:,i]=im[:,:,i]*ratios[i]
        
        
        #conv to help reduce edge difference
        A=np.ones((5,5))/25
        weights = scipy.signal.convolve2d(1.0*newParts, A, mode='same')
        weights = scipy.signal.convolve2d(1*weights, A, mode='same')
        weights = scipy.signal.convolve2d(1*weights, A, mode='same')
        weights = scipy.signal.convolve2d(1*weights, A, mode='same')
        weights = scipy.signal.convolve2d(1*weights, A, mode='same')
        weights=weights/np.max(weights)
        weights[newParts]=1
        weights = np.tile(np.expand_dims(weights,2),(1,1,3))
        where=weights>0
        
        im_extend[where] = im[where]*weights[where]+im_extend[where]*(1-weights[where])
        
    
        
        #easy add
        #im_extend[newParts]=im[newParts]
        mask_extend = mask_extend | newParts[:,:]
        mask_extend[np.sum(im_extend,2)<20]=False
        
        print(j)
        if (j%5==0):
            #plt.imshow(cv2.cvtColor(im_pyr, cv2.COLOR_BGR2RGB))
            plt.imshow(cv2.cvtColor(im_extend, cv2.COLOR_BGR2RGB))
            plt.show()
    
    
    cap.release()
    cv2.destroyAllWindows()
    
    imageio.imsave(fileName+'_f='+str(f)+'_unsharp_06252020.jpg', im_extend[:,:,[2,1,0]])







    
    
    
    
    
    
    
    
    
    
    