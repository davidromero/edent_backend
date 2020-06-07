from __future__ import print_function
import datetime
import json
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


def create_event(event_details):
    creds = get_google_creds()
    service = build('calendar', 'v3', credentials=creds)
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
