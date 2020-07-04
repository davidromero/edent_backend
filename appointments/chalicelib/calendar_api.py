import logging
import os.path
import pickle
from datetime import datetime, timedelta

import httplib2
import pytz
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

SERVICE_ACCOUNT_FILE = 'chalicelib/credentials/edent-61d92-2e75249e0582.json'
PICKLE_FILE = 'chalicelib/credentials/token.pickle'
SCOPES = ['https://www.googleapis.com/auth/calendar']
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def use_gsuite_credentials():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    delegated_credentials = credentials.create_delegated('agatica@kaleidoscopic.dev')
    delegated_http = delegated_credentials.authorize(httplib2.Http())
    service = build('calendar', 'v3', cache_discovery=False, http=delegated_http)

    return service


def use_user_credentials():
    creds = None
    if os.path.exists(PICKLE_FILE):
        with open(PICKLE_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(PICKLE_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(PICKLE_FILE, 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds, cache_discovery=False)

    return service


def get_next_events(calendar):
    service = use_user_credentials()
    now = datetime.now(pytz.timezone('America/Guatemala')).replace(hour=0, minute=0)
    tomorrow = now + timedelta(days=1)
    logger.info(f'Retrieving events from {now.isoformat()}')
    events_result = service.events().list(calendarId=calendar, timeMin=now.isoformat(),
                                          timeMax=tomorrow.isoformat(), singleEvents=True,
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
