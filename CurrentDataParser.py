'''
FlightRadar24 data grabbing code intended to output a KML file with an animation of air traffic.
This is the first code that downloads and parses the data.
Creates a new file and appends new data based on a defined interval.
Data output is prepared for final parsing to a KML file.
Optionally, creates a file with the raw data.
Allows data filtering based on min/max latitude and longitude.
Default url set to the 'Poland' zone.
'''

import time
from urllib import request
from datetime import datetime
import re

cycleDelay = 120 #delay between data downloads in seconds
numberOfCycles = 30 #number of data downloads
#filter the data by Latitude and Longitude
minLat = 47.5
maxLat = 51.0
minLon = 15.0
maxLon = 20.5
createRAWfile = False #True/False

url = 'http://lhr.data.fr24.com/zones/fcgi/poland.json'
#url = 'http://krk.data.fr24.com/zones/fcgi/poland.json'
#url = 'http://bma.data.fr24.com/zones/fcgi/poland.json'
#url = 'http://arn.data.fr24.com/zones/fcgi/poland.json' #section of the world 'Poland' should be within the 1500 limit
#url = 'http://krk.fr24.com/zones/fcgi/full_all.json' #the url returns max 1500 aiplanes, however there might by 10000+ overall

rawDataPrepared = ''

def download_data(urlTXT, file):
    global rawDataPrepared
    response = request.urlopen(urlTXT)
    txt = response.read()
    txt_str = str(txt)
    lines = txt_str.split('\\n')
    if createRAWfile:
        frr = open(file, 'a')
        frr.write(datetime.now().strftime('<when>%Y-%m-%dT%H:%M:%SZ</when>') + '\n')
        for line in lines:
            frr.write(line + '\n')
        frr.close()
    x = 0
    for i in txt_str:
        x += 1
        if i == ',':
            break
    txt_str = txt_str[x:]
    x = 0
    for i in txt_str:
        if i == ',':
            break
        x += 1
    txt_str = txt_str[x:]
    lines = txt_str.split('\\n')
    for line in lines:
        subOBJ = re.sub('(\"|\[|\]|\}|\')', "", line)
        if subOBJ:
            rawDataPrepared = rawDataPrepared + subOBJ + '\n'

def parse_data(file):
    global rawDataPrepared
    lines = rawDataPrepared
    rawDataPrepared = ''
    strOut = ''
    for line in lines:
        substOBJ = re.sub(',', ",,", line)
        strOut = strOut + substOBJ
    strOut2 = ''
    for line in strOut:
        substOBJ2 = re.sub(':', ',,', line)
        strOut2 = strOut2 + substOBJ2
    strOut3 = ''
    strOut3 = strOut2.split('\n')
    strOut4 = ''
    for line in strOut3:
        substOBJ3 = re.search('$', line, re.M)
        strOut4 = strOut4 + line[1:] + ',\n'
    listOut = strOut4.split('\n')
    fr = open(file, 'a')
    for line in listOut:
        findallOBJ = re.findall(r',(.*?),', line)
        if findallOBJ:
            latitude = float(findallOBJ[2])
            longitude = float(findallOBJ[3])
            altitude = int(float(findallOBJ[5]) * 0.3048)
            if latitude >= minLat and latitude <= maxLat and longitude >= minLon and longitude <= maxLon:
                #print(findallOBJ[0] + datetime.now().strftime(';<when>%Y-%m-%dT%H:%M:%SZ</when>') + ';<gx:coord>' + findallOBJ[3] + ' ' + findallOBJ[2] + ' ' + str(altitude) + '</gx:coord>')
                fr.write(findallOBJ[0] + datetime.now().strftime(';<when>%Y-%m-%dT%H:%M:%SZ</when>') + ';<gx:coord>' + findallOBJ[3] + ' ' + findallOBJ[2] + ' ' + str(altitude) + '</gx:coord>' + '\n')
    fr.close()


fileName = 'fr24 ' + str(datetime.now().strftime('%Y%m%d%H%M%S')) + '.txt'
fr = open(fileName, 'w')
fr.close()

fileNameRaw = 'fr24raw ' + str(datetime.now().strftime('%Y%m%d%H%M%S')) + '.txt'
if createRAWfile:
    frr = open(fileNameRaw, 'w')
    frr.close()


print('Cycles to do: ' + str(numberOfCycles))
print('Delay between cycles: ' + str(cycleDelay))

i = 0

while i < numberOfCycles:
    download_data(url, fileNameRaw)
    parse_data(fileName)
    i += 1
    print('Cycle number ' + str(i) + ' done at ' + str(datetime.now().strftime('%H:%M:%S')))
    if i == numberOfCycles:
        break
    time.sleep(cycleDelay)
