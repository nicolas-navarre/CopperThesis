#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 30 11:47:34 2019

@author: nicolasnavarre
"""

#import forecastio 
import math
import datetime
import requests

from collections import defaultdict
from datetime import timedelta

def weather_data_2017_v3(first_day,delta,future_cast,lat,lng):
    
    """'Dark Sky' key needed for weather information."""
    #api_key = 'b028e52ba07428fb70a3c4de4748c2e0'

    hourly_dict = defaultdict(list)
    count = 0
    delta = 365
    
    for y in range (0,delta):
        date = first_day + timedelta(days=y)
    
        #forecast = forecastio.load_forecast(api_key,lat, lng, date, units= "si")
        #print('hi')
        #byHour = forecast.hourly()
        #print(byHour.data)
        #if len(byHour.data) < 24:
        API_KEY = '60b147b1804b42789e694630192705'
        url = 'https://api.worldweatheronline.com/premium/v1/past-weather.ashx?key='+API_KEY+'&q='+str(lat)+','+str(lng)+'45&date='+date.strftime('%Y-%m-%d')+'&tp=1&format=json'
        req = requests.get(url)
        req = req.json()
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
        print(hourly_dict[count-1][7].strftime("%B-%d"), '\tLoading Data...')
    local_dict = hourly_dict
    print('Data successfully loaded.')
    
    if -1 in local_dict:
        del local_dict[-1]

    return local_dict
        
        
"""        
        pass
        try_count = 0 
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
                    hourly_dict[count-(24-int(hourly_dict[count][4]))] = hourly_dict[count]
                    print('del')
                    del hourly_dict[count]
                    count = count - 1
                    try_count -= 1
                if hourly_dict[count][7] == hourly_dict[count-1][7]:
                    hourly_dict[count-1] = hourly_dict[count]
                    print('delete')
                    del hourly_dict[count]
                    count = count - 1
                    try_count -= 1 
                try_count += 1
                
            except:
                print('yo')
                del hourly_dict[count]
                API_KEY = '60b147b1804b42789e694630192705'
                url = 'https://api.worldweatheronline.com/premium/v1/past-weather.ashx?key='+API_KEY+'&q='+str(lat)+','+str(lng)+'45&date='+date.strftime('%Y-%m-%d')+'&tp=1&format=json'
                req = requests.get(url)
                req = req.json()
                #print('Loading Data: \t', date.strftime('%Y-%m-%d'))
                count = count - try_count 
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
    
    """