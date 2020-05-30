from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import logging


SCOPES = ['https://www.googleapis.com/auth/calendar']
logging.basicConfig()
logger = logging.getLogger(__name__)


def get_google_creds():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './chalicelib/credentials/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


def get_next_events(max_items, calendar):
    creds = get_google_creds()
    service = build('calendar', 'v3', credentials=creds)

    now = datetime.datetime.utcnow().isoformat() + 'Z'
    logger.debug(f'Getting the upcoming {max_items} events')
    events_result = service.events().list(calendarId=calendar, timeMin=now,
                                          maxResults=max_items, singleEvents=True,
                                          orderBy='startTime').execute()
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