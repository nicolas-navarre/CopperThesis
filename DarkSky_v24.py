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
from Weather_Data_Collection_function_vtest import weather_data, update_data, weather_lists
from Germination_Model_function_v3 import determine_pis, PMOc_integration, infection_modeling
from Vineyard_Geometry_function_v2 import vineyard_geometry
from Bud_Break_function import bud_break_model
from Erosion_calculation_function_v1 import erosion_calc
from Raster_function_v2 import k_factor_pull, p_factor_pull, ls_factor_pull, Cu_concentration_pull, Bulk_density_pull, Soil_pH_pull, Soil_OC_pull,\
Soil_sand_pull, Soil_clay_pull, Soil_AWC_pull, Soil_hydro_pull, Soil_wcfc_pull, Soil_wcwp_pull
from Soil_transport_function_v3 import soil_transport
from Monthly_calcs_function import monthly_change
from weather_data_2017_v3 import weather_data_2017_v3

#%%
data_already = input("Do you already have a data file?\n\
Enter y/n here: ")
import numpy as np
if data_already == 'y':
    file_name = input("What is the file name?\n\
                      Enter here: ")
    read_dictionary = np.load(file_name)
    file_in = True
    weather_dict_2018_v2 = read_dictionary
else:
    file_in = False

"""Locate the vineyard geocoordinates. This is used to gather the 
meteorological data. See file for further description of function."""
#%%
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
#file_in = False
if file_in == False:
    first_day = datetime.datetime(2009,1, 1, 0)
    future_cast = int(input('How many days in the future would you like to forecast?\n\
    Enter Here: '))
    print('\n')
    
    delta = datetime.datetime.now() + timedelta(days = future_cast) - first_day
    
    weather_file_it_2011 = Path('weather_data-it-2011'+str(lat)+str(lng)+'.pkl')
    weather_dict_it_2011 = weather_data_2017_v3(first_day, delta, future_cast, lat, lng)
    """
    try:
        weather_file = weather_file.resolve(strict=True)
    except FileNotFoundError: 
        weather_dict = weather_data(first_day, delta, future_cast, lat, lng)
    else:
        delta = datetime.datetime.now() - first_day
        weather_dict = pickle.load(open('weather_data-'+str(lat)+str(lng)+'.pkl', 'rb'))
        #weather_dict = read_dictionary
        updated_dict = update_data (first_day,delta,future_cast,lat,lng, weather_dict)
        combined_dict = {**weather_dict, **updated_dict}
        weather_dict = combined_dict
    """
output = open('weather_data-it-2011'+str(lat)+str(lng)+'.pkl', 'wb')
pickle.dump(weather_dict_it_2011, output)

#%%
"""Convert rain, temp, RH, and VPD dictionary pairs to lists
See source function for further description of function."""

weather_dict = weather_dict_2011_v2
import numpy as np
# Save
dictionary = weather_dict
#np.save('weather_dict_2018_Guignard.npy', dictionary) 


rain_list, temp_list, rel_hum_list, vpd_list, Dewpoint, Dewpoint_wet = weather_lists(weather_dict) 
count = 0
tempe_list = []
for tempe in temp_list:
    if count > 1776:
        tempe_list.append(tempe)
    count = count + 1 
    if count == 5447:
        break
print(sum(tempe_list)/len(tempe_list))


"""Determine when the bud break is. Infections can not happen before this.
See source function for further description of function."""

do_nothing = False
bud_break_date, do_nothing, DD_dict, SA_dict, WU_dict, LAI_dict = bud_break_model (weather_dict, temp_list)

LAI_list = []
for LAI_area in LAI_dict:
    print(LAI_area)
    print(LAI_dict[LAI_area][0])
    LAI_list.append(LAI_dict[LAI_area][0])
    if LAI_area == '2009-08-15 23:00:00':
        break
    
LAI_total = sum(LAI_list)/len(LAI_list)
print(LAI_total)
    


"""Determine the initial conditions of each rain event and all parameters needed
See source function for further description of function."""

event_dict, W_dict, DORh, PMOh, HT_dict, HT_list, do_nothing = determine_pis(weather_dict, rain_list, temp_list, vpd_list, Dewpoint_wet)

#%%

"""Determine the relative density of each cohort. (Percentage of entire spore
population that will germinate during this event.) 
See source function for further description of function."""

if do_nothing == False:
    PMOc_dict, total_PMOc = PMOc_integration(event_dict, DORh, HT_dict, do_nothing)



"""Determine whether or not the cohort will cause an infection.
See source function for further description of function."""

