# FlightRadarKML
FlightRadar24 data downloader and parser with a KML animation constructor.

CurrentDataParser.py periodically accesses FlightRadar24 servers, downloads the current data and parses it to a .txt file.
AnimationConstructor.py opens the predefined .txt file and creates a .kml file containing an animation of the air traffic for Google Earth.
