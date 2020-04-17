import boto3 as boto3
from chalice import Chalice

from chalicelib import database, custom_responses
from chalicelib.config import TABLE_NAME, AWS_DEFAULT_REGION

app = Chalice(app_name='patients')
_DB = None


@app.route('/', methods=['GET'])
def index():
    return custom_responses.get_base_res()


@app.route('/patients', methods=['GET'])
def get_all_patients():
    active_patient_list = get_app_db().list_active_items()
    return custom_responses.get_active_patients(active_patient_list)


@app.route('/patients/{uid}', methods=['GET'])
def get_patient(uid):
    response = get_app_db().get_item(uid)
    return custom_responses.get_response(response, uid)


@app.route('/patients', methods=['POST'])
def add_new_patient():
    body = app.current_request.json_body
    new_item_id = get_app_db().add_item(patient=body)
    return custom_responses.post_response(new_item_id)


@app.route('/patients/{uid}', methods=['DELETE'])
def delete_patientt(uid):
    response = get_app_db().inactivate_item(uid)
    return custom_responses.edit_response(response, uid)


@app.route('/patients/{uid}', methods=['PUT'])
def update_patient(uid):
    body = app.current_request.json_body
    response = get_app_db().update_item(uid, body)
    return custom_responses.edit_response(response, uid)


def get_app_db():
    global _DB
    if _DB is None:
        _DB = database.DynamoDBPatients(
            boto3.Session().resource(service_name='dynamodb', region_name=AWS_DEFAULT_REGION).Table(TABLE_NAME)
        )
    return _DB
