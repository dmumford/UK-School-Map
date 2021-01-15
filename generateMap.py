# TODO
# 1. Optimise code
# 2. Find a way to get lat/lon of failed Map markers
# 3. Cluster Map Markers
# 4. Add custom Map Marker icon

# required imports/dependencies
import os
import time
import folium
import mysql
import mysql.connector
from functools import partial
from geopy.geocoders import Nominatim

startTime = time.time()

# Specify path of generated map file
mapOutputPath = r'/Users/david/Documents/python scripts/map/map.html'
# Specify path of failed Map marker txt file
failedMarkersTxtFile = '/Users/david/Documents/python scripts/map/\
    failed_markers.txt'

# SQL limit
SqlLimit = "500"


# class to support printing to terminal in colour
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# mysql db credentials
db = mysql.connector.connect(host="localhost",
                             user="demo_user",
                             passwd="my_password",
                             database="uk_schools",
                             port=8889)

# check if connection to db is successful
if (db):
    print("Connected to Database.")

else:
    print(bcolors.FAIL + "Connection to Database Failed!" + bcolors.ENDC)

cursor = db.cursor()

# SQL Query (LIMIT used for testing only)
cursor.execute(
    "SELECT `school`, `addr1`, `addr2`, `town`, `county`, `postcode`, `country`, \
        `id` from `uk_schools_overview` LIMIT " + SqlLimit)
result = list(cursor.fetchall())
if result:
    print("Data retrieved from MySQL")
else:
    print(bcolors.FAIL + "Failed to retrieve data from MySQL" + bcolors.ENDC)
cursor.close()

db.close()
print("Database Connection Closed.")

geolocator = Nominatim(user_agent="Dave")
geocode = partial(geolocator.geocode, language="en")

# define map
m = folium.Map(
    location=[53.5438234, -2.1761227],  # longlat of centre of UK
    zoom_start=6,
    tiles="OpenStreetMap")

# variables used for tracking if Map Marker status
markerSuccess = 0
markerFail = 0

failedMarkers = []

# loop through SQL rows
for data in result:
    # school (mysql col)
    name = data[0]
    print("Constructing Map Marker for: " + name)

    addressOne = data[1]
    addressTwo = data[2]
    town = data[3]
    county = data[4]
    pcode = data[5]
    country = data[6]
    rowId = data[7]

    # change <blank> values to empty string
    def blankToEmptyString(inputArray: list) -> str:
        for x in inputArray:
            if x == "<blank>":
                print(bcolors.OKCYAN + x +
                      " field(s) changed to empty string" + bcolors.ENDC)
            x = ""

    blankToEmptyString(
        [name, addressOne, addressTwo, town, county, pcode, country])

    # construct address (town + county + UK)
    address = name + " " + addressOne + " " + pcode

    # get long/lat from address
    longLat = geolocator.geocode(address)

    # if unable to get long/lat
    if longLat is None:

        print(bcolors.FAIL + rowId + ">> Map Marker Failed to initialise (" +
              name + ")" + bcolors.ENDC)
        markerFail += 1

        failedMarkers.append(rowId)

    else:
        lon = longLat.longitude
        lat = longLat.latitude

        tooltipMeta = name

        folium.Marker(location=[lat, lon], tooltip=tooltipMeta).add_to(m)

        print(bcolors.OKGREEN + rowId + ">> Map Marker Created (" + name +
              ")" + bcolors.ENDC)
        markerSuccess += 1

# Print total Successful Map Markers
print("\n" + bcolors.OKGREEN + str(markerSuccess) + " Markers added\n" +
      bcolors.ENDC)

# Print total Failed Map Markers
print(bcolors.FAIL + str(markerFail) + " Markers failed to initialise" +
      bcolors.ENDC + "\n")

# Print percentage of Sucessful Map Markers
percentageSuccess = str(
    (markerSuccess % (markerSuccess + markerFail)) * 100) + "%"
print(bcolors.WARNING + percentageSuccess + " Schools Successfully added" +
      bcolors.ENDC)

# create text file and fill with failed map marker id's

# If text file already exists, delete
if os.path.exists(failedMarkersTxtFile):
    os.remove(failedMarkersTxtFile)
    print(bcolors.WARNING + "Deleted existing " + failedMarkersTxtFile +
          bcolors.ENDC)
with open(failedMarkersTxtFile, 'w') as txtFile:
    for marker in failedMarkers:
        txtFile.write("%s\n" % marker)

# If map file already exists, delete
if os.path.exists(mapOutputPath):
    os.remove(mapOutputPath)
    print(bcolors.WARNING + "Deleted existing " + mapOutputPath + bcolors.ENDC)

# Save it as html
# mapOutputPath = os.path.dirname(os.path.realpath(__file__)) + "/map.html"
m.save(mapOutputPath)

# check if new map file was saved
if os.path.exists(mapOutputPath):
    print(bcolors.OKGREEN + "\nSaved map > " + mapOutputPath + bcolors.ENDC)
else:
    print(bcolors.FAIL + "\nFailed to create " + mapOutputPath + bcolors.ENDC)

# Finally, Format and Print Script execution time
scriptExecutionTime = (time.time() - startTime)

hours, rem = divmod(time.time() - startTime, 3600)
minutes, seconds = divmod(rem, 60)
print(bcolors.BOLD +
      bcolors.OKCYAN + "\nTotal Time >> {:0>2}:{:0>2}:{:05.2f}".format(
          int(hours), int(minutes), seconds) + bcolors.ENDC + "\n")
