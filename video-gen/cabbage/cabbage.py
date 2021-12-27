# -*- coding: utf-8 -*-
"""
Created on Sun Dec 19 10:49:11 2021

@author: Matthew Ritch matt.ritch.33@gmail.com

cabbage

every point has strong attraction to the middle
    -stronger away from middle distance
points have strong attraction to their two chain neighbors
    -increase with distance
    -repulsion if get too close
points have repulsion from every other point
    -drops off quickly with distance
"""

import math #:)
import numpy as np
import matplotlib.pyplot as plt
from numba import jit


ind=0
#%%
def init_circle(center, radius, n_nodes):
    """
    makes initial curve with certain parameters
    """
    point_angles = np.random.rand(1)*math.pi + np.arange(0, 2*math.pi, step = 2*math.pi/n_nodes)
    x_coords = center[0] + radius * np.cos(point_angles)
    y_coords = center[1] + radius * np.sin(point_angles)
    circle = np.stack((x_coords, y_coords), axis = 1)
    
    return circle
#%%
#@jit(nopython=True)
def grow_curve(curve, p_add = .1):
    """
    maybe adjust all points while we're at it? 
    will probably be more efficient than kicking it to the evolution step
    """
    L = curve.shape[0]
    insertion_inds = np.floor (np.arange(L, step =L * p_add)) .astype(int)
    insertion_inds = (np.random.rand(len(insertion_inds))*insertion_inds[0]*.5).astype(int)+insertion_inds
    insertion_inds= insertion_inds % L
    points = (curve[insertion_inds,:] + curve[insertion_inds+1,:]) * 0.5
    curve = np.insert(curve, insertion_inds+1, points, axis = 0)
    
    return curve
#%%
#@jit(nopython=True)
def grow_curve_close(curve, p_add = .2):
    """
    maybe adjust all points while we're at it? 
    will probably be more efficient than kicking it to the evolution step
    """
    L = curve.shape[0]
    n = np.linalg.norm(curve, axis = 1)
    inds = np.argsort(n)
    insertion_inds = inds [0:np.floor(L*p_add).astype(int)]
    insertion_inds= insertion_inds % L
    points = (.5*curve[insertion_inds,:] + .5*curve[(insertion_inds+1) % L,:])
    curve = np.insert(curve, (insertion_inds+1) % L, points, axis = 0)
    return curve
#%%
#@jit(nopython=True)
def grow_curve_curve(curve, p_add = .1):
    """
    maybe adjust all points while we're at it? 
    will probably be more efficient than kicking it to the evolution step
    """
    L = curve.shape[0]
    temp = curve.copy()
    left =  np.roll(temp, shift = -1, axis=0) - temp
    right = np.roll(temp, shift = 1, axis=0) - temp
    ###
    inds =  np.sum(left * right, axis = 1)
    inds = np.argsort(-inds)
    insertion_inds = inds [0:np.floor(L*p_add).astype(int)]
    insertion_inds= insertion_inds % L
    points = (.5*curve[insertion_inds,:] + .5*curve[(insertion_inds+1) % L,:])
    curve = np.insert(curve, (insertion_inds+1) % L, points, axis = 0) 
    return curve
#%%
#@jit(nopython=True)
def grow_curve_length(curve, p_add = .05):
    """
    maybe adjust all points while we're at it? 
    will probably be more efficient than kicking it to the evolution step
    """
    L = curve.shape[0]
    temp = curve.copy()
    right = np.roll(temp, shift = 1, axis=0) - temp
    dists = np.linalg.norm(right, axis=1)   
    
    inds = np.argsort(-dists)
    insertion_inds = inds [0:np.floor(L*p_add).astype(int)]
    insertion_inds= insertion_inds % L
    points = (.5*curve[insertion_inds,:] + .5*curve[(insertion_inds+1) % L,:])
    curve = np.insert(curve, (insertion_inds+1) % L, points, axis = 0)   
    return curve
