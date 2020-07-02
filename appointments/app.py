import boto3 as boto3
import logging
from chalice import Chalice

from chalicelib import database, custom_responses, calendar_api
from chalicelib.config import TABLE_NAME, AWS_DEFAULT_REGION, cors_config

app = Chalice(app_name='appointments')
app.log.setLevel(logging.DEBUG)
_DB = None


@app.route('/', methods=['GET'], cors=cors_config)
def index():
    return custom_responses.get_base_res()


@app.route('/appointments', methods=['GET'], cors=cors_config)
def get_all_appointments():
    params = app.current_request.query_params
    if params is not None:
        appointment_list = calendar_api.get_next_events(params.get('results'), 'primary')
        return custom_responses.get_appointments_list(appointment_list)
    appointment_list = get_app_db().get_next_events()
    return custom_responses.get_appointments_list()



@app.route('/appointments/{uid}', methods=['POST'], cors=cors_config)
def add_new_appointment(uid):
    body = app.current_request.json_body
    new_item_id = get_app_db().add_item(appointment=body, patient_uid=uid)
    return custom_responses.post_response(new_item_id)


def get_app_db():
    global _DB
    if _DB is None:
        _DB = database.DynamoDBAppointments(
            boto3.Session().resource(service_name='dynamodb', region_name=AWS_DEFAULT_REGION).Table(TABLE_NAME)
        )
    return _DB