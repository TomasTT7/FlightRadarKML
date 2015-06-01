'''
KML animation file constructor.
Uses the data output of 'CurrentDataParser.py'.
'''
# -*- coding: utf-8 -*-

import re

#Enter the name of the source file with the parsed data.
inputFile = 'fr24 20150601111413.txt'

fs = open(inputFile, 'r')
inputFileText = fs.read()
fs.close()

whenList = re.findall(r"<when>(.*)</when>", inputFileText)

dateAndTime = inputFile[5:19]
fileName = 'Air Traffic ' + inputFile[5:19] + '.kml'
animStart = inputFile[5:9] + '-' + inputFile[9:11] + '-' + inputFile[11:13] + 'T' + inputFile[13:15] + ':' + inputFile[15:17] + ':' + inputFile[17:19] + 'Z'
animEnd = whenList[-1]
animLon = inputFileText[52:59]
animLat = inputFileText[60:67]
animAlt = '5000'
animRange = '500000'
animTilt = '45'

kmlStringHeader = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2">
  <Document>
    <name>Air Traffic {dateTime}</name>
    <LookAt>
      <gx:TimeSpan>
        <begin>{start}</begin>
        <end>{end}</end>
      </gx:TimeSpan>
      <longitude>{lon}</longitude>
      <latitude>{lat}</latitude>
      <altitude>{alt}</altitude>
      <range>{range}</range>
      <tilt>{tilt}</tilt>
    </LookAt>
    <Style id="multiTrack_n">
      <IconStyle>
        <scale>0.6</scale>
        <Icon>
          <href>http://maps.google.com/mapfiles/kml/pal2/icon56.png</href>
        </Icon>
      </IconStyle>
      <LineStyle>
        <color>99ff0000</color>
        <width>1</width>
      </LineStyle>
      <LabelStyle>
        <scale>0</scale>
      </LabelStyle>
    </Style>
    <Style id="multiTrack_h">
      <IconStyle>
        <scale>1.0</scale>
        <Icon>
          <href>http://maps.google.com/mapfiles/kml/pal2/icon56.png</href>
        </Icon>
      </IconStyle>
      <LineStyle>
        <color>99ff0000</color>
        <width>2</width>
      </LineStyle>
      <LabelStyle>
        <scale>0.6</scale>
      </LabelStyle>
    </Style>
    <StyleMap id="multiTrack">
      <Pair>
        <key>normal</key>
        <styleUrl>#multiTrack_n</styleUrl>
      </Pair>
      <Pair>
        <key>highlight</key>
        <styleUrl>#multiTrack_h</styleUrl>
      </Pair>
    </StyleMap>
    <Folder>
      <name>Tracks</name>""".format(dateTime = dateAndTime, start = animStart, alt=animAlt, range=animRange, tilt=animTilt, lat=animLat, lon=animLon, end=animEnd)

kmlStringEnd = """
    </Folder>
  </Document>
</kml>"""

kmlPlacemarkHeader1 = """
        <Placemark>"""

kmlPlacemarkHeader2 = """
          <styleUrl>#multiTrack</styleUrl>
          <gx:Track>
          <gx:altitudeMode>absolute</gx:altitudeMode>"""

kmlPlacemarkEnd = """
          </gx:Track>
        </Placemark>"""


inputFileList = inputFileText.split('\n')
inputFileList.sort()
inputFileStr = '\n'.join(inputFileList)
inputFileText2 = ''
for i in inputFileStr:
  subOBJ = re.sub(';', '\n', i)
  inputFileText2 = inputFileText2 + subOBJ
inputFileListAll = inputFileText2.split('\n')
inputFileListAll.remove('')
kmlPlacemarkBody = ''
currentPlane = inputFileListAll[0]
first = True
for i in inputFileListAll:
  if first:
    kmlPlacemarkBody = kmlPlacemarkBody + """
        <Placemark>
          <name>{name}</name>
          <styleUrl>#multiTrack</styleUrl>
          <gx:Track>
          <gx:altitudeMode>absolute</gx:altitudeMode>""".format(name=i)
    first = False
    continue
  if '<when>' in i:
    kmlPlacemarkBody = kmlPlacemarkBody + """
            {when}""".format(when=i)
  elif '<gx:coord>' in i:
    kmlPlacemarkBody = kmlPlacemarkBody + """
            {coord}""".format(coord=i)
  else:
    if i != currentPlane:
      kmlPlacemarkBody = kmlPlacemarkBody + """
          </gx:Track>
        </Placemark>
        <Placemark>
          <name>{name}</name>
          <styleUrl>#multiTrack</styleUrl>
          <gx:Track>
          <gx:altitudeMode>absolute</gx:altitudeMode>""".format(name=i)
      currentPlane = i

kmlPlacemarkBody = kmlPlacemarkBody + """
          </gx:Track>
        </Placemark>"""

fk = open(fileName, 'w')
fk.write(kmlStringHeader)
fk.write(kmlPlacemarkBody)
fk.write(kmlStringEnd)
fk.close()
