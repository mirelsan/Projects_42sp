import json
from space_station import SpaceStation

with open('../data_generator/generated_data/space_stations.json') as f:
    data = json.load(f)

for item in data:
    try:
        s = SpaceStation.model_validate(item)
        print('SUCCESS:', s.station_id)

    except Exception as e:
        print('FAIL:', item.get('station_id'), '->', e)