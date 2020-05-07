import json

# http://www.copypastemap.com/

json_file = open("streetlight-json.json", "r")
streetlights = json.load(json_file)

output_file = open("streetlight-txt.txt", "w")

ctr = 1
for streetlight_id in streetlights:
    streetlight = streetlights[streetlight_id]

    if streetlight['road'] == "Torrey Pines Road":

        latitude = streetlight['latitude']
        longitude = streetlight['longitude']

        output_file.write(latitude + "\t" + longitude + "\t" + "dot1" + "\t" + "blue" + "\t" + str(ctr) + "\t" + streetlight_id +"\n")

    ctr += 1

json_file.close()
output_file.close()