print('Vineyard Location:', location['address'])
y = datetime.datetime.now()
print('Date of simulation:', y.strftime("%B %d, %Y"))

if do_nothing == False:

    
    spray_dict, app_total, ZDI_dict, infect_dict, r_list = infection_modeling(event_dict, weather_dict, W_dict, PMOc_dict, \
                       rain_list, temp_list, rel_hum_list, bud_break_date,\
                       dose_sprayed, dose_sprayed, LAI_dict)

#import numpy as np
# Save
#dictionary = weather_dict
#np.save('weather_dict_2017.npy', dictionary) 

# Load
#read_dictionary = np.load('weather_dict_2017.npy').item()

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
    monthly_rain_dict, erosion_monthly_dict, total_month_rain = erosion_calc(weather_dict, LAI, lat, lng, location, k_factor, p_factor, ls_factor)
except:
    print('Erosion calculations cannot be performed due to missing data.')
    if isinstance(k_factor, str) == True:
        print ('K_factor data missing.')
    if isinstance(ls_factor, str) == True:
        print ('LS_factor data missing.')
    if isinstance(p_factor, str) == True:
        print ('P_factor data missing.')
        
#for month in total_month_rain:
#    app_total[month].append(0)
        
#%%
#cu_conc = Cu_concentration_pull(lat, lng)
cu_conc = 26.58

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
soil_pH = 3.84*1.1
#leach_factor = 0.108
#A = 0
from collections import defaultdict

app_total_reg = defaultdict(list)
app_total_reg[1].append(0)
app_total_reg[2].append(0)
app_total_reg[3].append(0)
app_total_reg[4].append(1400)
app_total_reg[5].append(1400)
app_total_reg[6].append(3000)
app_total_reg[7].append(4000)
app_total_reg[8].append(1600)
app_total_reg[9].append(0)
app_total_reg[10].append(0)
app_total_reg[11].append(0)
app_total_reg[12].append(0)
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
total_root = sum(yearly_root)


print(total_applied)
print(total_in_soil)
print(total_lost)
print(total_root)

#%%
yearly_rain = []
yearly_temp = []
temp_count = 0 
for monthly_rain in total_month_rain:
    if 3 < monthly_rain < 9: 
        yearly_rain.append(total_month_rain[monthly_rain][0])
print(sum(yearly_rain))

#%%
budbreak_date = ['2016-04-14', '2016-04-18',\
        '2016-04-03', '2016-04-05',\
        '2016-04-15', '2016-03-24',\
        '2016-04-12', '2016-03-30',\
        '2016-03-29', '2016-04-03']
        
mean = (np.array(budbreak_date, dtype='datetime64[s]')
        .view('i8')
        .mean()
        .astype('datetime64[s]'))

print(mean)
#%%
max_LAI = ['2016-06-19', '2016-06-26',\
        '2016-06-06', '2016-06-22',\
        '2016-07-07', '2016-06-19',\
        '2016-06-16', '2016-06-30',\
        '2016-06-14', '2016-06-18']

print(datetime.datetime(2016,6,18)-datetime.datetime(2016,4,3))
        







#%%
for temp_calc in weather_dict:
    if weather_dict[temp_calc][7] > datetime.datetime(2009, 1, 1, 0) and weather_dict[temp_calc][7] < datetime.datetime(2009, 5, 1, 0):
        #print(weather_dict[temp_calc][7])
        yearly_temp.append(float(weather_dict[temp_calc][1]))
        temp_count += 1
    
print(sum(yearly_temp)/temp_count)

#%%
import matplotlib.pyplot as plt
pmoc_list = []
for bla in PMOc_dict:
    pmoc_list.append(PMOc_dict[bla][0])
plt.plot(pmoc_list)


#%%
infect_list = []
first_run = True
count_germ = 0
count_infect = 0 

date_list = []
app_list = []
for x in weather_dict:
    date_list.append(weather_dict[x][7])
    
for x in ZDI_dict:
    if first_run == True:
        for i in range(0,x):
            infect_list.append(0)
        first_run = False
    if len(ZDI_dict[x]) > 0 and len(ZDI_dict[x]) < 2:
        infect_list.append(0.5)
        count_germ += 1
    
    if len(ZDI_dict[x]) > 1:
        infect_list.append(1)
        count_infect += 1
    else:
        infect_list.append(0)

plt.plot(date_list)
print(count_germ, count_infect)
ratio = count_infect/count_germ
print(round(ratio*100,2))
print(62/71, 9/71)

LAI_list = []
for x in LAI_dict:
    LAI_list.append(LAI_dict[x][0])
    app_list.append(LAI_dict[x][1])
    
#plt.plot(LAI_list)   

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

