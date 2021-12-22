# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 11:22:50 2021

@author: Matthew Ritch matt.ritch.33@gmail.com
"""

import numpy as np
import math, cv2
import matplotlib.pyplot as plt
import imageio
from scipy.ndimage import gaussian_filter as gfilt
from skimage.transform import resize

#params
imageName = "base-images/flanjpg_square.jpg"

#ni=2/np.max(minScale,maxScale)
#read in image
image  = np.asarray(imageio.imread(imageName)).astype(float)
sze=np.asarray(image.shape)#[::-1]
image=resize(image, [100,100,3])

dim=np.min(sze[:2])
image=image[:dim,:dim,:]

#plt.imshow(image)

invs=image.copy()
invs[:,:,0]=np.linalg.inv(image[:,:,0])
invs[:,:,1]=np.linalg.inv(image[:,:,1])
invs[:,:,2]=np.linalg.inv(image[:,:,2])

#invs = invs - np.min(invs)
#invs = invs/np.max(invs)

prod = image.copy()/255
prod[:,:,0]=np.matmul(prod[:,:,0],prod[:,:,0])
prod[:,:,1]=np.matmul(prod[:,:,1],prod[:,:,1])
prod[:,:,2]=np.matmul(prod[:,:,2],prod[:,:,2])

prod=prod/np.max(prod)
prod=(prod*255).astype('uint8')
#plt.imshow(prod)

imageio.imwrite("testout_4.jpg", invs)
#plt.imshow(np.matmul(invs[:,:,1],image[:,:,0]))