#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 13:49:02 2019

@author: nicolasnavarre
"""
import numpy 
import math

def vineyard_geometry():
    height = float(input('What is the average height of your vines?\
 Measure at least 5 to get an averages.\n\
Enter average height (m): '))
    
    width = float(input('What is the average width of your vines?\
 Measure at least 5 to get an averages.\n\
Enter average width (m): '))
    
    row_distance = float(input('What is the average row distance of your vineyard?\n\
Enter average row distance (m): '))
    
    adj_rate_list = []
    VRV = (height*width*10000)/row_distance
    app_eff = 0.66
    
    leaf_area_index_1 = ((1*10**(-5))*VRV**1.3977)
    leaf_area_index_2 = 3.5*10**(-5)*VRV**1.25
    
    exp_depo_1 = -2.6422*numpy.log(leaf_area_index_1)+3.947
    exp_depo_2 = -2.6422*numpy.log(leaf_area_index_2)+3.947
    exp_depo_3 = 0.2269*(leaf_area_index_1)**-0.5187
    exp_depo_4 = 0.2269*(leaf_area_index_2)**-0.5187
    
    adj_factor_1 = 0.5/exp_depo_1
    adj_factor_2 = 0.5/exp_depo_2
    adj_factor_3 = 0.5/exp_depo_3
    adj_factor_4 = 0.5/exp_depo_4
    

    app_rate_1 = 2*10**2*exp_depo_1*leaf_area_index_1/app_eff
    app_rate_2 = 2*10**2*exp_depo_2*leaf_area_index_2/app_eff
    app_rate_3 = 2*10**2*exp_depo_3*leaf_area_index_1/app_eff
    app_rate_4 = 2*10**2*exp_depo_4*leaf_area_index_2/app_eff
    
    adj_rate_1 = app_rate_1*adj_factor_1
    adj_rate_2 = app_rate_2*adj_factor_2
    adj_rate_3 = app_rate_3*adj_factor_3
    adj_rate_4 = app_rate_4*adj_factor_4
    
    adj_rate_list.append(adj_rate_1)
    adj_rate_list.append(adj_rate_2)
    adj_rate_list.append(adj_rate_3)
    adj_rate_list.append(adj_rate_4)
    
    if adj_rate_list[0] == max(adj_rate_list):
        print('\nEstimated LAI (1 = 10,000 m2/ha) =', round(leaf_area_index_1,2))
        print('Estimated average deposit on leaves and bunches (ng/cm2)/(g a.i./ha) =', round(exp_depo_1,2))
        final_rec = int(1.3*round(max(adj_rate_list)))
        final_rec = int(math.ceil(final_rec / 50.0)) * 50
        print('Recommended spay dose (g/ha) =', final_rec)
        LAI = leaf_area_index_1
        
    if adj_rate_list[1] == max(adj_rate_list):
        print('\nEstimated LAI (1 = 10,000 m2/ha) =', round(leaf_area_index_2,2))
        print('Estimated average deposit on leaves and bunches (ng/cm2)/(g a.i./ha) =', round(exp_depo_2,2))
        final_rec = int(1.3*round(max(adj_rate_list)))
        final_rec = int(math.ceil(final_rec / 50.0)) * 50
        print('Recommended spay dose (g/ha) =', final_rec)
        LAI = leaf_area_index_2
        
    if adj_rate_list[2] == max(adj_rate_list):
        print('\nEstimated LAI (1 = 10,000 m2/ha) =', round(leaf_area_index_1,2))
        print('Estimated average deposit on leaves and bunches (ng/cm2)/(g a.i./ha) =', round(exp_depo_3,2))
        final_rec = int(1.3*round(max(adj_rate_list)))
        final_rec = int(math.ceil(final_rec / 50.0)) * 50
        print('Recommended spay dose (g/ha) =', final_rec)
        LAI = leaf_area_index_1
        
    if adj_rate_list[3] == max(adj_rate_list):
        print('\nEstimated LAI (1 = 10,000 m2/ha) =', round(leaf_area_index_2,2))
        print('Estimated average deposit on leaves and bunches (ng/cm2)/(g a.i./ha) =', round(exp_depo_4,2))
        final_rec = int(1.3*round(max(adj_rate_list)))
        final_rec = int(math.ceil(final_rec / 50.0)) * 50
        print('Recommended spay dose (g/ha) =', final_rec)
        LAI = leaf_area_index_1
    

    return final_rec, LAI