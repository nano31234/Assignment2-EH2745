#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 28 01:28:17 2022

@author: Yu-Chieh Hsiao
"""
import numpy as np

import Create_Data
import kmeans
import k_nearest_neighbor
import matplotlib.pyplot as plt

# Generate the training and testing data of the 4 operating states
v1, vt1 = Create_Data.getVoltageProfile(70, 20, 1)  
v2, vt2 = Create_Data.getVoltageProfile(70, 20, 2)
v3, vt3 = Create_Data.getVoltageProfile(70, 20, 3)
v4, vt4 = Create_Data.getVoltageProfile(70, 20, 4)

# Combine the operating states into a single training or testing dataset
voltage_training = np.concatenate((v1, v2, v3, v4), axis=1)
label_training = voltage_training[-1][:]
label_training = label_training.astype(int)

voltage_testing = np.concatenate((vt1, vt2, vt3, vt4), axis=1)
label_testing = voltage_testing[-1][:]
label_testing = label_testing.astype(int)

# Plot the generated voltage profile

for i in range(len(voltage_training[0])):
    
    y = []
    x = []
    
    y = voltage_training[0:8, i]
    x = voltage_training[9:17, i]
    
    if voltage_training[-1, i] == 1:
        plt.scatter(x, y, s=5, c='blue')
        
    elif voltage_training[-1, i] == 2:
        plt.scatter(x, y, s=5, c='black')
        
    elif voltage_training[-1, i] == 3:
        plt.scatter(x, y, s=5, c='red')
        
    elif voltage_training[-1, i] == 4:
        plt.scatter(x, y, s=5, c='green')    
    
plt.xlabel('Normalized Voltage Angle')
plt.ylabel('Voltage Magnitude (p.u.)')
plt.show()
        

# Perform the k means clustering using the datasets created by getVoltageProfile
kmeans_result = [None, None, None, None, None]
kmeans_result = kmeans.kmeans_clustering(voltage_training)
kmenas_k = kmeans_result[0]
kmeans_clusters = kmeans_result[1]
kmeans_centroids = kmeans_result[2]

# Label the results of k-means
label_kmeans = [0 for x in range(len(voltage_training[0]))]

for i in range(len(voltage_training[0])):
    for index, cluster in enumerate(kmeans_clusters):
        if i in cluster:
            label_kmeans[i] = index
            break

# Perform the kNN algorithmn using the datatype label created by getVoltageProfile
kNN_results = []

for i in range(7):
    
    kNN_results.append(k_nearest_neighbor.kNN(label_training, label_testing, voltage_training, voltage_testing, 2*i + 1))



