#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 14:25:06 2019

@author: nicolasnavarre
"""

#Erosion Calcs

#Need monthly list of rain amount and time. 
from collections import defaultdict

import math
import calendar

def erosion_calc(weather_dict, LAI, lat, lng, location, k_factor, p_factor, ls_factor):

    monthly_rain_dict = defaultdict(list)
    erosion_monthly_dict = defaultdict(list)
    total_month_rain = defaultdict(list)
    monthly_rain = 0
    total_rain = 0
    count = 1 
    LU_vineyard = 7
    for rain in weather_dict:
        rain = int(rain)
        if weather_dict[rain][0] != 'No Data':
            if rain > 1: 
                if weather_dict[rain][6] == weather_dict[rain-1][6]:
                    total_rain += weather_dict[rain][0]
                    if weather_dict[rain][0] != 0:   
                        monthly_rain += weather_dict[rain][0]
                        count += 1 
                    if monthly_rain < 10 and weather_dict[rain][0] == 0:
                        monthly_rain = 0
                        count = 1 
                else:
                    total_month_rain[int(weather_dict[rain-1][6])].append(total_rain)
                    if monthly_rain > 10:
                        monthly_rain_dict[weather_dict[rain-1][6]].append(monthly_rain)
                        monthly_rain_dict[weather_dict[rain-1][6]].append(count)
                        monthly_rain_dict[weather_dict[rain-1][6]].append(monthly_rain/count)
                    else:
                        monthly_rain_dict[weather_dict[rain-1][6]].append(0)
                        monthly_rain_dict[weather_dict[rain-1][6]].append(0)
                        monthly_rain_dict[weather_dict[rain-1][6]].append(0)
                    monthly_rain = weather_dict[rain][0]
                    total_rain = weather_dict[rain][0]
                    count = 1    
                    
                if rain == len(weather_dict)-1:
                    total_month_rain[int(weather_dict[rain-1][6])].append(total_rain)
                    monthly_rain_dict[weather_dict[rain-1][6]].append(monthly_rain)
                    monthly_rain_dict[weather_dict[rain-1][6]].append(count)
                    monthly_rain_dict[weather_dict[rain-1][6]].append(monthly_rain/count)

    v_factor = math.exp(LU_vineyard*(1-math.exp(-0.431*LAI)))

    for r_factor in monthly_rain_dict:
        if monthly_rain_dict[r_factor][0]!= 0:
            erosion = ((524+222*math.log10(monthly_rain_dict[r_factor][2]))/v_factor)*k_factor*(ls_factor/p_factor)
            erosion_monthly_dict[int(r_factor)].append(round(erosion,4))
        else:
            erosion_monthly_dict[int(r_factor)].append(0)
    if len(erosion_monthly_dict) == 0:
        print('No expected water erosion at this time.')
    else:
        for key in erosion_monthly_dict:
            month = int(key)
            monthly_loss = round(erosion_monthly_dict[key][0]*1000,4)
         
            print(calendar.month_name[month]+':', str(monthly_loss)+' kg/ha soil eroded.')
    
    return monthly_rain_dict, erosion_monthly_dict, total_month_rain