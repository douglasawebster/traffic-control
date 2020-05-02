from geopy.geocoders import Nominatim  # Provided by https://geopy.readthedocs.io/en/stable/
import json
import csv
import re

geolocator = Nominatim(timeout=30)

json_file = open("streetlight-json.json", "r")
streetlights = json.load(json_file)

#streetlights = {}

num_checked = 37510
ctr = 0

max_latitude_north = 32.889147
min_latitude_south = 32.802140
max_longitude_west = -117.289555
min_longitude_east = -117.235660

la_jolla_postcode = "92037"

with open("streetlight-locations.csv") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')

    for row_data in reader:
        '''
            row_data[0]: ID
            row_data[1]: Model
            row_data[2]: Type
            row_data[3]: Wattage
            row_data[4]: Voltage
            row_data[5]: Longitude
            row_data[6]: Latitude
            row_data[7]: Description
        '''
        if ctr == 0:  # Skip the header of the csv file
            ctr += 1
            continue

        if ctr > num_checked:
            latitude = float(row_data[6])
            longitude = float(row_data[5])

            # Pre-screen to make sure coordinates are close to the desired area
            if ((latitude < max_latitude_north) and (latitude > min_latitude_south) and (longitude > max_longitude_west) and (longitude < min_longitude_east)):
                coordinate = str(latitude) + ", " + str(longitude)
                print(coordinate)
                try:
                    location = geolocator.reverse(coordinate)  # Query coordinates
                    location_raw = location.raw  # Extract data from query
                    address = location_raw['address']
                    postal_code = address['postcode']
                    road = address['road']

                    # Make sure streetlight is in La Jolla
                    if postal_code == la_jolla_postcode:
                        streetlights[row_data[0]] = {
                            "model": row_data[1],
                            "type": row_data[2],
                            "wattage": row_data[3],
                            "voltage": row_data[4],
                            "longitude": row_data[5],
                            "latitude": row_data[6],
                            "description": row_data[7],
                            "road": road
                        }
                except:
                    # If connection is lost to geopy notify with the last successful query
                    print("Last successful iteration: ", ctr - 1)
                    break

        print("Iteration: " + str(ctr))
        ctr += 1

# Write dictionary to json
with open('streetlight-json.json', 'w') as fp:
    json.dump(streetlights, fp)

json_file.close()
fp.close()
