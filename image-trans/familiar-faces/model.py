# -*- coding: utf-8 -*-
"""
Created on Tue May  5 01:08:33 2020

@author: Matthew



"The most straightforward solution would go like this:

mid_layer = model.get_layer("layer_name")

you can now treat the "mid_layer" as a model, and for instance:

mid_layer.predict(X)

Oh, also, to get the name of a hidden layer, you can use this:

model.summary() 

this will give you some insights about the layer input/output as well.""


"""
from tensorflow import keras

#import tensorflow_probability as tfp

#define a few parameters
base_n=4
p=16
n_fc = 1024*3
#this function is just shorthand for the base-2 exponential function
def f(x):
    return 2**x

def autoencoder_model(pretrained_weights = None,input_shape = (256,256,3)):
    #see ronnenberger for architecture description
    
    inputs = keras.layers.Input(input_shape,name='image_input')
    
    #Begin Descending Branch
    conv1 = keras.layers.Conv2D(f(base_n), 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(inputs)
    conv1 = keras.layers.Conv2D(f(base_n), 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv1)
    pool1 = keras.layers.MaxPooling2D(pool_size=(2, 2))(conv1)
    
    conv2 = keras.layers.Conv2D(f(base_n+1), 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool1)
    conv2 = keras.layers.Conv2D(f(base_n+1), 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv2)
    pool2 = keras.layers.MaxPooling2D(pool_size=(2, 2))(conv2)
    
    conv3 = keras.layers.Conv2D(f(base_n+2), 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool2)
    conv3 = keras.layers.Conv2D(f(base_n+2), 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv3)
    pool3 = keras.layers.MaxPooling2D(pool_size=(2, 2))(conv3)
    
    conv4 = keras.layers.Conv2D(f(base_n+2), 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool3)
    conv4 = keras.layers.Conv2D(f(base_n+2), 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv4)
    drop4 = keras.layers.Dropout(0.5)(conv4)
    pool4 = keras.layers.MaxPooling2D(pool_size=(2, 2))(drop4)
    
    #BOTTOM LAYER    
    conv5 = keras.layers.Conv2D(f(base_n+3), 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool4)
    conv5 = keras.layers.Conv2D(f(base_n+3), 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv5)
    drop5 = keras.layers.Dropout(0.5)(conv5)
    flat = keras.layers.Flatten()(drop5)
    bottle   = keras.layers.Dense(n_fc)(flat)
    unbottle = keras.layers.Dense(drop5.shape[1]*drop5.shape[2]*f(base_n+3))(bottle)
    shaped = keras.layers.Reshape(drop5.shape[1:])(unbottle)
    
    #Begin Ascending Branch
    up6   = keras.layers.Conv2D(f(base_n+2), 2, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(keras.layers.UpSampling2D(size = (2,2))(shaped))
    conv6 = keras.layers.Conv2D(f(base_n+2), 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(up6)
    conv6 = keras.layers.Conv2D(f(base_n+2), 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv6)
    
    up7   = keras.layers.Conv2D(f(base_n+2), 2, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(keras.layers.UpSampling2D(size = (2,2))(conv6))
    conv7 = keras.layers.Conv2D(f(base_n+2), 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(up7)
    conv7 = keras.layers.Conv2D(f(base_n+2), 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv7)
    
    up8   = keras.layers.Conv2D(f(base_n+1), 2, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(keras.layers.UpSampling2D(size = (2,2))(conv7))
    conv8 = keras.layers.Conv2D(f(base_n+1), 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(up8)
    conv8 = keras.layers.Conv2D(f(base_n+1), 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv8)
    
    up9   = keras.layers.Conv2D(f(base_n), 2, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(keras.layers.UpSampling2D(size = (2,2))(conv8))
    conv9 = keras.layers.Conv2D(f(base_n), 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(up9)
    
    conv9 = keras.layers.Conv2D(f(base_n), 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv9)
    conv10 = keras.layers.Conv2D(3, 1 ,activation = 'relu', padding = 'same')(conv9)
    
    model = keras.models.Model(inputs = inputs, outputs = conv10) 
    model.compile(optimizer = keras.optimizers.Adam(lr = 1E-3), loss = 'mean_squared_error', metrics = ['mean_absolute_error']) 
    
    #load existing model if provided
    if(pretrained_weights):
    	model.load_weights(pretrained_weights)
    return model