import boto3 as boto3
from chalice import Chalice

from chalicelib import database, custom_responses
from chalicelib.config import TABLE_NAME, AWS_DEFAULT_REGION, cors_config

app = Chalice(app_name='appointments')
_DB = None


@app.route('/', methods=['GET'])
def index():
    return custom_responses.get_base_res()


@app.route('/appointments', methods=['GET'])
def get_all_appointments():
    active_appointments_list = get_app_db().list_all_items()
    return custom_responses.get_appointments_list(active_appointments_list)


@app.route('/appointments', methods=['POST'], cors=cors_config)
def add_new_patient():
    body = app.current_request.json_body
    new_item_id = get_app_db().add_item(appointment=body)
    return custom_responses.post_response(new_item_id)


def get_app_db():
    global _DB
    if _DB is None:
        _DB = database.DynamoDBAppointments(
            boto3.Session().resource(service_name='dynamodb', region_name=AWS_DEFAULT_REGION).Table(TABLE_NAME)
        )
    return _DB
