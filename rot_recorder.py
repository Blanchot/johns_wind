#!/usr/bin/python3

'''15 April 2019: Rotterdam Weather Recorder to run on Diana
Recording: [temp, windr (direction), windkmh, lv (humidity), luchtd (pressure), sup (sunrise), sunder (sunset)]
at 10 minute intervals and storing these in a csv file
Info over the weerlive API: http://weerlive.nl/delen.php
Requires: records.txt in the same folder
'''

import requests, json
import datetime
import time
#import pprint

rwl= dict()

def tijd():
  timestamp= int(time.time())
  localtime= datetime.datetime.fromtimestamp(timestamp)
  #localdate= localtime.strftime('%d-%m-%Y')
  localdate= localtime.strftime('%d-%m')
  #localtime= localtime.strftime('%H:%M:%S')
  localtime= localtime.strftime('%H:%M')
  timestamp= str(timestamp)
  d_t= localdate + ' ' + localtime
  #print(localdate)
  #print(localtime)
  return d_t

def convert_wind_dir(wind_dir: str) -> str:
  if wind_dir == 'Noord': #North (N)
    wind_dir= 'N  '
  elif wind_dir == 'NNO': #North-northeast (NNE)
    wind_dir= 'NNE' 
  elif wind_dir == 'NO': # Northeast (NE)
    wind_dir= 'NE '
  elif wind_dir == 'ONO': #East-northeast (ENE)
    wind_dir= 'ENE'
  elif wind_dir == 'Oost': # East (E)
    wind_dir= 'E  '
  elif wind_dir == 'OZO': # East-southeast (ESE)
    wind_dir= 'ESE'
  elif wind_dir == 'ZO': # Southeast (SE)
    wind_dir= 'SE '
  elif wind_dir == 'ZZO': # South-southeast (SSE)
    wind_dir= 'SSE'
  elif wind_dir == 'Zuid': # South (S)
    wind_dir= 'S  '
  elif wind_dir == 'ZZW': # South-southwest (SSW)
    wind_dir= 'SSW'
  elif wind_dir == 'ZW': # Southwest (SW)
    wind_dir= 'SW '
  elif wind_dir == 'WZW': # West-southwest (WSW)
    wind_dir= 'WSW'
  elif wind_dir == 'West': # West (W)
    wind_dir= 'W  '
  elif wind_dir == 'WNW': # West-northwest (WNW)
    wind_dir= 'WNW'
  elif wind_dir == 'NW': # Northwest (NW)
    wind_dir= 'NW '
  elif wind_dir == 'NNW': # North-northwest (NNW)
    wind_dir= 'NNW'
  else:
        print('No wind direction')
  return wind_dir
  
def peil():
  global rwl
  weerlive = "http://weerlive.nl/api/json-10min.php?locatie=Rotterdam"
  try:
    rwl= requests.get(weerlive).json() #rwl is dictionary object
    #print(rwl)
    #pprint.pprint(rwl)
    temp= rwl['liveweer'][0]['temp'] #temp: str
    wind_dir= rwl['liveweer'][0]['windr'] #wind_dir: str
    wind_dir= convert_wind_dir(wind_dir)
    wind_kmh= rwl['liveweer'][0]['windkmh'] #wind_kmh: str
    humid= rwl['liveweer'][0]['lv'] #humid: str
    press= rwl['liveweer'][0]['luchtd'] #press: str
    sun_up= rwl['liveweer'][0]['sup'] #sun_up: str
    sunset= rwl['liveweer'][0]['sunder'] #sunset: str
    d_t= tijd()
    data= d_t+ ', '+temp+', '+wind_dir+', '+wind_kmh+', '+humid+', '+press
    #print(data)
    
    fileobj= open('/home/pi/rotweer/records.txt', 'a')
    fileobj.write(update)
    fileobj.write("\n")
    fileobj.close
  
  except requests.ConnectionError:
    print("Error querying WeerLive API")

#peil()

while True:
  peil()
  time.sleep(600)