#%%
#@jit(nopython=True)
def calc_forces(curve, center):
    """
    :)
    """
    forces = np.zeros(curve.shape)  
    n_nodes = curve.shape[0]
    n_forces = np.zeros(curve.shape)
    collision_forces = np.zeros(curve.shape)    
    #%% calc center force
    curve = curve - center
    dists = np.linalg.norm(curve, axis=1)
    cent_forces = np.stack((curve[:,0] * dists, curve[:,1] * dists) , 1)
    
    #calc spiral force
    spiral_f=1*cent_forces[:,[1,0]]
    spiral_f[:,1]=-1*spiral_f[:,1]
        
    #%%calc neighbor forces
    #want the points to remain the heuristic distance apart- normed to 1 unit distance earlier
    for i in range(n_nodes):
        neighbors = [(i-1) % n_nodes, (i+1) % n_nodes]
        
        #vector points from neighbor to point
        left_neighbor_vec =   curve[i,:] - curve[neighbors[0],:]
        right_neighbor_vec =  curve[i,:] - curve[neighbors[1],:]
        #calculate distance
        left_dist = np.linalg.norm(left_neighbor_vec)
        right_dist = np.linalg.norm(right_neighbor_vec)
        #calculate force. positive forces point away from neighbor
        left_force = (left_dist - 1) * left_neighbor_vec
        right_force = (right_dist - 1) * right_neighbor_vec
        #TODO right force is negative of circular shift left force. optimize.
        n_forces [i,:] = -1*(left_force + right_force)
        
    #%%calcs collision forces
    #TODO optimize
    # #get pairwise difference vectors (upper triangle)
    #new method
    x_posn = curve[:,0,np.newaxis]
    y_posn = curve[:,1,np.newaxis]
    x_grid = np.repeat(x_posn, n_nodes, axis=1)
    y_grid = np.repeat(y_posn, n_nodes, axis=1)
    pair_diffs_x = x_grid - np.transpose(x_grid)
    pair_diffs_y = y_grid - np.transpose(y_grid)   
    
    diffs=np.stack((pair_diffs_x, pair_diffs_y), axis=2)
    dists = np.linalg.norm(diffs, axis=2)
    
    for i in range(n_nodes):
        dists[i,(i-1)%n_nodes]=0
        dists[i,(i+1)%n_nodes]=0
    
    #calculate forces (inverse square)
    f_mags = 1/(np.square(dists))
    f_mags[~np.isfinite(f_mags)] = 0
    f_x = diffs[:,:,0] * f_mags
    f_y = diffs[:,:,1] * f_mags
    #vector points from other point to point force acts on. 
    #pos vector means positive force on point.
    #sum up along rows.
    f_x = np.sum(f_x, axis = 1)
    f_y = np.sum(f_y, axis = 1)
    collision_forces = 1* np.stack ((f_x, f_y), axis=1)
    ###########
    
    #sum force components
    forces = -.25*cent_forces + 4*n_forces + 3*collision_forces + 0*spiral_f
    return forces
#%%
#@jit(nopython=True)
def evolve_curve(curve, evolve_steps, center): 
    global ind
    n_points = curve.shape[0]  
    for i in range(evolve_steps):
        forces = calc_forces(curve, center)
        steps = 0.001 * forces
        curve = curve + steps  
    return curve  
#%%

def main():
    n_circles = 1
    center = np.asarray((0,0)) # coord will be transformed to frame coords after the shape is grown
    init_radius = 10
    init_n_nodes = 100
    ind=0
    
    seed=init_circle(center, init_radius, init_n_nodes)
    #normalize distances to heuristic
    heur_dist = np.linalg.norm(seed[0,:]-seed[1,:])
    seed = seed / heur_dist
    curve = seed.copy()
    for i in range(1000):
        curve=evolve_curve(curve, 2, center)
        if (i%6 == 0):  #and (i<25):
            curve=grow_curve_length(curve, p_add = .05)
            curve=grow_curve_curve(curve, p_add = .05)
            #curve=grow_curve(curve, p_add=.05)
        if i%1==0: #plot fig
            
            fig=plt.figure(facecolor='grey',figsize=[5,5])
            plt.axis('off')
            plt.gca().axis('off')
            ax = plt.axes( frameon=False)
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
            plt.autoscale(tight=False)
            
    
            plt.plot(curve[:,0],curve[:,1], color='k')
            plt.plot([curve[-1,0],curve[0,0]],[curve[-1,1],curve[0,1]], color='k')
            #plt.show()
            fig.savefig("out-2/step" + '_' + str(ind), dpi = 200, facecolor = 'grey')#, bbox_inches='tight')
            ind+=1
            plt.close(fig)
    
if __name__ == "__main__":
    main()