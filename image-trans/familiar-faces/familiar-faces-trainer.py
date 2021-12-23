# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 12:27:21 2021

@author: Matthew Ritch matt.ritch.33@gmail.com
"""

import numpy as np
import matplotlib.pyplot as plt
import glob
import scipy.misc
import skimage
import skimage.io
import skimage.transform
import model
from tensorflow.keras.callbacks import ModelCheckpoint

def train_generator():
    images=glob.glob("C:/Users/Matthew/Documents/gen-art-ims/familiar-faces/**/*.jpg", recursive = True)
    images.extend(glob.glob("C:/Users/Matthew/Documents/gen-art-ims/familiar-faces/**/*.png", recursive = True))
    while True:
        choice=images[np.random.randint(0,len(images))]
        try:
            im= skimage.io.imread(choice).astype(float)/255
            #make square (take center)
            if im.shape[0] != im.shape[1]:
                L = min(im.shape[:2])
                diff = np.floor((np.asarray(im.shape[:2]) - L)/2).astype(int)
                im = im [diff[0]:im.shape[0]-diff[0], diff[1]:im.shape[1]-diff[1], :] 
                
            im = skimage.transform.resize(im, [256, 256, 3])
            yield (np.expand_dims(im,0)), (np.expand_dims(im,0))
        except:
            continue


def main():     
    tr_generator=train_generator()    
    mName='ff_model2.hdf5'
    mName='ff_model_v4.hdf5'  
    #famfacesnet=model.autoencoder_model('ff_model.hdf5')
    famfacesnet=model.autoencoder_model(mName)
    #famfacesnet=model.autoencoder_model()
    mName = 'ff_model_v4-2.hdf5'  
    model_checkpoint = ModelCheckpoint(mName, monitor='loss',verbose=2, save_best_only=True) #saves model if performance increases
    if True:
        print("training model")
        famfacesnet.fit(tr_generator,steps_per_epoch=200,epochs=2*100,callbacks=[model_checkpoint])
    
    
    famfacesnet=model.autoencoder_model(mName)

if __name__ == "__main__":
    main()
    
    #show results
    gen = train_generator()
    
    #famfacesnet=model.autoencoder_model("ff_model_biggerlatent.hdf5")
    famfacesnet=model.autoencoder_model("ff_model_v4.hdf5")
    #famfacesnet=model.autoencoder_model("ff_model3.hdf5")
    
    for i in [0,1,2]:
        i=0+i
        im  =next(gen)
        plt.imshow(im[0][0,:,:,:])
        plt.show()
        out = famfacesnet.predict(im)
        for j in np.arange(0,25):
            out = famfacesnet.predict(out)
            plt.imshow(out[0,:,:,:])
            plt.show()
            skimage.io.imsave("modlong" + str(i) + "_" + str(j) + ".jpg", out[0,:,:,:])
        skimage.io.imsave("base" + str(i) + ".jpg", im[0][0,:,:,:])
        
    im = skimage.io.imread("IMG_3004.jpg")
    im = im.astype(float)/255
    L = min(im.shape[:2])
    diff = np.floor((np.asarray(im.shape[:2]) - L)/2).astype(int)
    im = im [diff[0]:im.shape[0]-diff[0], diff[1]:im.shape[1]-diff[1], :]
    im = skimage.transform.resize(im, [256, 256, 3])
    im = np.expand_dims(im,0)
    out = famfacesnet.predict(im)
    skimage.io.imsave("base_spec" + ".jpg", im[0,:,:,:])
    skimage.io.imsave("mod_spec" + ".jpg", out[0,:,:,:])
