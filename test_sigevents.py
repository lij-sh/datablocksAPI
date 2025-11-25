import datablockAPI as api
from datablockAPI.core.models import SignificantEvent, SignificantEventTextEntry

api.init(database='sqlite:///test_sigevents.db', echo=False)
api.load('Material/eventsfilings.json')
session = api.get_session()

sig_count = session.query(SignificantEvent).count()
text_count = session.query(SignificantEventTextEntry).count()

print(f'Significant events loaded: {sig_count}')
print(f'Text entries loaded: {text_count}')

if sig_count > 0:
    first_event = session.query(SignificantEvent).first()
    print(f'\nFirst event: {first_event.event_type_description} on {first_event.event_date}')

api.close()
