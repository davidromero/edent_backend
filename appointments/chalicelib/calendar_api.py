import datetime
import logging
import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

SERVICE_ACCOUNT_FILE = 'chalicelib/credentials/edent-61d92-2e75249e0582.json'
SCOPES = ['https://www.googleapis.com/auth/calendar']
logging.basicConfig()
logger = logging.getLogger(__name__)


def get_google_calendar_service():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    delegated_credentials = credentials.create_delegated('agatica@kaleido.page')
    delegated_http = delegated_credentials.authorize(httplib2.Http())
    service = build('calendar', 'v3', cache_discovery=False, http=delegated_http)

    return service


def get_next_events(max_items, calendar):
    service = get_google_calendar_service()

    now = datetime.datetime.utcnow().isoformat() + 'Z'
    print(f'Getting the upcoming {max_items} events')
    events_result = service.events().list(calendarId='primary').execute()
    events = events_result.get('items', [])
    if not events:
        logger.debug('No upcoming events found.')
        return None
    else:
        return make_response(events)


def make_response(event_list):
    appointments = []
    for event in event_list:
        appointment = {
            'id': event['id'],
            'link': event['htmlLink'],
            'title': event['summary'],
            'start': event['start'],
            'end': event['end'],
        }
        appointments.append(appointment)
    return appointments


def create_event(event_details):
    service = get_google_calendar_service()
    start_time = datetime.datetime.strptime(event_details['start_time'], '%Y-%m-%dT%H:%M:%S')
    end_time = start_time + datetime.timedelta(minutes=int(event_details['duration']))
    summary = f'{event_details["first_name"]} {event_details["last_name"]}'
    description = f'{event_details["treatment_name"]}.\n {event_details["clinic_location"]}'
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': event_details['start_time'],
            'timeZone': 'America/Guatemala',
        },
        'end': {
            'dateTime': end_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'America/Guatemala',
        }
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    print(event)
    return event.get('htmlLink')
