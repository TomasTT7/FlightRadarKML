'''
FlightRadar24 data grabbing code intended to output a KML file with an animation of air traffic.
Creates a new file and appends new data based on a defined interval.
Data output is prepared for final parsing to a KML file.
Additionally, creates a file with the raw data.
Allows data filtering based on min/max latitude and longitude.
'''

#v1.1
#time data points for each airplane separately match with coordinates now (previously one time data point for one data cycle)
#Google Earth automatically moves all animations 2 hours to the future (some settings of my instance?)

import time
from urllib import request
from datetime import datetime
import re

numberOfCycles = 25 #number of data downloads
stepBetweenCycles = 300 #seconds between two data time stamps
playbackStart = '06/04/2015 09:00:01' #'%m/%d/%Y %H:%M:%S' UTC+2
#set Latitude and Longitude area
minLat = 47.5
maxLat = 51.0
minLon = 15.0
maxLon = 20.5
createRAWfile = False #True/False

timestamp = time.mktime(datetime.strptime(playbackStart, '%m/%d/%Y %H:%M:%S').timetuple())
coords = str(maxLat) + ',' + str(minLat) + ',' + str(minLon) + ',' + str(maxLon)

url = 'http://krk.data.fr24.com/zones/fcgi/feed.js?bounds={coord}&faa=1&mlat=1&flarm=1&adsb=1&gnd=1&air=1&vehicles=1&estimated=1&maxage=900&gliders=1&stats=1&history={start}'.format(coord=coords, start=int(timestamp))
#url = 'http://krk.data.fr24.com/zones/fcgi/feed.js?bounds={coord}&faa=1&mlat=1&flarm=1&adsb=1&gnd=1&air=1&vehicles=1&estimated=1&maxage=900&gliders=1&stats=1&history={start}&&callback=fetch_playback_cb&_=1433285486945'.format(coord=coords, start=playbackStart)

rawDataPrepared = ''

def download_data(urlTXT, file, timestampIn):
    global rawDataPrepared
    global timestamp
    response = request.urlopen(urlTXT)
    txt = response.read()
    txt_str = str(txt)
    lines = txt_str.split('\\n')
    if createRAWfile:
        frr = open(file, 'a')
        frr.write(datetime.fromtimestamp(timestampIn).strftime('<when>%Y-%m-%dT%H:%M:%SZ</when>') + '\n')
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
    interimData = ''
    for line in lines:
        subOBJ = re.sub('(\"|\[|\]|\}|\')', "", line)
        if subOBJ:
            interimData = interimData + subOBJ + '\n'
    interimData2 = interimData.split('\n')
    for x in range(len(interimData2) - 2):
        rawDataPrepared = rawDataPrepared + interimData2[x] + '\n'

def parse_data(file, timestampIn):
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
                #print(findallOBJ[0] + datetime.fromtimestamp(int(findallOBJ[11])).strftime(';<when>%Y-%m-%dT%H:%M:%SZ</when>') + ';<gx:coord>' + findallOBJ[3] + ' ' + findallOBJ[2] + ' ' + str(altitude) + '</gx:coord>' + '\n')
                fr.write(findallOBJ[0] + datetime.fromtimestamp(int(findallOBJ[11])).strftime(';<when>%Y-%m-%dT%H:%M:%SZ</when>') + ';<gx:coord>' + findallOBJ[3] + ' ' + findallOBJ[2] + ' ' + str(altitude) + '</gx:coord>' + '\n')
    fr.close()


ts = datetime.fromtimestamp(timestamp).strftime('%Y%m%d%H%M%S')
fileName = 'fr24 ' + ts + '.txt'
fr = open(fileName, 'w')
fr.close()

fileNameRaw = 'fr24raw ' + ts + '.txt'
if createRAWfile:
    frr = open(fileNameRaw, 'w')
    frr.close()

i = 0

while i < numberOfCycles:
    download_data(url, fileNameRaw, timestamp)
    parse_data(fileName, timestamp)
    timestamp += stepBetweenCycles
    url = 'http://krk.data.fr24.com/zones/fcgi/feed.js?bounds={coord}&faa=1&mlat=1&flarm=1&adsb=1&gnd=1&air=1&vehicles=1&estimated=1&maxage=900&gliders=1&stats=1&history={start}'.format(coord=coords, start=int(timestamp))
    #url = 'http://krk.data.fr24.com/zones/fcgi/feed.js?bounds={coord}&faa=1&mlat=1&flarm=1&adsb=1&gnd=1&air=1&vehicles=1&estimated=1&maxage=900&gliders=1&stats=1&history={start}&&callback=fetch_playback_cb&_=1433285486945'.format(coord=coords, start=playbackStart)
    i += 1
    if i == (numberOfCycles):
        break
    print("Cycle number " + str(i) + ', please wait.')
    time.sleep(5)
