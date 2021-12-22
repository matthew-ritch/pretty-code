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


ind=0

def init_circle(center, radius, n_nodes):
    """
    makes initial curve with certain parameters
    """
    point_angles = np.random.rand(1)*math.pi + np.arange(0, 2*math.pi, step = 2*math.pi/n_nodes)
    x_coords = center[0] + radius * np.cos(point_angles)
    y_coords = center[1] + radius * np.sin(point_angles)
    circle = np.stack((x_coords, y_coords), axis = 1)
    
    return circle

def grow_curve(curve, p_add = .2444):
    """
    maybe adjust all points while we're at it? 
    will probably be more efficient than kicking it to the evolution step
    """
    L = curve.shape[0]
    insertion_inds = np.floor (np.arange(L, step =L * p_add)) .astype(int)
    points = (curve[insertion_inds,:] + curve[insertion_inds+1,:]) * 0.5
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
        
    #add all other forces (from other parts of the curve)
    
    
    #sum force components
    forces = cent_forces + n_forces + collision_forces
    return forces

def evolve_curve(curve, evolve_steps, center): 
    global ind
    n_points = curve.shape[0]  
    for i in range(evolve_steps):
        forces = calc_forces(curve, center)
        steps = 0.01 * forces
        curve = curve + steps  
        
        fig=plt.figure(facecolor=(0,0,0),figsize=[4,4])
        plt.axis('off')
        plt.gca().axis('off')
        ax = plt.axes([0,0,1,1], frameon=False)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        plt.autoscale(tight=False)
        
        plt.plot(curve[:,0],curve[:,1], color='w')
        plt.plot([curve[-1,0],curve[0,0]],[curve[-1,1],curve[0,1]], color='w')
        fig.savefig("out_test/step" + '_' + str(ind), dpi = 100, facecolor = 'k')
        ind+=1
        plt.close(fig)
    
    
    return curve
    
    
    


def main():
    
    n_circles = 1
    center = (0,0) # coord will be transformed to frame coords after the shape is grown
    init_radius = 50
    init_n_nodes = 400
    
    seed=init_circle(center, init_radius, init_n_nodes)
    #normalize distances to heuristic
    heur_dist = np.linalg.norm(seed[0,:]-seed[1,:])
    seed = seed / heur_dist
    curve = seed.copy()
    for i in range(300):
        curve=evolve_curve(curve, 10, center)
        if i%100:
            curve=grow_curve(curve)
        if i%1==0:
            
            
            a=[]
            # fig=plt.figure(facecolor=(0,0,0),figsize=[4,4])
            # plt.axis('off')
            # plt.gca().axis('off')
            # ax = plt.axes([0,0,1,1], frameon=False)
            # ax.get_xaxis().set_visible(False)
            # ax.get_yaxis().set_visible(False)
            # plt.autoscale(tight=False)
    
            # plt.plot(curve[:,0],curve[:,1], color='w')
            # plt.show()
            
            # fig.savefig("fibgrid_proto prog/step" + '_' + str(ind) ,facecolor = 'w', dpi = 300)
            # im = np.asarray(scipy.misc.imread("fibgrid_proto prog/step" + '_' + str(ind)+".png")[:,:,:3]).astype('uint8')
    
    
    
if __name__ == "__main__":
    main()

