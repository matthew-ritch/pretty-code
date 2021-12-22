# -*- coding: utf-8 -*-
"""
Created on Sun Dec 19 10:49:11 2021

@author: Matthew Ritch matt.ritch.33@gmail.com

cabbage

every point has strong attraction to the middle
    -invariant to distance?
points have strong attraction to their two chain neighbors
    -increase with distance
    -repulsion if get too close?
points have repulsion from every other point
    -drops off quickly with distance
"""

import math
import numpy as np
import matplotlib.pyplot as plt
import scipy


ind=0

def init_circle(center, radius, n_nodes):
    """
    makes initial curve with certain parameters
    """
    point_angles = np.random.rand(1)*math.pi + np.arange(0, 2*math.pi, step = 2*math.pi/n_nodes)
    x_coords = center[0] + radius * 4*np.cos(point_angles)
    y_coords = center[1] + radius * np.sin(point_angles)
    circle = np.stack((x_coords, y_coords), axis = 1)
    
    return circle

def grow_curve(curve, p_add = 1/9):
    """
    maybe adjust all points while we're at it? 
    will probably be more efficient than kicking it to the evolution step
    """
    L = curve.shape[0]
    insertion_inds = np.floor (np.arange(L, step =L * p_add)) .astype(int)
    insertion_inds = (np.random.rand(len(insertion_inds))*insertion_inds[0]*.5).astype(int)+insertion_inds
    insertion_inds= insertion_inds%L
    points = (curve[insertion_inds,:] + curve[insertion_inds-1,:]) * 0.5
    curve = np.insert(curve, insertion_inds+1, points, axis = 0)
    
    return curve

def calc_forces(curve, center):
    """
    forces are all calculated linearly - may make the modeling more sophisticated
    with square and inverse square laws. will see if needed
    """
    forces = np.zeros(curve.shape)
    
    n_nodes = curve.shape[0]
    n_forces = np.zeros(curve.shape)
    collision_forces = np.zeros(curve.shape)
    
    #calc center force
    curve = curve - center
    dists = np.linalg.norm(curve, axis=1)
    cent_forces = -1*np.stack((curve[:,0] / dists, curve[:,1]/dists) , 1)
    
    #calc neighbor forces
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
        #TODO right force is negative of circular shift left force
        n_forces [i,:] = -4*(left_force + right_force)
        
    #add collision forces 
    #get pairwise difference vectors (upper triangle)
    pair_diffs_x = np.zeros((n_nodes,n_nodes))
    pair_diffs_y = np.zeros((n_nodes,n_nodes))
    for i in range(n_nodes - 1):
        for j in np.arange(i+2, n_nodes):
            pair_diffs_x [i, j] = curve[i,0] - curve[j,0]
            pair_diffs_y [i, j] = curve[i,1] - curve[j,1]
    
    diffs=np.stack((pair_diffs_x, pair_diffs_y), axis=2)
    diffs[-1,0,:] = 0
    diffs[0,-1,:] = 0
    
    dists = np.linalg.norm(diffs, axis=2)
    
    #calculate forces (inverse square)
    f_mags = 1/(np.square(dists))
    f_mags[~np.isfinite(f_mags)] = 0
    f_x = diffs[:,:,0] * f_mags
    f_y = diffs[:,:,1] * f_mags
    #equal opposite reaction
    f_x = f_x - np.transpose (f_x)
    f_y = f_y - np.transpose (f_y)
    #vector points from other point to point force acts on. 
    #pos vector means positive force on point.
    #sum up along rows.
    f_x = np.sum(f_x, axis = 1)
    f_y = np.sum(f_y, axis = 1)
    collision_forces = 1* np.stack ((f_x, f_y), axis=1)
    
    #remove forces from neighbors and self
    
    #sum force components
    forces = 10*cent_forces + n_forces + collision_forces
    return forces

def evolve_curve(curve, evolve_steps, center): 
    global ind
    n_points = curve.shape[0]  
    for i in range(evolve_steps):
        forces = calc_forces(curve, center)
        steps = 0.02 * forces
        curve = curve + steps  
           
    
    return curve
    
    
    


def main():
    
    n_circles = 1
    center = (0,0) # coord will be transformed to frame coords after the shape is grown
    init_radius = 50
    init_n_nodes = 300
    ind=0
    seed=init_circle(center, init_radius, init_n_nodes)
    #normalize distances to heuristic
    heur_dist = np.linalg.norm(seed[0,:]-seed[1,:])
    seed = seed / heur_dist
    curve = seed.copy()
    for i in range(3000):
        curve=evolve_curve(curve, 1, center)
        if i%50 == 0:
            curve=grow_curve(curve)
        if i%2==0:
            #curve=grow_curve(curve)
            toplot = curve.copy()
            toplot = scipy.interpolate.CubicSpline (curve[:,0], curve[:,1])
            
            fig=plt.figure(facecolor=(0,0,0),figsize=[4,4])
            plt.axis('off')
            plt.gca().axis('off')
            ax = plt.axes( frameon=False)
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
            #plt.autoscale(tight=False)
    
            plt.plot(curve[:,0],curve[:,1], color='w')
            plt.plot([curve[-1,0],curve[0,0]],[curve[-1,1],curve[0,1]], color='w')
            #plt.show()
            plt.autoscale(tight=False)
            fig.savefig("out_test/step" + '_' + str(ind), dpi = 200, facecolor = 'k')
            ind+=1
            plt.close(fig)
    
    
    
if __name__ == "__main__":
    main()

