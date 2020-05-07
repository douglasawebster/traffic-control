import json

json_file = open("streetlight-json.json", "r")
streetlights = json.load(json_file)

street_names = {}

for streetlight_id in streetlights:
    streetlight = streetlights[streetlight_id]
    road = streetlight['road']

    if street_names.get(road) is None:
        street_names[road] = 0
    else:
        street_names[road] = street_names[road] + 1

with open('street-names.json', 'w') as fp:
    json.dump(street_names, fp)

json_file.close()
fp.close()