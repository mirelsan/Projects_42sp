import json
from space_crew import Rank, CrewMember, SpaceMission

with open('../data_generator/generated_data/space_missions.json') as f:
    data = json.load(f)

for item in data:
    try:
        s = SpaceMission.model_validate(item)
        print('SUCCESS:', s.mission_id)
    except Exception as e:
        print('FAIL:', item.get('mission_id'), '->', e)