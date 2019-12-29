#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 11:32:05 2019

@author: simuser
"""
from math import sqrt

def velocity(track, steps_backward = 2):
    """ 
        calculates velocity of tracker, in px/s
        Args:
            track (sort.KalmanBoxTracker): the tracker
            steps_backward (int): the number of locations to look previously to determine velocity
        Returns:
            the speed of tracked object
    """
    # Return 0 if not enough locations
    # to be able to create velocity with
    if len(track.locations) < steps_backward:
        return 0
    prev_timestamp, prev_hitbox = track.locations[-steps_backward]
    current_timestamp, current_hitbox = track.locations[-1]
    # Divide by 1000 because of how unix is stored in ts
    dt = (current_timestamp - prev_timestamp) / 1000
    
    vel_x = (
            ((prev_hitbox[0] + prev_hitbox[2]) / 2)
            - ((current_hitbox[0] + current_hitbox[2] / 2)) / dt
            )
    
    vel_y = (prev_hitbox[3] - current_hitbox[3]) / dt
    
    ## want to get the total speed in one direction so will use pythagorian theorem
    vel = sqrt(vel_x*vel_x + vel_y*vel_y)
    return vel

def speed(locations, steps_backward=2):
    """ 
            calculates velocity of tracker, in px/s
            Args:
                track (sort.KalmanBoxTracker): the tracker
                steps_backward (int): the number of locations to look previously to determine velocity
            Returns:
                the speed of tracked object
    """
    # Return 0 if not enough locations
    # to be able to create velocity with
    if len(locations) < steps_backward:
        return 0
    prev_timestamp, prev_hitbox = locations.iloc[0,:]
    current_timestamp, current_hitbox =locations.iloc[-1,:]
    # Divide by 1000 because of how unix is stored in ts
    dt = (current_timestamp - prev_timestamp) / 1000
        
    vel_x = (
            ((prev_hitbox[0] + prev_hitbox[2]) / 2)
            - ((current_hitbox[0] + current_hitbox[2] / 2)) / dt
            )
        
    vel_y = (prev_hitbox[3] - current_hitbox[3]) / dt
        
    ## want to get the total speed in one direction so will use pythagorian theorem
    vel = sqrt(vel_x*vel_x + vel_y*vel_y)
    #print("previous:", prev_timestamp, prev_hitbox)
    #print("current:", current_timestamp, current_hitbox)
    return vel

