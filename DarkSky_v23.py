#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 13:40:36 2019

@author: nicolasnavarre
"""

import datetime
from datetime import timedelta
import pickle 
from pathlib import Path
import sys
import math
import calendar
#import urllib.parse
#import requests

"""Definitions called"""
from Geo_Coder_function import locate_vineyard
from Weather_Data_Collection_function_vtest1 import weather_data, update_data, weather_lists
from Germination_Model_function_v3 import determine_pis, PMOc_integration, infection_modeling
from Vineyard_Geometry_function_v2 import vineyard_geometry
from Bud_Break_function import bud_break_model
from Erosion_calculation_function_v1 import erosion_calc
from Raster_function_v2 import k_factor_pull, p_factor_pull, ls_factor_pull, Cu_concentration_pull, Bulk_density_pull, Soil_pH_pull, Soil_OC_pull,\
Soil_sand_pull, Soil_clay_pull, Soil_AWC_pull, Soil_hydro_pull, Soil_wcfc_pull, Soil_wcwp_pull
from Soil_transport_function_v3 import soil_transport
from Monthly_calcs_function import monthly_change

#%%
#data_already = input("Do you already have a data file?\n\
#Enter y/n here: ")
import numpy as np
#if data_already == 'y':
#    file_name = input("What is the file name?\n\
#Enter here: ")
#    read_dictionary = np.load(file_name).item()
#    file_in = True
#else:
#    file_in = False

"""Locate the vineyard geocoordinates. This is used to gather the 
meteorological data. See file for further description of function."""
vineyard_location = input("Where is your vineyard's address?\n\
Enter Here: ")

lat, lng, location = locate_vineyard(vineyard_location)

#sys.stdout = open(str(lat)+','+str(lng)+'.txt', 'w')
#%%
""" Determine volume and dose need based on vineyard properties.
See source function for further description of function."""

dose_sprayed, LAI = vineyard_geometry()

#%%
"""Gather the weather data starting on the 1st of every year until
a certain date or update existing data file. 
See source function for further description of function."""

first_day = datetime.datetime(2019, 1, 1, 0)
future_cast = int(input('How many days in the future would you like to forecast?\n\
Enter Here: '))
print('\n')

delta = datetime.datetime.now() + timedelta(days = future_cast) - first_day

weather_file = Path('weather_data'+str(lat)+str(lng)+'.pkl')
print(weather_file)
weather_dict = pickle.load(open('weather_data-'+str(lat)+str(lng)+'.pkl', 'rb'))
#%%
print(len(weather_dict))
updated_dict = update_data (first_day,delta,future_cast,lat,lng, weather_dict)

#%%
combined_dict = {**weather_dict, **updated_dict}
weather_dict = combined_dict
output = open('weather_data-'+str(lat)+str(lng)+'.pkl', 'wb')
pickle.dump(weather_dict, output)

#%%
"""Convert rain, temp, RH, and VPD dictionary pairs to lists
See source function for further description of function."""

rain_list, temp_list, rel_hum_list, vpd_list, Dewpoint, Dewpoint_wet = weather_lists(weather_dict) 


#%%
"""Determine when the bud break is. Infections can not happen before this.
See source function for further description of function."""

do_nothing = False
bud_break_date, do_nothing, DD_dict, SA_dict, WU_dict, LAI_dict = bud_break_model (weather_dict, temp_list)


#%%
"""Determine the initial conditions of each rain event and all parameters needed
See source function for further description of function."""

event_dict, W_dict, DORh, PMOh, HT_dict, HT_list, do_nothing = determine_pis(weather_dict, rain_list, temp_list, vpd_list, Dewpoint_wet)


#%%
"""Determine the relative density of each cohort. (Percentage of entire spore
population that will germinate during this event.) 
See source function for further description of function."""

if do_nothing == False:
    PMOc_dict, total_PMOc = PMOc_integration(event_dict, DORh, HT_dict, do_nothing)


#%%
"""Determine whether or not the cohort will cause an infection.
See source function for further description of function."""

print('Vineyard Location:', location['address'])
y = datetime.datetime.now()
print('Date of simulation:', y.strftime("%B %d, %Y"))
if do_nothing == False:
    spray_dict, app_total, ZDI_dict = infection_modeling(event_dict, weather_dict, W_dict, PMOc_dict, \
                       rain_list, temp_list, rel_hum_list, bud_break_date,\
                       dose_sprayed, dose_sprayed, LAI_dict)

# Save
dictionary = weather_dict
np.save('my_file.npy', dictionary) 

# Load
read_dictionary = np.load('my_file.npy').item()

#%%
dictionary = weather_dict
np.save('weather_data-'+str(lat)+str(lng)+'.npy', dictionary)
read_dictionary = np.load('weather_data-'+str(lat)+str(lng)+'.npy').item()


#%%
try:
    weather_file = weather_file.resolve(strict=True)
except FileNotFoundError: 
    weather_dict = weather_data(first_day, delta, future_cast, lat, lng)
else:
    delta = datetime.datetime.now() - first_day
    weather_dict = pickle.load(open('weather_data00-'+str(lat)+str(lng)+'.pkl', 'rb'))
    #weather_dict = read_dictionary
    updated_dict = update_data (first_day,delta,future_cast,lat,lng, weather_dict)
    combined_dict = {**weather_dict, **updated_dict}
    weather_dict = combined_dict
    
output = open('weather_data-long_term'+str(lat)+str(lng)+'.pkl', 'wb')
pickle.dump(weather_dict, output)

#%%
"""Gather k_factor, p_factor, and LS_factor from EU database files to implement 
into G2 model equation"""
#g2_parameters = defaultdict(list)
print('\nGathering erosion factors for your location. This may take a few minutes.')

k_factor, utm, value = k_factor_pull(lat, lng)
#g2_parameters[lat,lng].append(k_factor)
ls_factor = ls_factor_pull(lat, lng)
p_factor = p_factor_pull(lat, lng)

#%%
try:
    monthly_rain_dict, erosion_monthly_dict = erosion_calc(weather_dict, LAI, lat, lng, location, k_factor, p_factor, ls_factor)
except:
    print('Erosion calculations cannot be performed due to missing data.')
    if isinstance(k_factor, str) == True:
        print ('K_factor data missing.')
    if isinstance(ls_factor, str) == True:
        print ('LS_factor data missing.')
    if isinstance(p_factor, str) == True:
        print ('P_factor data missing.')
        
#%%
cu_conc = Cu_concentration_pull(lat, lng)

#%%
bulk_p = Bulk_density_pull(lat, lng)
soil_om = Soil_OC_pull(lat, lng)
soil_sand = Soil_sand_pull(lat, lng)
soil_pH = Soil_pH_pull(lat, lng)
soil_clay = Soil_clay_pull(lat, lng)
soil_awc = Soil_AWC_pull(lat, lng)
soil_hydro = Soil_hydro_pull(lat, lng)
soil_wcfc = Soil_wcfc_pull(lat, lng)
soil_wcwp = Soil_wcwp_pull(lat, lng)

#%%

#leach_factor = 0.108
#A = 0
monthly_dict, copper_dict = soil_transport(spray_dict, bulk_p, soil_om, soil_sand, soil_pH, soil_clay,\
                   soil_awc, cu_conc, monthly_rain_dict, weather_dict, WU_dict, app_total,\
                   soil_wcfc, soil_wcwp)
                   #erosion_monthly_dict) 
                   #leach_factor, A)

#%%
copper_balance, yearly_drift, yearly_applied, yearly_soil,\
yearly_water, yearly_root, yearly_leach, yearly_erosion\
= monthly_change(copper_dict, bulk_p, app_total, erosion_monthly_dict)


total_applied = sum(yearly_applied)
total_lost = sum(yearly_leach)
total_in_soil = sum(yearly_soil)

print(total_applied)
print(total_in_soil)
print(total_lost)

#%%
sum_pmoc = []
for x in PMOc_dict:
    sum_pmoc.append(PMOc_dict[x][0])

print(sum(sum_pmoc))
#%%
"""
yearly_drift = []
yearly_applied = []
yearly_soil = []
yearly_water = []
yearly_root = []
yearly_leach = []
yearly_erosion = []

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

        delta_leach = delta_applied - delta_soil 
        #copper_dict[month][3]*copper_dict[month][1]*1000*10**4/10**6*((soil_wcfc+soil_wcwp)/2)
        print(round(delta_leach,3), 'kg leach')
        yearly_leach.append(delta_leach)
        
        delta_erosion = erosion_monthly_dict[month][0]*copper_dict[month][0]/1000
        print(round(delta_erosion,3), 'kg erosion\n')
        yearly_erosion.append(delta_erosion)


