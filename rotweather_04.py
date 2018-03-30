# rotweather.py v.04 PYTHON CODE VERSION!
# v.04 adds a MUCH BETTER VERSION OF WINDREC WRITING DATA TO A JSON FILE
# v.03 adds windrecord
# v.02 changes to localtime adjustment (gave up on jsontest time)

import json
import requests
import time

# V.04 code
windrec = {'N':0,'NNE':0,'NE':0,'ENE':0,'E':0,'ESE':0,'SE':0,'SSE':0,
'S':0,'SSW':0,'SW':0,'WSW':0,'W':0,'WNW':0,'NW':0,'NNW':0}

def add(str):
    windrec[str] = windrec[str] + 1
    data = json.dumps(windrec)
    with open('windrec.json', 'w') as f:
        f.write(data)

# url for scraping local time
url = 'https://script.googleusercontent.com/macros/echo?user_content_key=MEzcBJ3yCveKGxvJTWQ7LdCTuapiMrYJ4Wv0EGRrJICy4-xTaaA1DZryCQsYC1RDfx_I0rU-LrjVUPL1Qy6tY0Kghj-zpX1Nm5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnJ9GRkcRevgjTvo8Dc32iw_BLJPcPfRdVKhJT5HNzQuXEeN3QFwl2n0M6ZmO-h7C6bwVq0tbM60-BPr12bi8gvU&lib=MwxUjRcLr2qLlnVOLh12wSNkqcO1Ikdrk'

def localtime():
    t = requests.get(url).json()
    h = str(t['hours']) # returned integer coerced to string
    m = str(t['minutes']) # returned integer coerced to string
    s = str(t['seconds']) # returned integer coerced to string
    # .zfill(2) pads the string-integers with a 0 if necessary
    currtime = h.zfill(2) + ':' + m.zfill(2) + ':' + s.zfill(2)
    return currtime

def peil():
    t = localtime()
    r = requests.get('http://weerlive.nl/api/json-10min.php?locatie=Rotterdam').json()
    temp = r['liveweer'][0]['temp']
    bar = r['liveweer'][0]['luchtd']
    relhum = r['liveweer'][0]['lv']
    winddir = r['liveweer'][0]['windr']
    windms = r['liveweer'][0]['windms']
    windbeau = r['liveweer'][0]['winds']
    windkmh = r['liveweer'][0]['windkmh']
    # Translate wind direction
    if winddir == 'Noord':
        winddir = 'North'
        add('N')
    elif winddir == 'NNO':
        winddir = 'North-northeast'
        add('NNE')
    elif winddir == 'NO':
        winddir = 'Northeast'
        add('NE')
    elif winddir == 'ONO':
        winddir = 'East-northeast'
        add('ENE')
    elif winddir == 'Oost':
        winddir = 'East'
        add('E')
    elif winddir == 'OZO':
        winddir = 'East-southeast'
        add('ESE')
    elif winddir == 'ZO':
        winddir = 'Southeast'
        add('SE')
    elif winddir == 'ZZO':
        winddir = 'South-southeast'
        add('SSE')
    elif winddir == 'Zuid':
        winddir = 'South'
        add('S')
    elif winddir == 'ZZW':
        winddir = 'South-southwest'
        add('SSW')
    elif winddir == 'ZW':
        winddir = 'Southwest'
        add('SW')
    elif winddir == 'WZW':
        winddir = 'West-southwest'
        add('WSW')
    elif winddir == 'West':
        winddir = 'West'
        add('W')
    elif winddir == 'WNW':
        winddir = 'West-northwest'
        add('WNW')
    elif winddir == 'NW':
        winddir = 'Northwest'
        add('NW')
    elif winddir == 'NNW':
        winddir = 'North-northwest'
        add('NNW')

    print(t + ' Temp: ' + temp + 'C, Bar: ' + bar + ', Hum: ' + relhum + '%')
    print(winddir + ' wind at ' + windms + ' m/sec (' + windbeau + ' Bft, ' + windkmh + ' km/hr)')

# executes peil() once ever 10 minutes
def peiling():
    while True:
        print('')
        peil()
        time.sleep(600)

peiling()
