import logging

from chalice import Chalice
from chalicelib import custom_responses, calendar_api
from chalicelib.config import CALENDAR_ID

app = Chalice(app_name='appointments')
app.log.setLevel(logging.DEBUG)
_DB = None


@app.route('/appointments', methods=['GET'])
def get_all_appointments():
    appointment_list = calendar_api.get_next_events(CALENDAR_ID)
    return custom_responses.get_appointments_list(appointment_list)
