import datetime
import logging
import gflags
import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run_flow

SERVICE_ACCOUNT_FILE = './chalicelib/credentials/edent-61d92-388429d11137.json'
SCOPES = ['https://www.googleapis.com/auth/calendar.events']
logging.basicConfig()
logger = logging.getLogger(__name__)

# def main(argv):
    # Authenticate and construct service.

    # try:
    #     page_token = None
    #     while True:
    #         calendar_list = service.calendarList().list(
    #             pageToken=page_token).execute()
    #         for calendar_list_entry in calendar_list['items']:
    #             print(calendar_list_entry['summary'])
    #         page_token = calendar_list.get('nextPageToken')
    #         if not page_token:
    #             break
    #
    # except client.AccessTokenRefreshError:
    #     print('The credentials have been revoked or expired, please re-run'
    #           'the application to re-authorize.')


def get_google_calendar_service():
    # credentials = service_account.Credentials.from_service_account_file(
    #         './chalicelib/credentials/edent-61d92-388429d11137.json', scopes=SCOPES)
    # service = build('calendar', 'v3', credentials=credentials, cache_discovery=False)

    # service, flags = sample_tools.init(
    #     'something', 'calendar', 'v3', __doc__, SERVICE_ACCOUNT_FILE,scope='https://www.googleapis.com/auth/calendar.readonly')
    # print(service)

    # FLOW = OAuth2WebServerFlow(
    #     client_id='545442096199-onsf2bu26dmj47qndqh8m944b5dcper5.apps.googleusercontent.com',
    #     client_secret='bMViHy6SNU-Tu2E4gWvDrmIE',
    #     scope='https://www.googleapis.com/auth/calendar',
    #     user_agent='edent')

    http = httplib2.Http()
    service = build(serviceName='calendar', version='v3', http=http, cache_discovery=False,
                    developerKey='AIzaSyDRNJ3raowEpjparzPqTxCmp4tgUXbGSBQ')
    # storage = Storage('calendar.dat')
    # credentials = storage.get()
    # if credentials is None or credentials.invalid == True:
    #     credentials = run_flow(FLOW, storage)
    return service


def get_next_events(max_items, calendar):
    service = get_google_calendar_service()

    # try:
    #     page_token = None
    #     while True:
    #         calendar_list = service.calendarList().list(pageToken=page_token).execute()
    #         for calendar_list_entry in calendar_list['items']:
    #             print(calendar_list_entry['summary'])
    #         page_token = calendar_list.get('nextPageToken')
    #         if not page_token:
    #             break
    #
    # except client.AccessTokenRefreshError:
    #     print('The credentials have been revoked or expired, please re-run'
    #           'the application to re-authorize.')
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    print(f'Getting the upcoming {max_items} events')
    events_result = service.events().list(calendarId='aldogatica123@gmail.com').execute()
    # events = service.events().list(calendarId='<your_email_here>').execute()
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
    return event.get('htmlLink')
