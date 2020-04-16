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





def get_app_db():
    global _DB
    if _DB is None:
        _DB = database.DynamoDBContacts(
            boto3.Session().resource(service_name='dynamodb', region_name=AWS_DEFAULT_REGION).Table(TABLE_NAME)
        )
    return _DB
