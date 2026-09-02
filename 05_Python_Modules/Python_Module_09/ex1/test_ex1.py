import json
from alien_contact import ContactType, AlienContact

with open('../data_generator/generated_data/alien_contacts.json') as f:
    data = json.load(f)

for item in data:
    try:
        s = AlienContact.model_validate(item)
        print('SUCCESS:', s.contact_id)

    except Exception as e:
        print('FAIL:', item.get('contact_id'), '->', e)