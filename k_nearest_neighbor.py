#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 13:54:36 2022

@author: Yu-Chieh Hsiao
"""
import numpy as np

# k nearest neighbor
def kNN(label_training, label_testing, training_set, test_set, k):
    
    label_kNN = []
    n_training = len(training_set[0])
    n_test = len(test_set[0])
    
    # For each data point, find the nearest k data point
    for i in range(n_test):
        
        nearest_id = []
        nearest_dist = []
        nearest_dist_sorted = []
        nearest_dist_k = []
        
        # Find the distances between all data points and a single data point
        for j in range(n_training):
            nearest_dist.append(find_distance(j, i, training_set, test_set))
        
        # Having the list of distance, sort it in ascending order
        nearest_dist_sorted = sorted(nearest_dist)
        
        # Extract the k number of closest points
        nearest_dist_k = nearest_dist_sorted[0:k]
        
        # Find the corresponding id of the nearest data points
        for l in range(k):
           nearest_id.append(nearest_dist.index(nearest_dist_k[l]))
        
        # Having obtained the nearest points' ids, determine which class the
        # data point should belong to
        label_kNN.append(determine_label(nearest_id, label_training))
        
    # At last, the accuracy can be calculated using the labels of testing data
    return determine_accuracy(label_testing, label_kNN, test_set)

# This function finds the euclidean distance between two data point based on the
# given databases
def find_distance(train, test, profile_training, profile_test):
    
    dist = 0
    for i in range(18):
        dist = dist + (profile_training[i][train] - profile_test[i][test])**2
        
    return np.sqrt(dist)

# This function determines the class of a given data point containing
# a list of nearest points
def determine_label(lst, label_training):
    
    data_type = [0]*5
    for i in lst:
        data_type[label_training[i]] = data_type[label_training[i]] + 1
    
    data_type_max = data_type.index(max(data_type))
    
    return data_type_max

# This function determines the accuracy for the kNN algorithmn
def determine_accuracy(kNN_label, label, test_set):
    
    n = len(test_set)
    yes = 0
    no = 0
    for i in range(n):
        
        if kNN_label[i] == label[i]:
            yes = yes + 1
        
        else:
            no = no + 1
            
    accuracy = yes/(yes+no)
    
    return accuracy