#%%
mass_balanced = False

for month in copper_balance:
   if len(str(month)) <= 2:
       while mass_balanced == False:
            delta_drift = (sum(app_total[month])*0.16)/1000
            print(round(delta_drift,3), 'kg drift')
            delta_soil = copper_balance[month][0]*bulk_p*1000*0.2*10000/10**6
            print(round(delta_soil,3), 'kg soil')
            delta_water = copper_balance[month][1]*1000*0.2*10000\
            /10**6
            print(round(delta_water,3), 'kg water')
            delta_root = copper_balance[month][2]*1.65*0.2*10000/10**6
            print(round(delta_root,3), 'kg root')
            delta_erosion = erosion_monthly_dict[month][0]*copper_dict[month][0]/1000
            print(round(delta_erosion,3), 'kg erosion')
            delta_leach = copper_dict[month][3]*copper_dict[month][1]*1000*10**4/10**6
            delta_leach = delta_leach
            print(round(delta_leach,3), 'kg leach')
            
            total = delta_soil + delta_water + delta_root
            check = abs(total/delta_leach)
            
            if check > 0.95 and check < 1.05:
                monthly_dose = 0
                monthly_precip = 0 
                monthly_uptake = 0 
                ln_kd = 0.3793*float(soil_pH) + 0.1476*float(soil_om)-1.0417
                kd = math.exp(ln_kd)
                kd_m3 = kd/1000
        

                copper_balance = monthly_change(copper_dict, bulk_p)
                
                delta_drift = (sum(app_total[month])*0.16)/1000
                print(round(delta_drift,3), 'kg drift')
                delta_soil = copper_balance[month][0]*bulk_p*1000*0.2*10000/10**6
                print(round(delta_soil,3), 'kg soil')
                delta_water = copper_balance[month][1]*1000*0.2*10000\
                /10**6
                print(round(delta_water,3), 'kg water')
                delta_root = copper_balance[month][2]*1.65*0.2*10000/10**6
                print(round(delta_root,3), 'kg root')
                delta_erosion = erosion_monthly_dict[month][0]*copper_dict[month][0]/1000
                print(round(delta_erosion,3), 'kg erosion')
                delta_leach = copper_dict[month][3]*copper_dict[month][1]*1000*10**4/10**6
                delta_leach = delta_leach
                print(round(delta_leach,3), 'kg leach')
                
                print(str(round(total*1000,2)),'grams of Cu in the system')
                print(round(delta_leach*1000,3), 'grams lost to leach')
                print(round(delta_erosion*1000,3), 'grams lost to erosion')
                print('\n')
                mass_balanced = True
            else: 
                if check < 1.05:
                    leach_factor = leach_factor * 0.9
                    monthly_dict, copper_dict = soil_transport(spray_dict, bulk_p, soil_om, soil_sand, soil_pH, soil_clay,\
                       soil_awc, cu_conc, monthly_rain_dict, weather_dict, WU_dict, app_total,\
                       soil_wcfc, soil_wcwp, erosion_monthly_dict, leach_factor, A)
                    copper_balance = monthly_change(copper_dict, bulk_p)

                else:
                    leach_factor = leach_factor * 1.1 
                    monthly_dict, copper_dict = soil_transport(spray_dict, bulk_p, soil_om, soil_sand, soil_pH, soil_clay,\
                       soil_awc, cu_conc, monthly_rain_dict, weather_dict, WU_dict, app_total,\
                       soil_wcfc, soil_wcwp, erosion_monthly_dict, leach_factor, A)
                    copper_balance = monthly_change(copper_dict, bulk_p)
"""       

