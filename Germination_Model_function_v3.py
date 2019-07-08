#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 13:13:44 2019

@author: nicolasnavarre
"""

"""This function calculates the Hydrothermal time of the plants. It also builds a 
dictionary of every event happening in the PIS (Primary Inoculum Season). The PIS
starts when the hydrothermal time (a function of temperature and wet days) of the site 
is greater than 1.3 and ends when it is 8.6. These limits are usesd because 97% of the 
spore population will germinate within this time frame. This helps significantly reduce 
computing power as the final 3% are spread over the remainder of the year. 
 
An event occurs when ranfaill is greater than 0.2mm during the PIS and ends
when rainfall is less than 0.2mm. A dictionary is used to build track the 
event number as a key, and the beginning and ending hours are stored as values 
of that key.

The DORh is the progress of dormancy breaking in the oospores population 
at hour h.

PMOh is the physiologically mature oospores (going from MMO to PMO. This is 
regulated by DORh"""

import math
import datetime
from collections import defaultdict

def determine_pis(test_dict, R, T, VPD, Dewpoint_wet):
    
    hour_now = len(test_dict)   #Current hour of year. 
    J = []      #Number of events triggering germination. 
    DORh = []   #List of DOR at each hour of the year
    PMOh = []   #List of PMO at each hour of the year
    HTh = []    #List of HT at each hour of the year
    HT = 0      #Hydro-thermal time. Used for quantifying 
                #germination response to temperature and water potentia in hours

    count = 1       #Count of triggering events
    event = 0       #Check to whether this is the first event hour
    check = False   #Boolean to regulate count
    do_nothing = False

    event_dict = defaultdict(list)  #This dictionary stores the event number (J) as a key
                                    #and stores the starting and ending hour as values
    W_dict = defaultdict(list)      #Dictionary which stores weather an hour was wet or not.
                                    #Wet is classified as more than 0.2mm of rain in an hour.
                                    #This is a dichotomic value (0) Dry (1) Wet
    HT_dict = defaultdict(list)
    for hour in range (0, hour_now):
        
        if R[hour] > 0 or Dewpoint_wet[hour] > 0:
            W_dict[hour].append(1)
            
        else:
            W_dict[hour].append(0)
    
        if R[hour] == 0 and VPD[hour] > 4.5:
            HT = HT
        elif R[hour] > 0 or VPD[hour] == 4.5:
            if T[hour] <= 0:
                HT = HT 
            else:
                HT = HT + 1/(1330.1 - 116.19*T[hour] + 2.6256*T[hour]**2)          
        if HT >= 1.3 and HT <= 8.6:              #Check conditions if this is in PIS.
            if R[hour] >= 0.2:
                print(hour)
                check = True
    
                if event == 0: 
                    event_dict[count].append(hour)
                    HT_dict[count].append(HT)
                event += 1 
                
            if R[hour] == 0 and check == True:  #Ending condition to PIS event
                J.append(count)
                check = False
                event = 0 
                event_dict[count].append(hour)
                HT_dict[count].append(HT)
                count = count + 1
                
        if HT > 8.6 and len(event_dict[len(event_dict)]) < 2:

            event_dict[count].append(hour)
            HT_dict[count].append(HT)
            break
            
        if hour == hour_now and len(len(event_dict[len(event_dict)]) == 1):
            event_dict[count].append(hour)
            HT_dict[count].append(HT)
        
        
        HTh.append(HT)
        
        #In this case DORh and PMOh are the same because MMO = 1. I've kept them
        #seperate to keep the model more flexible.
        MMO = 1

        
        DORh.append(round(math.exp(-15.891 * math.exp(-0.653 * (HT + 1))),3))
        PMOh.append(round(MMO*math.exp(-15.891 * math.exp(-0.653 * (HT + 1))),3))
    
    if len(event_dict) == 0: 
        print ('There are no past or coming germination events. Your vineyard is not currently at risk of Downy Mildew.')
        do_nothing = True 
    if HTh[len(HTh)-1] < 1.3 and do_nothing == False:
        print ('The primary inoculation season has not exceed 3% yet.\nYour vineyard is not currently at risk of Downy Mildew.')
    
    if HTh[len(HTh)-1] > 8.6 and do_nothing == False:
        print ('The primary inoculation season has exceed 97% yet.\nYour vineyard is not at risk of Downy Mildew anymore.')
    
    #Safety check in case the final event has not ended yet. Remove it from simulation
    if len(event_dict[len(event_dict)]) < 2 and len(event_dict) >= 1 and do_nothing == False: 
        print('The final germination event starting on:', test_dict[event_dict[len(event_dict)][0]][7].strftime('%h-%d at %H:%M'),' has not ended within the requested timeframe\
 and was not included in the simulation')
        del event_dict[len(event_dict)]
    print (HTh)        
    return event_dict, W_dict, DORh, PMOh, HT_dict, HTh, do_nothing




"""This for function integrates the DOR of the time of each event and stores 
the values in a list. Each value represents the amount of oospores that have 
borken dormancy during any rain event. This is called the PMOc or the density of
each oospore cohort. This number SHOULD be between 0 and 1 however I can't find a way 
to make this true for all events. """ 

def PMOc_integration(event_dict, DORh, HT_dict, do_nothing):
    import scipy.integrate as integrate
    PMOc_dict = defaultdict(list)
    total_PMOc = 0
    for germ_events in event_dict:
        if do_nothing == True:
            break
        
        if germ_events >= 2: 
            DORh_integral = integrate.quad(lambda HT: 10.37*math.exp(-15.891*math.exp(-0.653*(HT+1))-0.653*(HT+1)),HT_dict[germ_events-1][0], HT_dict[germ_events][1])
        else:
            DORh_integral = integrate.quad(lambda HT: 10.37*math.exp(-15.891*math.exp(-0.653*(HT+1))-0.653*(HT+1)),0.0028, HT_dict[germ_events][1])

        if germ_events == len(event_dict):
            total_PMOc = integrate.quad(lambda HT: 10.37*math.exp(-15.891*math.exp(-0.653*(HT+1))-0.653*(HT+1)),HT_dict[1][0], HT_dict[germ_events][1])
        PMOc = DORh_integral[0]
        PMOc_dict[germ_events].append(round(PMOc,3))
        
    return PMOc_dict, total_PMOc

"""This for loop looks at the germination of the PMOs (physiologically mature oospores). 
GEO is the germinatED oospores (oospores with sporangia) and 
GER is the germinatION of oospores (formation of sporangia). 
SUS is the survival of sporangia given certian weather conditions. 
The conditions determine which value is appropriate for storage.
This is done for each cohort event (J)"""

"""I stored everything in a dictionary as a lot of the equations are looking for 
specific values at a specific time and this was the easiest way for me to handle
two values at the same time."""

def infection_modeling(event_dict, test_dict, W_dict, PMOc_dict, \
                       R, T, RH, bud_break, vol_sprayed, dose_sprayed, LAI_dict):
    GEO_dict = defaultdict(list)        #Germinated oospores
    ZRE_dict = defaultdict(list)        #Zoospores released from sporangia
    REL_dict = defaultdict(list)        #Zoospore release
    ZRE_dict = defaultdict(list)        #Zoospore released from sporangia
    ZDI_dict = defaultdict(list)        #Zoospores dispresed from soil to leaves
    GERh_dict = defaultdict(list)       #Germination of oospores
    spray_dict = defaultdict(list)
    app_total = defaultdict(list)
    r_list = []
    
    first_cond = 0
    total_app = 0
    loop_count = 0  #Included to prevent final loop from running until last iterations.
    time_check = 0 
    
    
    for i in range (1, 13):
        app_total[i].append(0)
    
    
    for germ_events in event_dict:
        #Initialize and reset all parameters for each cohort event
        GER = 0
        GEOy = 0            # germinated oospores
        SUSh = 0            #Survival of Sporangia 
        WD = 0              #Wetness Duration
        count = 0
        TDW = 0                        
        num = 0 
        denom = 0 
        loop_count += 1 
        event_app = 0 
        WD_TDW_list = defaultdict(list)
        sporangia_survive = True
        sporangia_dispersed = False
        incomplete = False
    
        starting_time = test_dict[event_dict[germ_events][0]][7]
        ending_time = test_dict[event_dict[germ_events][1]][7]
        print('\t', '-'*40,'\nRain event from:', starting_time.strftime('%h-%d %H:%M'),'to', ending_time.strftime('%h-%d %H:%M'), 'will cause a Downy Mildew germination event.\n')
        
        past_date = ending_time - datetime.datetime(2019,8, 15, 0)
        
        print(past_date.days)
        if past_date.days > 0:
            break
        
        for z in range(event_dict[germ_events][0], len(W_dict)):
            #checking the temeperature conditions
            if T[z] <= 0:
                    GER = GER       
            else:
                GER = GER + 1/(1330.1 - (116.19*T[z]) + (2.6256*(T[z]**2)))
            
            GERh_dict[z].append(round(GER,3))
            
            #At GER >= 1 germination process has ended and spores have become sporangia.
            if GER >= 1:
                GEOy = PMOc_dict[germ_events][0]
                GEO_dict[z].append(GEOy)
                print('Germination process will be completed at', test_dict[z][7].strftime('%h-%d %H:%M'))
                break
            if z == len(W_dict)-1:
                GEO_dict[z].append(0)
                print('Current germination process ('+str(int(GER*100))+'% complete) will not end before', test_dict[z][7].strftime('%h-%d %H:%M.'), 'Run simulation again before this date.')
                print('\t', '-'*40, '\n')
                incomplete = True
                break

        if incomplete == True:
            continue
        #for loop which caculates the survival of sporangia from their time of formation
        #(end of germination until zoospore release or until end of cohort event
        
        for phi in range(z, len(W_dict)):
            count += 1 
            SUSh = SUSh + 1/(24*(5.67-0.47*(T[z]*(1-RH[z]))+0.01*(T[z]*(1-RH[z]))**2))

            #print(SUSh)
            if SUSh <= 1:
                GEO_dict[phi].append(GEOy)
                sporangia_survive = True
            else: 
                GEO_dict[phi].append(0)
                print('Sporangia formed but did not survive. Died at:',test_dict[phi][7].strftime('%h-%d %H:%M'))#, '\nDo not apply Cu fungicide')
                temp_time = str(test_dict[phi][7].strftime('%Y-%m-%d '+'23:00:00'))
                app_total[int(test_dict[phi][6])].append(0)
                
                print('\t', '-'*40)
                sporangia_survive = False
                sporangia_dispersed = True
                break
            
            if W_dict[phi] != 0 :
                W = 1
            else:
                W = 0
            
            WD = WD + W
            TDW = (TDW*(count-1) + T[phi])/count
            WD_Benchmark = math.exp((-1.022+19.634)/TDW)
            WD_TDW_list[phi].append(WD*TDW)
    
            if WD >= WD_Benchmark:
                REL_dict[phi].append(1)
                print('Zoospores from viable sporangia will be released (to ground) at:', test_dict[phi][7].strftime('%h-%d %H:%M'))
                ZRE_dict[phi].append(GEO_dict[phi][0])
                break
            else:
                REL_dict[phi].append(0)
    
        #For loop which calculates the survival of zoorspores from release to end of 
        #cohort event
        for release in REL_dict:
            denom = 0
            if REL_dict[release][0] != 0:
                for i in range (phi, len(W_dict)):
                    counting = i + 1
                    if i+1 == len(W_dict):
                        break
                    num = i - phi
                    denom = denom + W_dict[counting][0]
                    if num > denom:
                        ZRE_dict[i].append(0)
                        break
                    if denom >= num:
                        ZRE_dict[i].append(1)
    
        #for loop which calculates the dispersion of the surviving zoospores
        if sporangia_survive == True:
            for surv in range (phi, i+1):
                count += 1 
                
                if W_dict[surv] != 0 :
                    W = 1
                else:
                    W = 0
                WD = WD + W
                TDW = (TDW * (count-1) + T[phi])/count
                
                if R[surv] >= 0.2:
                    if test_dict[surv][7] > bud_break:
                        print('Zoospores will be dispersed to grapevines at:', test_dict[surv][7].strftime('%h-%d %H:%M'))
                        ZDI_dict[surv].append(GEO_dict[z][0])
                        ZDI_dict[surv].append(test_dict[surv][7])
                        sporangia_dispersed = True
                
                infect_dict = defaultdict(list)
                infect_count = 0 
                for infect_date in ZDI_dict:
                    try:
                        if ZDI_dict[infect_date][0] > 0:
                            infect_dict[infect_count].append(infect_date)
                            infect_count = infect_count + 1
                    except:
                        continue
                #print(infect_dict)
                
                if sporangia_dispersed == True and WD*TDW >= 60:
                    print('Zoospores will cause infection at:', test_dict[surv][7].strftime('%h-%d %H:%M'))
                    temp_time = str(test_dict[surv][7].strftime('%Y-%m-%d '+'23:00:00'))
                    check_time = test_dict[surv][7].strftime('%h-%d %H:%M')
                    if check_time != time_check:
                        r_amount = 0 
                        time_dif = 365
                        
                        for checks in range (0+first_cond, len(infect_dict)):
                            if checks > 0+first_cond:
                                print (infect_dict[checks][0], 'check')
                                print (infect_dict[checks-1][0], 'check -1')
                                r_amount = sum(R[infect_dict[checks-1][0]:infect_dict[checks][0]])
                                time_dif = infect_dict[checks][0]-infect_dict[checks-1][0]
                                time_dif = time_dif/24
                                first_cond = checks
                                break
                        print(time_dif)
                        print(r_amount)
                        r_list.append(r_amount)
                        if r_amount < 5 and time_dif < 5:
                            app_total[int(test_dict[surv][6])].append(LAI_dict[temp_time][1]/2) 
                        else:
                            app_total[int(test_dict[surv][6])].append(LAI_dict[temp_time][1]) 
                        time_check = check_time
                        #print(LAI_dict[temp_time], 'temp_time')
                        print(app_total[int(test_dict[surv][6])])
                    else:
                        app_total[int(test_dict[surv][6])].append(0) 

                    
                    inf_app_prime = 0
                    inf_app_double_prime = 0
                    for inf_appearance in range(surv, len(test_dict)):
                        if inf_app_prime < 1:
                            inf_app_prime += 1/(24*(45.1-3.45*T[inf_appearance]+0.073*T[inf_appearance]**2))
                            if inf_app_prime >= 1:
                                prime = test_dict[inf_appearance][7].strftime('%h-%d %H:%M')
                        
                        if inf_app_double_prime < 1:
                            inf_app_double_prime += 1/(24*(59.9-4.55*T[inf_appearance]+0.095*T[inf_appearance]**2))
                            if inf_app_double_prime >= 1:
                                double_prime = test_dict[inf_appearance][7].strftime('%h-%d %H:%M')
                        
                        if inf_app_prime >= 1 and inf_app_double_prime >=1:
                            if prime > double_prime:
                                print('Infections will likely appear between:', double_prime, 'and', str(prime)+'.')
                                break
                            else:
                                print('Infections will likely appear between:', prime, 'and', str(double_prime)+'.')
                                break
                            
                        if inf_appearance == len(test_dict)-1:
                            if inf_app_double_prime < inf_app_prime:
                                print('Current incubation process ('+str(int(inf_app_double_prime*100))+'-'+str(int(inf_app_prime*100))+'% complete) has not ended. Oil spots will not appear before',\
                                      test_dict[inf_appearance][7].strftime('%h-%d %H:%M'), 'however primary infection has occurred.')
                            else:
                                print('Current incubation process ('+str(int(inf_app_prime*100))+'-'+str(int(inf_app_double_prime*100))+'% complete) has not ended. Oil spots will not appear before',\
                                      test_dict[inf_appearance][7].strftime('%h-%d %H:%M'), 'however priamry infections has occured.')      
                    break
                if surv == i:
                    ZDI_dict[surv].append(0)
    
        
        if sporangia_dispersed == False:
            if test_dict[surv][7] < bud_break:
                print('Zoospores were dispersed before budbreak. Do not apply Cu fungicide')
            else:
                print('Zoospores were released however no rain event dispersed them before dying.')
                print('Zoospores died at :', test_dict[i][7].strftime('%h-%d %H:%M'))
                print('Do not apply Cu fungicide')
                temp_time = str(test_dict[i][7].strftime('%Y-%m-%d '+'23:00:00'))
                app_total[int(test_dict[i][6])].append(0)
                #if test_dict[i][7] > datetime.datetime(2019,7,15):
                #    break

            print('\t', '-'*40)
            continue
        
        if sporangia_survive == False:
            continue
        
        dry_count = 0
        repeater = False
        for y in range (z, len(W_dict)):
            dry_count = 0 
            forward_dry_count = 0
            rainfall = 0
            if len(ZDI_dict[y]) > 0:
                for x in range(len(ZDI_dict[y])):
                    if ZDI_dict[y][x] != 0 and repeater == False:
                        repeater = True
                        for backwards in range (y, 0, -1):
                            best_app_time = False
                            if test_dict[backwards][0] != 0:
                                dry_count = 0
                            if test_dict[backwards][0] == 0:
                                dry_count += 1
                            if test_dict[backwards][0] == 0 and dry_count == 3:
                                #print('Apply fungicide before:', test_dict[backwards][7].strftime('%h-%d %H:%M'),'\n\t', '-'*40)
                                for dry_break in range(backwards, 0, -1):
                                    if test_dict[dry_break][0] != 0:
                                        if test_dict[dry_break+2][7] >test_dict[backwards][7]:
                                            print ('\nApply fungicide at:', test_dict[dry_break+2][7].strftime('%h-%d %H:%M'))
                                        else:
                                            print ('\nApply fungicide between:', test_dict[dry_break+2][7].strftime('%h-%d %H:%M'),'and:', test_dict[backwards+1][7].strftime('%h-%d %H:%M'))
                                        break
                                print_once = 0     
                                for near_time in range(backwards, dry_break+1, -1):
                                    if test_dict[near_time][8] > 1 and test_dict[near_time][8] < 2 and test_dict[near_time][1] < 25 and test_dict[near_time][2] > 0.4:
                                        print_once += 1 
                                        if print_once == 1:
                                            print ('Favorable wind condition times and speeds for application are:')
                                        #print(test_dict[near_time][7].strftime('%h-%d %H:%M.'), '\t|Wind Speed:', round(test_dict[near_time][8],1), '\t| Temp (Cel):', int(test_dict[near_time][1]), '\t|Rel Hum:', test_dict[near_time][2])
                                        best_app_time = True
                                    if near_time == dry_break+2 and best_app_time == False:
                                        print ('\nNo favorable wind condition speeds for this application window. Apply when convenient.')
                                break
                            else:
                                near_time = x
                        print_once = 0
                        for forwards in range (backwards+3, len(W_dict)):
                            if test_dict[forwards][0] != 0:
                                forward_dry_count = 0
                            if test_dict[forwards][0] == 0:
                                forward_dry_count += 1
                            if forward_dry_count == 3:
                                break
                            if test_dict[forwards][0] != 0 and forward_dry_count < 3:
                                rainfall = rainfall + test_dict[forwards][0]
                            pos_resplash = False    
                            if forwards != backwards+3 and test_dict[forwards-1][0] == 0 and test_dict[forwards-2][0] == 0 and test_dict[forwards+1][0] != 0:
            
                                for resplash in range (forwards, len(W_dict)):
                                    if test_dict[resplash][0] > 0.2:
                                        print('\nPossible recontamination at:', test_dict[resplash][7].strftime('%h-%d %H:%M'))
                                        pos_resplash = True
                                        break
                                if pos_resplash == True:
                                    print('Two hour dry window to reapply from:', test_dict[forwards-2][7].strftime('%h-%d %H:%M'), 'and', test_dict[forwards][7].strftime('%h-%d %H:%M'))
            

                        if rainfall <= 5:
                            print('\nIt will rain', round(rainfall,2), 'mm between:', test_dict[backwards+3][7].strftime('%h-%d %H:%M'), 'and', test_dict[forwards-3][7].strftime('%h-%d %H:%M'), '\nApply 0.3 g/L. at', round(dose_sprayed),'g/ha')
                            #print(test_dict[near_time][6])
                            dose_sprayed = dose_sprayed/2
                            total_app = total_app + event_app
                            spray_dict[test_dict[near_time][6]].append(dose_sprayed)
                        if rainfall > 5:
                            print('\nIt will rain', round(rainfall,2), 'mm between:', test_dict[backwards+3][7].strftime('%h-%d %H:%M'), 'and', test_dict[forwards-3][7].strftime('%h-%d %H:%M'), '\nApply 0.5 g/L. at', round(dose_sprayed),'g/ha')
                            dose_sprayed = dose_sprayed
                            #print(test_dict[near_time][6])
                            spray_dict[test_dict[near_time][6]].append(dose_sprayed)
                        #if rainfall > 30:
                        #    print('\nIt will rain', round(rainfall,2), 'mm between:', test_dict[backwards+3][7].strftime('%h-%d %H:%M'), 'and', test_dict[forwards-3][7].strftime('%h-%d %H:%M'), '\nApply 0.7 g/L. at', round(vol_sprayed),'L/ha')
                        #    event_app = (event_app + 0.7*vol_sprayed)/1000
                        #    total_app = total_app + event_app
                        print('\t', '-'*40)
                        
    return spray_dict, app_total, ZDI_dict, infect_dict, r_list
                    

