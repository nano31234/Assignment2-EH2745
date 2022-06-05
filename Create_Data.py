#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 13:50:49 2022

@author: Yu-Chieh Hsiao
"""
import os
import numpy as np
import pandas as pd
import tempfile
import random

import pandapower as pp
from pandapower.timeseries import DFData
from pandapower.timeseries import OutputWriter
from pandapower.timeseries.run_time_series import run_timeseries
from pandapower.control import ConstControl

import matplotlib.pyplot as plt

# This function generates a training data and a testing data for the given
# number of time steps and given state of operation
# x = 1: high load
# x = 2: low load
# x = 3: line disconnection
# x = 4: generator disconnection
def getVoltageProfile(no_time_steps, no_test_time_steps, x):
    
    time_steps = range(0, no_time_steps)
    test_time_steps = range(0, no_test_time_steps)
    network = pp.create_empty_network()
    
    buses = []
    for i in range(9):
        buses.append(pp.create_bus(network, 110))
         
    pp.create_ext_grid(network, buses[0])
    pp.create_line(network, buses[0], buses[3], 10, '149-AL1/24-ST1A 110.0')
    pp.create_line(network, buses[3], buses[4], 10, '149-AL1/24-ST1A 110.0')
    pp.create_line(network, buses[3], buses[8], 10, '149-AL1/24-ST1A 110.0')
    pp.create_line(network, buses[4], buses[5], 10, '149-AL1/24-ST1A 110.0')
    pp.create_line(network, buses[5], buses[2], 10, '149-AL1/24-ST1A 110.0')
    pp.create_line(network, buses[8], buses[7], 10, '149-AL1/24-ST1A 110.0')
    pp.create_line(network, buses[5], buses[6], 10, '149-AL1/24-ST1A 110.0')
    pp.create_line(network, buses[6], buses[7], 10, '149-AL1/24-ST1A 110.0')
    pp.create_line(network, buses[7], buses[1], 10, '149-AL1/24-ST1A 110.0')
    
    pp.create_load(network, buses[4], p_mw=90., q_mvar=30., name='load1')
    pp.create_load(network, buses[6], p_mw=100., q_mvar=35., name='load2')
    pp.create_load(network, buses[8], p_mw=125., q_mvar=50., name='load3')
    
    pp.create_sgen(network, buses[1], p_mw=163, q_mvar=0, name='generator1')
    pp.create_sgen(network, buses[2], p_mw=85, q_mvar=0, name='generator2')
    
    profile = pd.DataFrame()
    test_profile = pd.DataFrame()
    
    if x == 1:
    
        # high load
        profile['load1_p'] = np.random.normal(99, 9, no_time_steps)
        profile['load2_p'] = np.random.normal(110, 10, no_time_steps)
        profile['load3_p'] = np.random.normal(137.5, 12.5, no_time_steps)
        
        # Test set
        test_profile['load1_p'] = np.random.normal(99, 9, no_test_time_steps)
        test_profile['load2_p'] = np.random.normal(110, 10, no_test_time_steps)
        test_profile['load3_p'] = np.random.normal(137.5, 12.5, no_test_time_steps)
        
    elif x == 2:
        # low load state
        profile['load1_p'] = np.random.normal(81, 9, no_time_steps)
        profile['load2_p'] = np.random.normal(90, 10, no_time_steps)
        profile['load3_p'] = np.random.normal(112.5, 12.5, no_time_steps)
    
        # Test set
        test_profile['load1_p'] = np.random.normal(81, 9, no_test_time_steps)
        test_profile['load2_p'] = np.random.normal(90, 10, no_test_time_steps)
        test_profile['load3_p'] = np.random.normal(137.5, 12.5, no_test_time_steps)
        
    elif x == 3:
        # Line Disconnection
        profile['load1_p'] = np.random.normal(90, 4.5, no_time_steps)
        profile['load2_p'] = np.random.normal(100, 5, no_time_steps)
        profile['load3_p'] = np.random.normal(125, 6.25, no_time_steps)
        
        # Test set
        test_profile['load1_p'] = np.random.normal(90, 4.5, no_test_time_steps)
        test_profile['load2_p'] = np.random.normal(100, 5, no_test_time_steps)
        test_profile['load3_p'] = np.random.normal(125, 6.25, no_test_time_steps)
        
        pp.create_switch(network, bus=5, closed=False, element=6, et='l', type='CB')
    
    elif x == 4:
        
        # Generator Disconnection
        profile['load1_p'] = np.random.normal(90, 4.5, no_time_steps)
        profile['load2_p'] = np.random.normal(100, 5, no_time_steps)
        profile['load3_p'] = np.random.normal(125, 6.25, no_time_steps)
        profile['generator1_p'] = [0]*no_time_steps
        
        # Test set
        test_profile['load1_p'] = np.random.normal(90, 4.5, no_test_time_steps)
        test_profile['load2_p'] = np.random.normal(100, 5, no_test_time_steps)
        test_profile['load3_p'] = np.random.normal(125, 6.25, no_test_time_steps)
        test_profile['generator1_p'] = [0]*no_test_time_steps
        
    
    dataSource_test = DFData(test_profile)
    dataSource = DFData(profile)
    
    ConstControl(network, element='load', variable='p_mw', element_index=[0],
                     data_source=dataSource, profile_name=["load1_p"])
    ConstControl(network, element='load', variable='p_mw', element_index=[1],
                     data_source=dataSource, profile_name=["load2_p"])
    ConstControl(network, element='load', variable='p_mw', element_index=[2],
                     data_source=dataSource, profile_name=["load3_p"])
    
    if x == 4:
        # Generator Disconnection
        ConstControl(network, element='sgen', variable='p_mw', element_index=[0],
                         data_source=dataSource, profile_name=["generator1_p"])

    output_dir = os.path.join(tempfile.gettempdir(), "time_series_example")
    print("Results can be found in your local temp folder: {}".format(output_dir))
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    
    ow = OutputWriter(network, time_steps, output_path=output_dir, output_file_type=".xls", log_variables=list())
    # these variables are saved to the harddisk after / during the time series loop
    ow.log_variable('res_load', 'p_mw')
    ow.log_variable('res_bus', 'vm_pu')
    ow.log_variable('res_bus', 'va_degree')
    ow.log_variable('res_line', 'loading_percent')
    ow.log_variable('res_line', 'i_ka')
    
    pp.set_user_pf_options(network, calculate_voltage_angles=True)
    run_timeseries(network, time_steps)
    
    # Voltage magnitude
    vm_pu_file = os.path.join(output_dir, "res_bus", "vm_pu.xls")
    vm_pu_tot = pd.read_excel(vm_pu_file)
    vm_pu = vm_pu_tot[[0,1,2,3,4,5,6,7,8]]
    vm_pu.plot(label="vm_pu")
    plt.xlabel("time step")
    plt.ylabel("voltage mag. [p.u.]")
    plt.title("Voltage Magnitude")
    plt.grid()
    plt.show()
    
    # Voltage angle
    va_degree_file = os.path.join(output_dir, "res_bus", "va_degree.xls")
    va_degree_tot = pd.read_excel(va_degree_file)
    va_degree = va_degree_tot[[0,1,2,3,4,5,6,7,8]]
    va_degree.plot(label="va_degree")
    plt.xlabel("time step")
    plt.ylabel("voltage angle. [degree]")
    plt.title("Voltage Angle")
    plt.grid()
    plt.show()
    
    # generate training data
    # Get the voltage magnitude and angle from the data frame
    voltage_mag = []
    voltage_deg = []
    
    for i in range(9):
        temp_mag = []
        temp_deg = []
        for j in range(no_time_steps):
            temp_mag.append(vm_pu_tot[i][j])
            temp_deg.append(va_degree_tot[i][j])
        
        voltage_mag.append(temp_mag)
        voltage_deg.append(temp_deg)
    
    # Normalize voltage angle
    minimum = 0
    maximum = 0
    
    for i in range(9):
        
        if i == 0:
            continue
        
        minimum = np.amax(voltage_deg[i])
        maximum = np.amin(voltage_deg[i])
        
        voltage_deg[i] = (voltage_deg[i] - minimum)/(maximum - minimum)
    
    voltage_profile_temp = voltage_mag + voltage_deg
    voltage_profile = np.empty(shape=(19,no_time_steps))
    for i in range(18):
        for j in range(no_time_steps):
            voltage_profile[i][j] = voltage_profile_temp[i][j]
    
    for i in range(no_time_steps):
        voltage_profile[-1][i] = x
    
    # Generate testing data
    # Generate test system and get the corresponding voltage profile

    ConstControl(network, element='load', variable='p_mw', element_index=[0],
                     data_source=dataSource_test, profile_name=["load1_p"])
    ConstControl(network, element='load', variable='p_mw', element_index=[1],
                     data_source=dataSource_test, profile_name=["load2_p"])
    ConstControl(network, element='load', variable='p_mw', element_index=[2],
                     data_source=dataSource_test, profile_name=["load3_p"])
    
    if x == 4:
        # Generator Disconnection
        ConstControl(network, element='sgen', variable='p_mw', element_index=[0],
                         data_source=dataSource_test, profile_name=["generator1_p"])
    
    output_dir_test = os.path.join(tempfile.gettempdir(), "time_series_test")
    if not os.path.exists(output_dir_test):
        os.mkdir(output_dir_test)
    ow_test = OutputWriter(network, test_time_steps, output_path=output_dir_test, output_file_type=".xls", log_variables=list())
    print("Results can be found in your local temp folder: {}".format(output_dir_test))
    
    # these variables are saved to the harddisk after / during the time series loop
    ow_test.log_variable('res_bus', 'vm_pu')
    ow_test.log_variable('res_bus', 'va_degree')
    pp.set_user_pf_options(network, calculate_voltage_angles=True)
    run_timeseries(network, test_time_steps)
    
    # Voltage magnitude
    vm_pu_file_test = os.path.join(output_dir, "res_bus", "vm_pu.xls")
    vm_pu_tot_test = pd.read_excel(vm_pu_file_test)
    vm_pu_test = vm_pu_tot_test[[0,1,2,3,4,5,6,7,8]]
    
    # Voltage angle
    va_degree_file_test = os.path.join(output_dir, "res_bus", "va_degree.xls")
    va_degree_tot_test = pd.read_excel(va_degree_file_test)
    va_degree_test = va_degree_tot_test[[0,1,2,3,4,5,6,7,8]]
    
    # Get the voltage magnitude and angle from the data frame
    voltage_mag_test = []
    voltage_deg_test = []
    
    for i in range(9):
        temp_mag = []
        temp_deg = []
        for j in range(no_test_time_steps):
            temp_mag.append(vm_pu_tot_test[i][j])
            temp_deg.append(va_degree_tot_test[i][j])
        
        voltage_mag_test.append(temp_mag)
        voltage_deg_test.append(temp_deg)
        
    # Normalize voltage angle
    minimum = 0
    maximum = 0
    
    for i in range(9):
        
        if i == 0:
            continue
        
        minimum = np.amax(voltage_deg_test[i])
        maximum = np.amin(voltage_deg_test[i])
        
        voltage_deg_test[i] = (voltage_deg_test[i] - minimum)/(maximum - minimum)    
    
    voltage_profile_temp = voltage_mag_test + voltage_deg_test
    voltage_profile_test = np.empty(shape=(19, no_test_time_steps))
    for i in range(18):
        for j in range(no_test_time_steps):
            voltage_profile_test[i][j] = voltage_profile_temp[i][j]
    
    for i in range(no_test_time_steps):
        voltage_profile_test[-1][i] = x
    
    return voltage_profile, voltage_profile_test