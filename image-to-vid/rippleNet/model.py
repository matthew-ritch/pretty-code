# -*- coding: utf-8 -*-
"""
Created on Tue May  5 01:08:33 2020

@author: Matthew
"""

import keras.models as models
import keras.layers as layers
import keras.optimizers as kOpt
from keras import backend as keras
import tensorflow as tf
#import tensorflow_probability as tfp

#define a few parameters
base_n=5
p=16
#this function is just shorthand for the base-2 exponential function
def f(x):
    return 2**x

def unet(pretrained_weights = None,input_shape = (512,512,3)):
    #see ronnenberger for architecture description
    
    inputs = layers.Input(input_shape,name='image_input')
    conv1 = layers.Conv2D(f(base_n), 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(inputs)
    conv1 = layers.Conv2D(f(base_n), 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv1)
    pool1 = layers.MaxPooling2D(pool_size=(2, 2))(conv1)
    #pool1= BatchNormalization(axis=3)(pool1)
    
    conv2 = layers.Conv2D(f(base_n+1), 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool1)
    #conv2= BatchNormalization(axis=3)(conv2)
    conv2 = layers.Conv2D(f(base_n+1), 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv2)
    pool2 = layers.MaxPooling2D(pool_size=(2, 2))(conv2)
    #pool2= BatchNormalization(axis=3)(pool2)
    
    conv3 = layers.Conv2D(f(base_n+2), 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool2)
    #conv3= BatchNormalization(axis=3)(conv3)
    conv3 = layers.Conv2D(f(base_n+2), 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv3)
    pool3 = layers.MaxPooling2D(pool_size=(2, 2))(conv3)
    #pool3= BatchNormalization(axis=3)(pool3)
    
    conv4 = layers.Conv2D(f(base_n+3), 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool3)
    #conv4= BatchNormalization(axis=3)(conv4)
    conv4 = layers.Conv2D(f(base_n+3), 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv4)
    drop4 = layers.Dropout(0.5)(conv4)
    pool4 = layers.MaxPooling2D(pool_size=(2, 2))(drop4)
    #pool4= BatchNormalization(axis=3)(pool4)
    
    conv5 = layers.Conv2D(f(base_n+4), 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool4)
    conv5 = layers.Conv2D(f(base_n+4), 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv5)
    drop5 = layers.Dropout(0.5)(conv5)
    
    up6 = layers.Conv2D(f(base_n+3), 2, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(layers.UpSampling2D(size = (2,2))(drop5))
    merge6 = layers.concatenate([drop4,up6], axis = 3)
    conv6 = layers.Conv2D(f(base_n+3), 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(merge6)
    conv6 = layers.Conv2D(f(base_n+3), 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv6)
    
    up7 = layers.Conv2D(f(base_n+2), 2, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(layers.UpSampling2D(size = (2,2))(conv6))
    merge7 = layers.concatenate([conv3,up7], axis = 3)
    conv7 = layers.Conv2D(f(base_n+2), 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(merge7)
    conv7 = layers.Conv2D(f(base_n+2), 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv7)
    
    up8 = layers.Conv2D(f(base_n+1), 2, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(layers.UpSampling2D(size = (2,2))(conv7))
    merge8 = layers.concatenate([conv2,up8], axis = 3)
    conv8 = layers.Conv2D(f(base_n+1), 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(merge8)
    conv8 = layers.Conv2D(f(base_n+1), 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv8)
    
    up9 = layers.Conv2D(f(base_n), 2, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(layers.UpSampling2D(size = (2,2))(conv8))
    merge9 = layers.concatenate([conv1,up9], axis = 3)
    conv9 = layers.Conv2D(f(base_n), 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(merge9)
    #conv9=Dropout(rate=.2)(conv9)
    conv9 = layers.Conv2D(f(base_n), 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv9)
    conv10 = layers.Conv2D(3, 1 ,activation = 'relu',padding = 'same')(conv9)
    
    model = models.Model(inputs = inputs, outputs = conv10) 
    model.compile(optimizer = kOpt.Adam(lr = 1E-4), loss = 'mean_squared_error', metrics = ['mean_absolute_error']) 
    #decay = 1E-4/100
    #load existing model if provided
    if(pretrained_weights):
    	model.load_weights(pretrained_weights)
    return model