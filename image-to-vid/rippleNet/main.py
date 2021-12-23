# -*- coding: utf-8 -*-
"""
Created on Tue May  5 00:29:30 2020

@author: Matthew
"""

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import glob, os
import scipy.misc
import model, cv2
from keras.callbacks import ModelCheckpoint

def train_generator():
    images=glob.glob("data/images/*")
    L=len(images)
    while True:
        choice=images[np.random.randint(0,L)]
        _,vid=os.path.split(choice)
        splitters=[np.char.find(vid,'_'),np.char.find(vid,'.')]
        frame=int(vid[splitters[0]+1:splitters[1]])
        vid=int(vid[:splitters[0]])
        
        nextFrame=frame+1
        
        try:
            im0= scipy.misc.imread('data/images/%d_%5.5d.png' % (vid,frame) ).astype(float)/255
            im1= scipy.misc.imread('data/images/%d_%5.5d.png' % (vid,nextFrame) ).astype(float)/255
            yield (np.expand_dims(im1,0),np.expand_dims(im0,0))
        except:
            continue

generator=train_generator()       
rippleNet=model.unet()
        
mName='new_model.hdf5'
model_checkpoint = ModelCheckpoint(mName, monitor='loss',verbose=2, save_best_only=True) #saves model if performance increases
if False:
    rippleNet.fit_generator(generator,steps_per_epoch=200,epochs=1*100,callbacks=[model_checkpoint])


rippleNet=model.unet(mName)




filenames=['crouch_square','walking_square','matthew_square','garage_square','flanjpg_square']
#filenames=filenames[1]
for j in range(1):#range(len(filenames)):
    
    # initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*'MP42')
    fps = float(30)
    video_filename = './'+filenames[j]+'.avi'
    out = cv2.VideoWriter(video_filename, 1, fps, (512, 512))
    
    filename=filenames[j]
    im = scipy.misc.imresize(scipy.misc.imread('inputs/'+filename+".jpg"), (512,512,3)).astype(float)/255
    plt.imshow(im)
    
    im=np.expand_dims(im,0)
    for i in range(100):
        print(i)
        im=rippleNet.predict(im)
        im=np.clip(im,0,1)
        im_write=(im*255).astype('uint8')[0,:,:,:]
        im_write=im_write[:,:,[2,1,0]]
        out.write(im_write)
        if i<20:
            out.write(im_write)
        if i==70:
            im[:,150:-150,150:-150,:]=0
            
        if i==35:
            im=im[:,:,:,[0,2,1]]
        
    #    plt.imshow(im[0,:,:,:])
    #    plt.show()
    out.release()