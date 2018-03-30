# beaufort1
# based in part on Radomir Dopieralski's workshop: HTTP requests

import json, urequests
import machine, neopixel, time

np = neopixel.NeoPixel(machine.Pin(15), 16)
winddir = ''
windbeau = ''

 # First get the appropriate color...
def beaucolor(windbeau): #get beaufort color based on windspeed
    if windbeau == '0': # off
        beaucolor = (0, 0, 0)
        return beaucolor
    elif windbeau == '1': # beaufort-1 white
        beaucolor = (16, 16, 16)
        return beaucolor
    elif windbeau == '2': # beaufort-2 blue
        beaucolor = (0, 0, 16)
        return beaucolor
    elif windbeau == '3': # beaufort-3 blue-green
        beaucolor = (0, 32, 16)
        return beaucolor
    elif windbeau == '4': # beaufort-4 green
        beaucolor = (0, 16, 0)
        return beaucolor
    elif windbeau == '5': # beaufort-5 yellow
        beaucolor = (32, 16, 0)
        return beaucolor
    elif windbeau == '6': # beaufort-6 orange
        beaucolor = (48, 8, 0)
        return beaucolor
    elif windbeau == '7': # beaufort-7 mauve
        beaucolor = (16, 0, 16)
        return beaucolor
    elif windbeau == '8': # beaufort-8 red
        beaucolor = (16, 0, 0)
        return beaucolor

# Then set the appropriate neopixel with the correct color
def setdirection(winddir): # clear all then set neopixel according to wind direction
    #global winddir, windbeau
    for i in range(16): # clear all neopixels
        np[i] = (0, 0, 0)
        np.write()
    if winddir == 'Noord': # North (N)
        np[0] = beaucolor(windbeau)
    elif winddir == 'NNO': # North-northeast (NNE)
        np[15] = beaucolor(windbeau)
    elif winddir == 'NO': # Northeast (NE)
        np[14] = beaucolor(windbeau)
    elif winddir == 'ONO': #East-northeast (ENE)
        np[13] = beaucolor(windbeau)
    elif winddir == 'Oost': # East (E)
        np[12] = beaucolor(windbeau)
    elif winddir == 'OZO': # East-southeast (ESE)
        np[11] = beaucolor(windbeau)
    elif winddir == 'ZO': # Southeast (SE)
        np[10] = beaucolor(windbeau)
    elif winddir == 'ZZO': # South-southeast (SSE)
        np[9] = beaucolor(windbeau)
    elif winddir == 'Zuid': # South (S)
        np[8] = beaucolor(windbeau)
    elif winddir == 'ZZW': # South-southwest (SSW)
        np[7] = beaucolor(windbeau)
    elif winddir == 'ZW': # Southwest (SW)
        np[6] = beaucolor(windbeau)
    elif winddir == 'WZW': # West-southwest (WSW)
        np[5] = beaucolor(windbeau)
    elif winddir == 'West': # West (W)
        np[4] = beaucolor(windbeau)
    elif winddir == 'WNW': # West-northwest (WNW)
        np[3] = beaucolor(windbeau)
    elif winddir == 'NW': # Northwest (NW)
        np[2] = beaucolor(windbeau)
    elif winddir == 'NNW': # North-northwest (NNW)
        np[1] = beaucolor(windbeau)
    else:
        print('No wind direction')


def peil(): # get winddir (windr) and windbeau (winds)
    global winddir, windbeau
    # r is a response object
    r = urequests.get("http://weerlive.nl/api/json-10min.php?locatie=Rotterdam")
    data = r.json() # data is a dict
    r.close() # important: close response object
    winddir = data['liveweer'][0]['windr'] # winddir is a string
    windbeau = data['liveweer'][0]['winds'] # windbeau is a string
    print('Direction: ' + winddir + ' Beafort: ' + windbeau) # test code
    print(beaucolor(windbeau))

while True:
    peil()
    setdirection(winddir)
    np.write()
    time.sleep(600)
