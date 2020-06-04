import boto3 as boto3
import logging
from chalice import Chalice

from chalicelib import database, custom_responses, calendar_api
from chalicelib.config import RATES_TABLE_NAME, TABLE_NAME, AWS_DEFAULT_REGION, cors_config

app = Chalice(app_name='appointments')
app.log.setLevel(logging.DEBUG)
_DB = None


@app.route('/')
def index():
    return custom_responses.get_base_res()


@app.route('/appointments', methods=['GET'], cors=cors_config)
def get_all_appointments():
    results = app.current_request.query_params.get('results')
    appointment_list = calendar_api.get_next_events(results, 'primary')
    return custom_responses.get_appointments_list(appointment_list)




def get_app_db():
    global _DB
    if _DB is None:
        _DB = database.DynamoDBAppointments(
            boto3.Session().resource(service_name='dynamodb', region_name=AWS_DEFAULT_REGION).Table(TABLE_NAME)
        )
    return _DB