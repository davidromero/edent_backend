import json

import requests
from chalice import Chalice, Cron
from chalicelib import custom_responses, calendar_api
from chalicelib.config import CALENDAR_ID
import logging

app = Chalice(app_name='calendar-scheduler')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


@app.schedule(Cron(0, 6, '*', '*', '?', '*'))
def get_all_appointments(event):
    appointment_list = calendar_api.get_next_events(CALENDAR_ID)
    response = custom_responses.get_appointments_list(appointment_list)
    if response['status'] == 200:
        for appointment in response['body']:
            logging.info('Posting ' + json.dumps(appointment))
            response = requests.post('https://5ticjo0pz9.execute-api.us-east-1.amazonaws.com/api/appointments/',
                                    json=appointment)
            logging.info(response.text)
