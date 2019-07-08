#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 14:59:33 2019

@author: nicolasnavarre
"""


from collections import defaultdict
import datetime
import math
import numpy


def bud_break_model (test_dict, T):
    DD_dict = defaultdict(list)
    SA_dict = defaultdict(list)
    WU_dict = defaultdict(list)
    LAI_dict = defaultdict(list)
    Budbreaking_dict = {'Cabernet Sauvignon': 318.6, 'Chasselas': 257.8, 'Chardonnay': 60,
                       'Grenache': 321.3, 'Merlot': 265.3, 'Pinot Noir': 258.4, 
                       'Riesling': 257.7, 'Sauvignon': 294.4, 'Syrah': 265.3, 'Ugni Blanc': 284.7}
    
    """  winetype = input('What type of grape species are you growing?\n\
    You can choose from:\n\
    Cabernet Sauvignon\n\
    Chasselas\n\
    Chardonnay\n\
    Grenache\n\
    Merlot\n\
    Pinot Noir\n\
    Riesling\n\
    Sauvignon\n\
    Syrah\n\
    Ugni Blanc\n\n\
    Enter Variety: ')"""
    winetype = 'Syrah'
    T_daily_avg = defaultdict (list)
    for j in test_dict:
        try: 
            if test_dict[j][4] == '23' or test_dict[j][4] == 23:
                T_daily_avg[test_dict[j][7]].append(round(sum(T[j-23:j])/24,2))
                    
        except (ValueError, IndexError):
            if j>1 and (test_dict[j][7] != test_dict[j-1][7]) and test_dict[j-1][4] == 'No Data':
                print(test_dict[j][7], 'data not available.') 
    
    wine_gc = Budbreaking_dict[winetype]
    Gc = 0 
    To = 5
    
    for bud_burst in T_daily_avg:
       
        if T_daily_avg[bud_burst][0] > To: 
            Gc = Gc + T_daily_avg[bud_burst][0] - To 
        else:
            Gc = Gc
    
        if Gc >= wine_gc:
            print('Bud burst is expected around:', bud_burst.strftime('%h-%d'))
            bud_break_date = bud_burst
            do_nothing = False
            break
    DD = 0
    SA = 0
    for bud_burst in T_daily_avg:
        DD = DD 
        SA = SA
        temp = T_daily_avg[bud_burst][0] - 10
        if temp > 0:
            DD = DD 
            SA = SA
            if datetime.datetime(2019,3,15) <= bud_burst:
                DD = DD + T_daily_avg[bud_burst][0] - 10
                SA = -2.6 + 6.63*(1-math.exp(-0.0042*DD))
                #print(SA)
                if SA < 0:
                    SA = 0
                DD_dict[bud_burst].append(DD)
                SA_dict[bud_burst].append(SA) 
            else:
                DD_dict[bud_burst].append(DD)
                SA_dict[bud_burst].append(SA)
        else: 
            DD_dict[bud_burst].append(DD)
            SA_dict[bud_burst].append(SA)
        water_use = -0.281+0.112*(SA/7.55)*100
        #print(water_use)
        if water_use > 0:
            water_use_ha = (water_use/7.55*30)
            WU_dict[bud_burst].append(water_use_ha)
            WU_dict[bud_burst].append(int(bud_burst.strftime('%m')))
        else:
            WU_dict[bud_burst].append(0)
            WU_dict[bud_burst].append(int(bud_burst.strftime('%m')))
        if SA_dict[bud_burst][0] > 0:
            #LAI = (0.0309/0.235)*((SA_dict[bud_burst][0]-0.552)/0.134)
            #print(LAI)
            LAI = (water_use-0/.369)/1.587
            if LAI >= 2.5:
                LAI = 2.5
            #print(LAI)
            if LAI > 0: 
                LAI_dict[str(bud_burst)].append(LAI)
            
                depo_1 = -2.6422*numpy.log(LAI)+3.947
                depo_2 = 0.2269*(LAI)**-0.5187
                
                adj_1 = 0.5/depo_1
                adj_2 = 0.5/depo_2
                
                app_rate_1 = 2*10**2*depo_1*LAI/0.46
                app_rate_2 = 2*10**2*depo_2*LAI/0.46
                
                adj_rate_1 = app_rate_1*adj_1
                adj_rate_2 = app_rate_2*adj_2
                
                if adj_rate_1 >= adj_rate_2:
                    final_rec = int(1.3*round(adj_rate_1))
                    final_rec = int(math.ceil(final_rec / 50.0)) * 50
                    LAI_dict[str(bud_burst)].append(final_rec)
                    LAI_dict[str(bud_burst)].append(bud_burst.strftime('%H-%d'))

                else:
                    final_rec = int(1.3*round(adj_rate_2))
                    final_rec = int(math.ceil(final_rec / 50.0)) * 50
                    LAI_dict[str(bud_burst)].append(final_rec)
                    LAI_dict[str(bud_burst)].append(bud_burst.strftime('%H-%d'))
            else:
                LAI_dict[str(bud_burst)].append(0)
                LAI_dict[str(bud_burst)].append(50)
                LAI_dict[str(bud_burst)].append(bud_burst.strftime('%H-%d'))
            
        else:
            LAI_dict[str(bud_burst)].append(0)
            LAI_dict[str(bud_burst)].append(50)
            LAI_dict[str(bud_burst)].append(bud_burst.strftime('%H-%d'))
    
    #Factor of safety of -14 is used to account for the RMSE of the values provided. 
    if Gc < wine_gc - 14:
        print('Buds are not expected to burst within the next 14 days. You are not at risk of infection.')
        bud_break_date = 'No Date'
        do_nothing = True
    
    return bud_break_date, do_nothing, DD_dict, SA_dict, WU_dict, LAI_dict
        