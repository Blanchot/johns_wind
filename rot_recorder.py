#!/usr/bin/python3

'''15 April 2019: Rotterdam Weather Recorder to run on Diana
Recording: [temp, windr (direction), windkmh, lv (humidity), luchtd (pressure), sup (sunrise), sunder (sunset)]
at 10 minute intervals and storing these in a csv file
Info over the weerlive API: http://weerlive.nl/delen.php
Requires: records.txt in the same folder

17 April 2019: Added summary and image (icon) recording and conversion
  
Wind Direction: https://en.m.wikipedia.org/wiki/Wind_direction
https://nl.m.wikipedia.org/wiki/Windstreek
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
  d_t= localdate + ' ' + localtime
  #print(localdate)
  #print(localtime)
  return d_t


def convert_wind_dir(wind_dir: str) -> str:
  '''Convert NL to UK and add compass directions
  Winds COME from the direction/compass point given'''
  if wind_dir == 'Noord': #North (N)
    wind_dir= 'N, 0'
  elif wind_dir == 'NNO': #North-northeast (NNE)
    wind_dir= 'NNE, 22.5' 
  elif wind_dir == 'NO': # Northeast (NE)
    wind_dir= 'NE, 45'
  elif wind_dir == 'ONO': #East-northeast (ENE)
    wind_dir= 'ENE, 67.5'
  elif wind_dir == 'Oost': # East (E)
    wind_dir= 'E, 90'
  elif wind_dir == 'OZO': # East-southeast (ESE)
    wind_dir= 'ESE, 112.5'
  elif wind_dir == 'ZO': # Southeast (SE)
    wind_dir= 'SE, 135'
  elif wind_dir == 'ZZO': # South-southeast (SSE)
    wind_dir= 'SSE, 157.5'
  elif wind_dir == 'Zuid': # South (S)
    wind_dir= 'S, 180'
  elif wind_dir == 'ZZW': # South-southwest (SSW)
    wind_dir= 'SSW, 202.5'
  elif wind_dir == 'ZW': # Southwest (SW)
    wind_dir= 'SW, 225'
  elif wind_dir == 'WZW': # West-southwest (WSW)
    wind_dir= 'WSW, 247.5'
  elif wind_dir == 'West': # West (W)
    wind_dir= 'W, 270'
  elif wind_dir == 'WNW': # West-northwest (WNW)
    wind_dir= 'WNW, 292.5'
  elif wind_dir == 'NW': # Northwest (NW)
    wind_dir= 'NW, 315'
  elif wind_dir == 'NNW': # North-northwest (NNW)
    wind_dir= 'NNW, 337.5'
  else:
        print('ERR, ERR')
  return wind_dir


def convert_summary(summary: str) -> str:
  if summary == 'onbewolkt':
    summary= 1
  elif summary == 'licht bewolkt':
    summary= 2
  elif summary == 'half bewolkt':
    summary= 3
  elif summary == 'geheel bewolkt':
    summary= 4
  elif summary == 'zwaar bewolkt':
    summary= 5
  elif summary == 'motregen':
    summary= 6
  elif summary == 'lichte motregen':
    summary= 7
  elif summary == 'dichte motregen':
    summary= 8
  elif summary == 'lichte motregen en regen':
    summary= 9
  elif summary == 'droog na motregen':
    summary= 10
  elif summary == 'motregen en regen':
    summary= 11
  elif summary == 'af en toe lichte regen':
    summary= 12
  elif summary == 'lichte regen':
    summary= 13
  elif summary == 'regen':
    summary= 14
  elif summary == 'droog na regen':
    summary= 15
  else:
    summary= 0
    print('Unknown! ->:', summary)
  return str(summary)


def convert_image(image: str) -> str:
  if image == 'zonnig':
    image= 1
  elif image == 'bliksem':
    image= 2
  elif image == 'regen':
    image= 3
  elif image == 'buien':
    image= 4
  elif image == 'hagel':
    image= 5
  elif image == 'mist':
    image= 6
  elif image == 'sneeuw':
    image= 7
  elif image == 'bewolkt':
    image= 8
  elif image == 'halfbewolkt':
    image= 9
  elif image == 'zwaarbewolkt':
    image= 10
  elif image == 'nachtmist':
    image= 11
  elif image == 'helderenacht':
    image= 12
  elif image == 'wolkennacht':
    image= 13
  else:
    image= 0
    print('Unknown! ->:', image)
  return str(image)


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
    summary= rwl['liveweer'][0]['samenv'] #summary: str
    summary= convert_summary(summary) #convert to integer
    image= rwl['liveweer'][0]['image'] #image: str
    image= convert_image(image) #convert to integer
    d_t= tijd()
    timestamp= int(time.time())
    timestamp= str(timestamp)
    update= d_t+', '+timestamp+', '+temp+', '+wind_dir+', '+wind_kmh+', '+humid+', '+press+', '+summary+', '+image
    print(update)
    
    fileobj= open('/home/pi/johns_wind/records.txt', 'a')
    fileobj.write(update)
    fileobj.write("\n")
    fileobj.close
  
  except requests.ConnectionError:
    print("Error querying WeerLive API")

#peil()

while True:
  peil()
  time.sleep(600)

