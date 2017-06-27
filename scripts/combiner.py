import json
import csv
import dbm

with open('data/parcels.json', 'r') as json_file:
    json_data = json.load(json_file)

    with open('data/fm-parcels.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file, ['case', 'parcel'])
        for row in reader:
            for obj in json_data['FORECLOSURES']:
                case_number = obj['CASENUM'].replace(" ", "")
                if row['case'] == case_number:
                    parcels = obj.get('PARCEL')
                    if parcels is None:
                        obj['PARCEL'] = [row['parcel']]

    db = dbm.open('centroids.dbm', 'r')
    for obj in json_data['FORECLOSURES']:
        obj['locations'] = {}
        parcels = obj.get('PARCEL')
        if parcels:
            for parcel in parcels:
                print(parcel)
                stripped_parcel = parcel.replace(" ", "")
                try:
                    latlon = db[stripped_parcel]
                    if latlon:
                        latlon = latlon.split()
                        obj['locations'][parcel] = latlon
                except Exception as e:
                    print(parcel, e)

    with open('data/outparcels.json', 'w') as out_file:
        json.dump(json_data, out_file, indent=4)
