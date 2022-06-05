#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 13:52:41 2022

@author: Yu-Chieh Hsiao
"""
import random
import numpy as np

# k means clustering
def kmeans_clustering(inputs):
    
    n = len(inputs[0])
    
    tole = 1e-3
    k = 1 # number of cluster starting from 1
    J = 10e9
    J_ = []
    means_ = []
    k_ = []
    means_rec = []
    clusters_rec = []
    
    while(True):
        
        # Randomly assign starting points based on k number of cluster
        start_ = random.sample(range(0, n - 1), k)
        means_ = []
        for i in range(k):
            means_.append(inputs[:, start_[i]])
            
        pre_means = [[0]*18]*k
        
        # For each k, find the best result
        while(True):
            
            stop_flag = 0
            clusters = [[] for x in range(k)]
            
            for i in range(n):
                
                # distance between k number of cluster
                dist_ = []
                for j in range(k):
                    
                    # for each cluster, append the distance
                    dist_.append(find_distance_mean(i, means_[j], inputs))
                
                # Find the smallest distance and assign the point to the cluster
                index_min = dist_.index(np.min(dist_))
                clusters[index_min].append(i)
            
            # Update the new means of each cluster
            pre_means = means_
            means_ = []
            
            for i in range(k):
                means_.append(find_mean(clusters[i], inputs))
                
            for i in range(k):
                if find_diff(means_[i], pre_means[i]) > tole:
                    stop_flag =+ 1
            
            if stop_flag == 0:
                break
            
        # Calculate the cost
        J = 0
        for i in range(k):
            for l in range(len(clusters[i])):
                J = J + find_distance_mean(clusters[i][l], means_[i], inputs)
    
        # Record the result of this k
        k_.append(k)
        J_.append(J)
        clusters_rec.append(clusters)
        means_rec.append(means_)
        
        if k > 3:
            
            J_diff1 = J_[-2] - J_[-1]
            J_diff2 = J_[-3] - J_[-2]
            
            if J_diff2 - J_diff1 > 8 or k == 12:
                break
        
        k = k + 1

    return k_[-2], clusters_rec[-2], means_rec[-2], k_, J_

# This function finds the euclidean distance between a data point and a mean value
def find_distance_mean(x1, x2, vol):
    
    # x1 is the index of the data point
    # x2 is the calculated mean value
    dist = 0
    for i in range(18):
        dist = dist + (vol[i][x1] - x2[i])**2
    
    return np.sqrt(dist)

# This function finds the mean value from a given cluster
def find_mean(lst_, vol):
    
    n = len(lst_)
    sumup = [0]*18
    
    for i in lst_:
         for j in range(18):
             sumup[j] = sumup[j] + vol[j][i]
    if n == 0:
        mean = sumup
    else:        
        mean = np.divide(sumup, n)
    
    return mean

#This function finds the difference between two mean values
def find_diff(x1, x2):
    
    sumup = 0
    for i in range(18):
        sumup = sumup + (x1[i] - x2[i])**2
        
    diff = np.sqrt(sumup)
    
    return diff