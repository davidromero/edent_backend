import logging

from chalice import Chalice, Cron
from chalicelib import custom_responses, calendar_api
from chalicelib.config import CALENDAR_ID

app = Chalice(app_name='calendar-scheduler')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
_DB = None


@app.schedule(Cron(0, 0, '*', '*', '?', '*'))
def get_all_appointments():
    appointment_list = calendar_api.get_next_events(CALENDAR_ID)
    logger.info(custom_responses.get_appointments_list(appointment_list))

