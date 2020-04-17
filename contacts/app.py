import boto3 as boto3
from chalice import Chalice

from chalicelib import database, custom_responses
from chalicelib.config import TABLE_NAME, AWS_DEFAULT_REGION

app = Chalice(app_name='contacts')
_DB = None


@app.route('/', methods=['GET'])
def index():
    return custom_responses.get_base_res()


@app.route('/contacts', methods=['GET'])
def get_all_contacts():
    active_contact_list = get_app_db().list_active_items()
    return custom_responses.get_active_contacts(active_contact_list)


@app.route('/contacts/{uid}', methods=['GET'])
def get_contact(uid):
    response = get_app_db().get_item(uid)
    return custom_responses.get_response(response, uid)


@app.route('/contacts', methods=['POST'])
def add_new_contact():
    body = app.current_request.json_body
    new_item_id = get_app_db().add_item(contact=body)
    return custom_responses.post_response(new_item_id)


@app.route('/contacts/{uid}', methods=['DELETE'])
def delete_contact(uid):
    response = get_app_db().inactivate_item(uid)
    return custom_responses.edit_response(response, uid)


@app.route('/contacts/{uid}', methods=['PUT'])
def update_contact(uid):
    body = app.current_request.json_body
    response = get_app_db().update_item(uid, body)
    return custom_responses.edit_response(response, uid)


def get_app_db():
    global _DB
    if _DB is None:
        _DB = database.DynamoDBContacts(
            boto3.Session().resource(service_name='dynamodb', region_name=AWS_DEFAULT_REGION).Table(TABLE_NAME)
        )
    return _DB


