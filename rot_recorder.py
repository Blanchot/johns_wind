#!/usr/bin/python3

'''15 April 2019: Rotterdam Weather Recorder to run on Diana
17 April 2019: Added summary and image (icon) recording and conversion
24 April 2019: Added alarm field (curious how this is represented)
02 May 2019: Wrote some code to write a line to records.txt in case of connection or json error and refactored code

Currently recording 10 fields saved as 11 comma separated values: 
date&time, timestamp, temp, wind_dir (saved as dir and numeric bearing), wind_kmh, humidity, pressure, summary, image, alarm
at 10 minute intervals and storing these in a csv file

Info over the weerlive API: http://weerlive.nl/delen.php
Requires: records.txt in the same folder
'''

import requests, json
import datetime
import time

#--------------------------------------------- HELPER FUNCTIONS
def tijd() -> tuple:
  '''returns a 2-tuple: local datetime + timestamp, both as strings'''
  timestamp= int(time.time())
  curr_dt= datetime.datetime.fromtimestamp(timestamp)
  curr_dt= curr_dt.strftime('%d-%m %H:%M')
  timestamp= str(timestamp)
  return (curr_dt, timestamp)


def write_file(update: str):
  '''writes to update to file using with context manager. 
  Eventually write code here to create new file each 35 days'''
  with open('/home/pi/johns_wind/records.txt', 'a') as fileobj:
  #with open('records.txt', 'a') as fileobj: #for testing
    fileobj.write(update)
    fileobj.write("\n")


def write_alarm(alarm_record: str):
  '''writes eventual alarm messages to file using with context manager'''
  with open('/home/pi/johns_wind/alarms.txt', 'a') as fileobj:
    fileobj.write(alarm_record)
    fileobj.write("\n")


#--------------------------------------------- CONVERSION FUNCTIONS
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
  if summary == 'Onbewolkt':
    summary= 1
  elif summary == 'Licht bewolkt':
    summary= 2
  elif summary == 'Half bewolkt':
    summary= 3
  elif summary == 'Geheel bewolkt':
    summary= 4
  elif summary == 'Zwaar bewolkt':
    summary= 5
  elif summary == 'Motregen':
    summary= 6
  elif summary == 'Lichte motregen':
    summary= 7
  elif summary == 'Dichte motregen':
    summary= 8
  elif summary == 'Lichte motregen en regen':
    summary= 9
  elif summary == 'Droog na motregen':
    summary= 10
  elif summary == 'Motregen en regen':
    summary= 11
  elif summary == 'Af en toe lichte regen':
    summary= 12
  elif summary == 'Lichte regen':
    summary= 13
  elif summary == 'Regen':
    summary= 14
  elif summary == 'Droog na regen':
    summary= 15
  else:
    print('Unknown! ->:', summary)
    summary= 0
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
    print('Unknown! ->:', image)
    image= 0
  return str(image)


#--------------------------------------------- MAIN FUNCTION
def peil():
  '''Main loop'''
  weerlive = "http://weerlive.nl/api/json-10min.php?locatie=Rotterdam"
  try:
    rwl= requests.get(weerlive).json() #rwl is dictionary object
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
    alarm= rwl['liveweer'][0]['alarm']
    
    curr_dt, timestamp= tijd()
    update= curr_dt+', '+timestamp+', '+temp+', '+wind_dir+', '+wind_kmh+', '+humid+', '+press+', '+summary+', '+image+', '+ alarm
    
    print(update)
    write_file(update)
    
    if int(alarm):
      alarm_txt= rwl['liveweer'][0]['alarmtxt'] #alarm text if alarm
      curr_dt, timestamp= tijd()
      alarm_record= curr_dt+', '+timestamp+', '+ alarm_txt
      write_alarm(alarm_record)
      
      
  except requests.ConnectionError:
    '''In case of error still write a line and use '17'' in image column to indicate lack of data'''
    print("Error querying WeerLive API")
    curr_dt, timestamp= tijd()
    blank= '_'
    update= curr_dt+ ', ' +timestamp+ ', ' +blank+ ', ' +blank+ ', ' +blank+ ', ' +blank+ ', ' +blank+ ', ' +blank+ ', ' +'17'+ ', ' +blank
    
    print(update)
    write_file(update)
  
  except json.decoder.JSONDecodeError:
    '''In case of error still write a line and use '17'' in image column to indicate lack of data'''
    print('JSON Error: Expecting value received None')
    curr_dt, timestamp= tijd()
    blank= '_'
    update= curr_dt+ ', ' +timestamp+ ', ' +blank+ ', ' +blank+ ', ' +blank+ ', ' +blank+ ', ' +blank+ ', ' +blank+ ', ' +'17'+ ', ' +blank
    
    print(update)
    write_file(update)


#peil() #for testing

while True:
  peil()
  time.sleep(600)


'''
JSONDecodeError NOTES:
raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
'''
