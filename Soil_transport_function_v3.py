#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  2 15:27:57 2019

@author: nicolasnavarre
"""

from collections import defaultdict
from scipy.integrate import odeint

import math
import numpy
import calendar


def soil_transport(spray_dict, bulk_p, soil_om, soil_sand, soil_pH, soil_clay,\
                   soil_awc, cu_conc, monthly_rain_dict, weather_dict, WU_dict, app_total,\
                   soil_wcfc, soil_wcwp):

    
    copper_dict = defaultdict(list)
    copper_dict['month #'].append('ct_Cu_tot mg/kg')
    copper_dict['month #'].append('[Cu]tot mg/L')
    copper_dict['month #'].append('Cu_bio mg/kg')
    copper_dict['month #'].append('Q_leach m/month')   
    
    beta_0 = 0.400
    beta_1 = 1.152
    beta_2 = 0.023
    beta_3 = -0.171
    
    "Convert mg/kg soil to mol/kg"
    print(round(cu_conc,3), 'Initial Cu tot mg/kg soil')
    cu_conc_mol = cu_conc * 1/(63.546*1000)
    bulk_p_m3 = bulk_p*1000

    "Calculate initial mol/kg reactive"
    ln_ctCu_re = beta_0+beta_1*math.log(float(cu_conc_mol))+beta_2*math.log(float(soil_om))+beta_3*math.log(float(soil_clay))
    ctCu_re_init = math.exp(ln_ctCu_re)
    print(round(ctCu_re_init*1000*63.546,3), 'Initial Cu react mg/kg soil')
    
    "Calculate initial mol/L concentration" 
    k_d = math.exp(0.68+0.16*soil_pH)
    Cu_tot_ss_init = ctCu_re_init/k_d
    print(round(Cu_tot_ss_init,8), 'Initial Cu mol/L')
    Cu_tot_ss_init_mg = Cu_tot_ss_init*1000*63.546
    Cu_tot_ss_init_mg_m3 = Cu_tot_ss_init_mg*1000
    print(round(Cu_tot_ss_init_mg,3), 'Initial Cu mg/L')
    
    n = 0.85
    alpha_0 = -2.26
    alpha_1 = 0.89
    alpha_2 = 0.90
    
    "Calculate initial bio fraction mg/kg root"
    ln_Kf = alpha_0 + alpha_1*soil_pH + alpha_2*math.log(soil_om)
    Kf = math.exp(ln_Kf)
    
    n_bio = 16005.86
    KA_Cu = math.exp(4.29)
    KA_Mg = math.exp(2.35)
    
    Cu_free_init = (ctCu_re_init/Kf)**(1/n)
    print(Cu_free_init, 'inital free Cu2+')
    Mg_free = (0.95/(24.305*1000))*1000*1000
    Cu_bio = (n_bio*KA_Cu*(Cu_free_init*10**6))/(1+KA_Mg*Mg_free)
    print(round(Cu_bio,3), 'Initial Cu mg/kgroot')

    "Calculate solid-solution partition"
    ln_kd = 0.3793*float(soil_pH) + 0.1476*float(soil_om)-1.0417
    kd = math.exp(ln_kd)
    kd_m3 = kd/1000
    
    copper_dict['initial'].append(round(cu_conc,3))
    copper_dict['initial'].append(round(Cu_tot_ss_init_mg,3))
    copper_dict['initial'].append(round(Cu_bio,3))
    
    monthly_dict = defaultdict(list)
    
    soil_awc = (soil_wcfc+soil_wcwp)/2
    g = ((n_bio*KA_Cu)/(1+KA_Mg*Mg_free))*((k_d/Kf)**(1/n))
    c = ((0.2/1.65)*g)/(bulk_p_m3*0.2*kd_m3+soil_awc*0.2)
    #/(bulk_p_m3*0.2*kd_m3+soil_awc*0.2)
    print(g, '= g')
    
    for month in app_total:
        print('\n'+calendar.month_name[month])
        monthly_dose = 0
        monthly_uptake = 0
        monthly_precip = 0 

        for app in app_total[month]:
            monthly_dose += app
            
        soil_awc = (soil_wcfc+soil_wcwp)/2
        monthly_dose = (monthly_dose/10000)*1000
        
        "A units are mg/m3-yr"
        A = (monthly_dose*0.84)/(bulk_p_m3*0.2*kd_m3+soil_awc*0.2)
        
        #A = A/1000/63.546/10000
        print(round(A,3), 'A mg/m3-month')
        
        for water_uptake in WU_dict:
            if WU_dict[water_uptake][1] == month:
                monthly_uptake += WU_dict[water_uptake][0]
        
        for precip in weather_dict:
            if int(weather_dict[precip][6]) == month:
                monthly_precip += weather_dict[precip][0]
        
        "Q_leach in mm"
        Q_leach = monthly_precip*0.108
        "Q_leach in meters"
        Q_leach = Q_leach/1000
        print(round(Q_leach,3), 'Q_leach m/month')
        
        "b units are 1/yr Q_leach in m/time, bulk_p_m3 in kg/m3, 0.2m, kd_m3 in m3/kg, soil_awc m/m"
        b = Q_leach/(bulk_p_m3*0.2*kd_m3+soil_awc*0.2)
        print(b, '= b in 1/month')
        "Numerically solve dif eq."
        def distribute(x,t):
            
            x_mol = x/(1000*63.546*1000)
            dxdt = A-b*x-(c*(x_mol**(1/n)))
            
            return dxdt
        
        month_length = calendar.monthrange(2019,month)
        
        t = numpy.linspace(0,month_length[1]/365,100)
        xo = Cu_tot_ss_init_mg_m3
        y = odeint(distribute,xo,t)
        new = float(y[99]/1000)
        print(round(new,3), 'Cu_tot_ss_new mg/L')
        Cu_tot_ss_T = float(y[99])
        
        "Get Cu_tot_ss_T from mg/m3 to mol/L"
        Cu_tot_ss_T = Cu_tot_ss_T/(1000*1000*63.546)
    
        "Calculate new equilibirium Cu_tot_ss_T at time T"
        #Cu_tot_ss_test = (Cu_tot_ss_init-A/b)*math.exp(-b/12)+A/b
        #print(round(Cu_tot_ss_test,3), 'compare y_final')
        
        "Get Cu_tot_ss_T to mg/L from mol/L"
        Cu_tot_ss_T_mg = Cu_tot_ss_T*1000*63.546

        "Calculate new ct_Cu_re based on new Cu_tot_ss_T"
        ct_Cu_re = Cu_tot_ss_T*k_d
    
        
        "Calculate new ct_Cu_tot base on new ct_Cu_re"
        ln_ct_Cu_tot = (math.log(ct_Cu_re)-beta_0-beta_2*math.log(soil_om)-beta_3*math.log(soil_clay))/beta_1
        ct_Cu_tot = math.exp(ln_ct_Cu_tot)
        ct_Cu_tot_mg = ct_Cu_tot*63.546*1000


        "Calculate new Cu_free/bio uptake based on new ct_Cu_re"
        Cu_free = (ct_Cu_re/Kf)**(1/n)
        Cu_bio = (n_bio*KA_Cu*(Cu_free*10**6))/(1+KA_Mg*Mg_free)
        print(Cu_bio, 'Cu_bio mg/kgroot')

        print(round(ct_Cu_tot_mg,3), 'New Cu tot mg/kg soil')
        print(round(ct_Cu_re*1000*63.546,3), 'New Cu react mg/kg soil')
        print(round(Cu_tot_ss_T_mg, 3), 'New Cu mg/L')

        "Append monthly data"
        copper_dict[month].append(round(ct_Cu_tot_mg,3))
        copper_dict[month].append(round(Cu_tot_ss_T_mg,3))
        copper_dict[month].append(round(Cu_bio,5))
        copper_dict[month].append(round(Q_leach,3))

        monthly_dict[month].append(A)
        monthly_dict[month].append(b)
        monthly_dict[month].append(Cu_tot_ss_T_mg)
        
        "Set the current [Cu_tot_ss] as the new intial"
        Cu_tot_ss_init_mg_m3 = float(y[99])
        
    return monthly_dict, copper_dict

def erosion_calc(weather_dict, LAI, lat, lng, location, k_factor, p_factor, ls_factor, spray_dict):

    
    
    monthly_rain_dict = defaultdict(list)
    erosion_monthly_dict = defaultdict(list)
    monthly_rain = 0
    count = 1 
    LU_vineyard = 7
    for rain in weather_dict:
        if weather_dict[rain][0] != 'No Data':
            if rain > 1: 
                if weather_dict[rain][6] == weather_dict[rain-1][6]:
                    if weather_dict[rain][0] != 0:   
                        monthly_rain += weather_dict[rain][0]
                        count += 1 
                    if monthly_rain < 10 and weather_dict[rain][0] == 0:
                        monthly_rain = 0
                        count = 1 
                else:
                    if monthly_rain > 10:
                        monthly_rain_dict[weather_dict[rain-1][6]].append(monthly_rain)
                        monthly_rain_dict[weather_dict[rain-1][6]].append(count)
                        monthly_rain_dict[weather_dict[rain-1][6]].append(monthly_rain/count)
                    else:
                        monthly_rain_dict[weather_dict[rain-1][6]].append(0)
                        monthly_rain_dict[weather_dict[rain-1][6]].append(0)
                        monthly_rain_dict[weather_dict[rain-1][6]].append(0)
                    monthly_rain = weather_dict[rain][0]
                    count = 1    
                    
                if rain == len(weather_dict)-1:
                    monthly_rain_dict[weather_dict[rain-1][6]].append(monthly_rain)
                    monthly_rain_dict[weather_dict[rain-1][6]].append(count)
                    monthly_rain_dict[weather_dict[rain-1][6]].append(monthly_rain/count)

    v_factor = math.exp(LU_vineyard*(1-math.exp(-0.431*LAI)))

    for r_factor in monthly_rain_dict:
        if monthly_rain_dict[r_factor][0]!= 0:
            erosion = ((524+222*math.log10(monthly_rain_dict[r_factor][2]))/v_factor)*k_factor*(ls_factor/p_factor)
            erosion_monthly_dict[r_factor].append(round(erosion,4))
    if len(erosion_monthly_dict) == 0:
        print('No expected water erosion at this time.')
    else:
        for key in erosion_monthly_dict:
            month = int(key)
            monthly_loss = round(erosion_monthly_dict[key][0]*1000,4)
         
            print(calendar.month_name[month]+':', str(monthly_loss)+' kg/ha soil eroded.')
    
    return monthly_rain_dict, erosion_monthly_dict