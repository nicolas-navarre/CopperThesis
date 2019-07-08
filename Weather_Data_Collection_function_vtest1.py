#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 12:39:32 2019

@author: nicolasnavarre
"""

import forecastio 
import math
import datetime
import requests

from collections import defaultdict
from datetime import timedelta

"""Gather the weather data starting on the 1st of every year until
the requested date. The information is pulled from the Dark Sky API.
The data is stored a dictionary with a line number sor"""
def weather_data(first_day,delta,future_cast,lat,lng):
    
    """'Dark Sky' key needed for weather information."""
    api_key = 'b028e52ba07428fb70a3c4de4748c2e0'
    
    hourly_dict = defaultdict(list)
    count = 0

    for y in range (0,delta.days):
        date = first_day + timedelta(days=y)
    
        forecast = forecastio.load_forecast(api_key,lat, lng, date, units= "si")
        #print('hi')
        byHour = forecast.hourly()
        #print(byHour.data)
        """
        if len(byHour.data) < 24:
            API_KEY = '60b147b1804b42789e694630192705'
            url = 'https://api.worldweatheronline.com/premium/v1/past-weather.ashx?key='+API_KEY+'&q='+str(lat)+','+str(lng)+'45&date='+date.strftime('%Y-%m-%d')+'&tp=1&format=json'
            req = requests.get(url)
            req = req.json()
            print(req)
            #print('Loading Data: \t', date.strftime('%Y-%m-%d'))

            for i in req['data']['weather'][0]['hourly']:
                #print('hello')
                try:
                    hourly_dict[count].append(float(i['precipMM']))
                except:
                    hourly_dict[count].append(i['summary'])
                hourly_dict[count].append(float(i['tempC']))
                try:
                    hourly_dict[count].append(float(i['humidity'])/100)
                except:
                    hourly_dict[count].append(hourly_dict[count-1][2])
                
                ES = 0.61078*math.exp((17.27*float(i['tempC']))/(float(i['tempC'])+237.3))
                EA = hourly_dict[count][2] * ES
                VPD = ES - EA
                hourly_dict[count].append(round(VPD,3))
                #darksky_data[count].append(i['icon'])
                #darksky_data[count].append(datetime.datetime.utcfromtimestamp(int(i['time'])).strftime('%H'))
                #darksky_data[count].append(datetime.datetime.utcfromtimestamp(int(i['time'])).strftime('%d'))
                #darksky_data[count].append(datetime.datetime.utcfromtimestamp(int(i['time'])).strftime('%m'))
                if len(i['time']) == 1:   
                    hourly_dict[count].append('0'+i['time'])
                if len(i['time']) == 3:
                    hourly_dict[count].append('0'+i['time'][0])
                if len(i['time']) == 4:
                    hourly_dict[count].append(i['time'][:2])
                
                #hour = date + timedelta(hours = int(hourly_dict[count][4]) -1)
                hourly_dict[count].append(date.strftime('%d'))
                hourly_dict[count].append(date.strftime('%m'))
                date_time_obj = datetime.datetime.strptime(date.strftime('%Y-%m-%d '+str(hourly_dict[count][4])+':00:00'), '%Y-%m-%d %H:%M:%S')
                hourly_dict[count].append(date_time_obj)
                
                try:
                    hourly_dict[count].append(round(float(i['windspeedKmph'])/3.6,3))
                    hourly_dict[count].append(float(i['winddirDegree']))
                except:
                    hourly_dict[count].append('No Data')
                    hourly_dict[count].append('No Data')
                try:
                    hourly_dict[count].append(float(i['DewPointC']))
                except:
                    hourly_dict[count].append('No Data') 
                count = count + 1
            pass
        """    
        for hourlyData in byHour.data:
            try:
                hourly_dict[count].append(hourlyData.precipIntensity)
                hourly_dict[count].append(hourlyData.temperature)
                hourly_dict[count].append(hourlyData.humidity)
                
                ES = 0.61078*math.exp((17.27*hourlyData.temperature)/(hourlyData.temperature+237.3))
                EA = hourlyData.humidity * ES
                VPD = ES - EA
                hourly_dict[count].append(round(VPD,3))
                hourly_dict[count].append(hourlyData.time.hour)
                hourly_dict[count].append(hourlyData.time.day)
                hourly_dict[count].append(hourlyData.time.month)
                hourly_dict[count].append(hourlyData.time)
                hourly_dict[count].append(hourlyData.windSpeed)
                hourly_dict[count].append(hourlyData.windBearing)
                hourly_dict[count].append(hourlyData.dewPoint)
                if hourly_dict[count][7] == hourly_dict[count-(24-int(hourly_dict[count][4]))][7]:
                    hourly_dict[count-1] = hourly_dict[count]
                    del hourly_dict[count]
                    count = count - 1
                if hourly_dict[count][7] == hourly_dict[count-1][7]:
                    hourly_dict[count-1] = hourly_dict[count]
                    del hourly_dict[count]
                    count = count - 1
            except:
                API_KEY = '60b147b1804b42789e694630192705'
                url = 'https://api.worldweatheronline.com/premium/v1/past-weather.ashx?key='+API_KEY+'&q='+str(lat)+','+str(lng)+'45&date='+date.strftime('%Y-%m-%d')+'&tp=1&format=json'
                req = requests.get(url)
                req = req.json()
                #print('Loading Data: \t', date.strftime('%Y-%m-%d'))
                print(req)
                for i in req['data']['weather'][0]['hourly']:
                    #print('hello')
                    try:
                        hourly_dict[count].append(float(i['precipMM']))
                    except:
                        hourly_dict[count].append(i['summary'])
                    hourly_dict[count].append(float(i['tempC']))
                    try:
                        hourly_dict[count].append(float(i['humidity'])/100)
                    except:
                        hourly_dict[count].append(hourly_dict[count-1][2])
                    
                    ES = 0.61078*math.exp((17.27*float(i['tempC']))/(float(i['tempC'])+237.3))
                    EA = hourly_dict[count][2] * ES
                    VPD = ES - EA
                    hourly_dict[count].append(round(VPD,3))
                    #darksky_data[count].append(i['icon'])
                    #darksky_data[count].append(datetime.datetime.utcfromtimestamp(int(i['time'])).strftime('%H'))
                    #darksky_data[count].append(datetime.datetime.utcfromtimestamp(int(i['time'])).strftime('%d'))
                    #darksky_data[count].append(datetime.datetime.utcfromtimestamp(int(i['time'])).strftime('%m'))
                    if len(i['time']) == 1:   
                        hourly_dict[count].append('0'+i['time'])
                    if len(i['time']) == 3:
                        hourly_dict[count].append('0'+i['time'][0])
                    if len(i['time']) == 4:
                        hourly_dict[count].append(i['time'][:2])
                    
                    #hour = date + timedelta(hours = int(hourly_dict[count][4]) -1)
                    hourly_dict[count].append(date.strftime('%d'))
                    hourly_dict[count].append(date.strftime('%m'))
                    date_time_obj = datetime.datetime.strptime(date.strftime('%Y-%m-%d '+str(hourly_dict[count][4])+':00:00'), '%Y-%m-%d %H:%M:%S')
                    hourly_dict[count].append(date_time_obj)
                    
                    try:
                        hourly_dict[count].append(round(float(i['windspeedKmph'])/3.6,3))
                        hourly_dict[count].append(float(i['winddirDegree']))
                    except:
                        hourly_dict[count].append('No Data')
                        hourly_dict[count].append('No Data')
                    try:
                        hourly_dict[count].append(float(i['DewPointC']))
                    except:
                        hourly_dict[count].append('No Data') 
                    count = count + 1
                break
            count = count + 1
        #print(hourly_dict)

        try:
            print(hourlyData.time.strftime("%B-%d"), '\tLoading Data...')
        except UnboundLocalError:
            print(hourly_dict[count-1][7].strftime("%B-%d"), '\tLoading Data...')
    
    local_dict = hourly_dict
    print('Data successfully loaded.')
    
    if -1 in local_dict:
        del local_dict[-1]

    return local_dict

def weather_lists (weather_dict):
    # # Rainfall in mm 
    R = []
    # Temperature at each hour in Celsius 
    T = []
    # Relative humidity in %
    RH = []
    # Vapour pressure deficit in hPa. Calculated from temperature and relative humidity
    VPD = []
    Dewpoint = []
    Dewpoint_wet = []
    for hour in weather_dict:
        print (weather_dict[hour])
        if weather_dict[hour][0] != 'No Data':
            R.append(weather_dict[hour][0])
            T.append(weather_dict[hour][1])
            RH.append(weather_dict[hour][2])
            VPD.append(round(weather_dict[hour][3],3))
            Dewpoint.append(weather_dict[hour][10])
        else:
            #print(test_dict[j])
            R.append(0)
            T.append(0)
            RH.append(0)
            VPD.append(0)
        if T[hour] < 0:
            Dewpoint_wet.append(0)
        elif T[hour]-Dewpoint[hour] > 3.7:
            Dewpoint_wet.append(0)
        else:
            if weather_dict[hour][8]< 2.5:
                inequality = 1.6064*T[hour]**0.5 + 0.0036*T[hour]**2 + 0.1531*RH[hour]*100\
                                     - 0.4599*weather_dict[hour][8] * (T[hour]-Dewpoint[hour])\
                                     - 0.0035*T[hour] * RH[hour]*100
                #print(inequality)
                if inequality > 14.4674:
                    Dewpoint_wet.append(1)
                else:
                    Dewpoint_wet.append(0)
            else:
                if RH[hour] < 0.878:
                    Dewpoint_wet.append(0)
                else:
                    inequality = 0.7921*T[hour]**0.5 + 0.0046*RH[hour]*100 - 2.3889*weather_dict[hour][8]\
                    - 0.0390*T[hour] * weather_dict[hour][8] + 1.0613*weather_dict[hour][8]*(T[hour]-Dewpoint[hour])
                    if inequality > 37:
                        Dewpoint_wet.append(1)
                    else:
                        Dewpoint_wet.append(0)
                    
            Dewpoint_wet.append(0)
    return R,T,RH,VPD, Dewpoint, Dewpoint_wet


def update_data(first_day,delta,future_cast,lat,lng, weather_dict):
    
    """'Dark Sky' key needed for weather information."""
    api_key = '91ac2cb8df7e71cca56a0dbf8ff2d3f8'
    
    hourly_dict = defaultdict(list)  
    start_point = weather_dict[len(weather_dict)-1][7]
    
    start_point = start_point - first_day
    print(start_point)
    future_days = datetime.datetime.now() + timedelta(days=future_cast)
    future_days = future_days - first_day
    count = len(weather_dict)
    for y in range (start_point.days,future_days.days):
        date = first_day + timedelta(days=y+1)
        forecast = forecastio.load_forecast(api_key,lat, lng, date, units= "si")
        byHour = forecast.hourly()
        for hourlyData in byHour.data:
            try:
                hourly_dict[count].append(hourlyData.precipIntensity)
                hourly_dict[count].append(hourlyData.temperature)
                hourly_dict[count].append(hourlyData.humidity)
                
                ES = 0.61078*math.exp((17.27*hourlyData.temperature)/(hourlyData.temperature+237.3))
                EA = hourlyData.humidity * ES
                VPD = ES - EA
                hourly_dict[count].append(round(VPD,3))
                hourly_dict[count].append(hourlyData.time.hour)
                hourly_dict[count].append(hourlyData.time.day)
                hourly_dict[count].append(hourlyData.time.month)
                hourly_dict[count].append(hourlyData.time)
                hourly_dict[count].append(hourlyData.windSpeed)
                hourly_dict[count].append(hourlyData.windBearing)
                hourly_dict[count].append(hourlyData.dewPoint)
                
            except:
                hourly_dict[count].append('No Data')
                hourly_dict[count].append('No Data')
                hourly_dict[count].append('No Data')
                hourly_dict[count].append('No Data')
                hourly_dict[count].append(hourlyData.time.hour)
                hourly_dict[count].append(hourlyData.time.day)
                hourly_dict[count].append(hourlyData.time.month)
                hourly_dict[count].append(hourlyData.time)
                hourly_dict[count].append('No Data')
                hourly_dict[count].append('No Data')
                hourly_dict[count].append('No Data')
                hourly_dict[count].append('No Data')
            count = count + 1
    
        try:
            if update_data == True:
                print('yo')
                print(hourlyData.time.strftime("%B-%d"), '\tUpdating Data...')
            else:
                print('yoyo')
                print(hourlyData.time.strftime("%B-%d"), '\tLoading Data...')
        except UnboundLocalError:
            if update_data == True:
                print('hello')
                print(hourly_dict[count-1][7].strftime("%B-%d"), '\tUpdating Data...')
            else:
                print('howdy')
                print(hourly_dict[count-1][7].strftime("%B-%d"), '\tLoading Data...')
            
    local_dict = hourly_dict
    print('Data successfully updated and loaded.')
    
    
    return local_dict