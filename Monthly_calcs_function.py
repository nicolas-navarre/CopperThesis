#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 11:24:44 2019

@author: nicolasnavarre
"""
from collections import defaultdict
import calendar

def monthly_change(copper_dict, bulk_p, app_total, erosion_monthly_dict):

    copper_balance = defaultdict(list)
    copper_balance['month #'].append('delta ct_Cu_tot mg/kg')
    copper_balance['month #'].append('delta [Cu]tot mg/L')
    copper_balance['month #'].append('delta Cu_bio mg/kg')
                
    second_run = True               
    
    yearly_drift = []
    yearly_applied = []
    yearly_soil = []
    yearly_water = []
    yearly_root = []
    yearly_leach = []
    yearly_erosion = []
    
    for month in copper_dict:
        if str(month) == 'initial':
            temp_soil = copper_dict[month][0]
            temp_water = copper_dict[month][1]
            temp_root = copper_dict[month][2]
            first_run = True
            continue
        
        if len(str(month)) <= 2 or str(month) == 'initial': 
            if second_run == False:
                second_run = True
            
            if first_run == True: 
                
                soil_change = copper_dict[month][0] - temp_soil
                copper_balance[month].append(round(soil_change,3))
                
                water_change = copper_dict[month][1] - temp_water
                copper_balance[month].append(round(water_change,3))
                
                root_change = copper_dict[month][2] - temp_root
                copper_balance[month].append(round(root_change,3))
                second_run = False
                first_run = False
            
            if second_run == True: 
                
                soil_change = copper_dict[month][0] - copper_dict[month-1][0]
                copper_balance[month].append(round(soil_change,3))

                water_change = copper_dict[month][1] - copper_dict[month-1][1]
                copper_balance[month].append(round(water_change,3))
            
                root_change = copper_dict[month][2] - copper_dict[month-1][2]
                copper_balance[month].append(round(root_change,3))
    
    for month in copper_balance:
        if len(str(month)) <= 2:
            print(calendar.month_name[month])
            
            delta_drift = (sum(app_total[month])*0.16)/1000
            print(round(delta_drift,3), 'kg drift')
            yearly_drift.append(delta_drift)
            
            delta_applied = (sum(app_total[month])*0.84)/1000
            print(round(delta_applied,3), 'kg entering soil system')
            yearly_applied.append(delta_applied)
            
            delta_soil = copper_balance[month][0]*bulk_p*1000*0.2*10000/10**6
            print(round(delta_soil,3), 'kg soil')
            yearly_soil.append(delta_soil)
            
            delta_water = copper_balance[month][1]*1000*0.2*10000/10**6
            print(round(delta_water,3), 'kg water')
            yearly_water.append(delta_water)
            
            delta_root = copper_balance[month][2]*1.65*0.2*10000/10**6
            print(round(delta_root,3), 'kg root')
            yearly_root.append(delta_root)
    
            delta_leach = delta_applied - delta_soil - delta_root
            #copper_dict[month][3]*copper_dict[month][1]*1000*10**4/10**6*((soil_wcfc+soil_wcwp)/2)
            print(round(delta_leach,3), 'kg leach')
            yearly_leach.append(delta_leach)
            
            delta_erosion = erosion_monthly_dict[month][0]*copper_dict[month][0]/1000
            print(round(delta_erosion,3), 'kg erosion\n')
            yearly_erosion.append(delta_erosion)
    
    
    return copper_balance, yearly_drift, yearly_applied, yearly_soil,\
yearly_water, yearly_root, yearly_leach, yearly_erosion

