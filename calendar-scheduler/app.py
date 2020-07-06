from chalice import Chalice, Cron
from chalicelib import custom_responses, calendar_api
from chalicelib.config import CALENDAR_ID

app = Chalice(app_name='calendar-scheduler')


@app.schedule(Cron(6, 0, '*', '*', '?', '*'))
def get_all_appointments(event):
    appointment_list = calendar_api.get_next_events(CALENDAR_ID)
    response = custom_responses.get_appointments_list(appointment_list)
