import boto3 as boto3
import logging
from chalice import Chalice

from chalicelib import database, custom_responses
from chalicelib.config import RATES_TABLE_NAME, TABLE_NAME, AWS_DEFAULT_REGION, cors_config

app = Chalice(app_name='treatments')
app.log.setLevel(logging.DEBUG)
_DB = None


@app.route('/', methods=['GET'], cors=cors_config)
def index():
    return custom_responses.get_base_res()


@app.route('/treatments', methods=['GET'], cors=cors_config)
def get_all_treatments():
    treatment_list = get_app_db().list_all_items()
    return custom_responses.get_treatment_list(treatment_list)


@app.route('/treatments/{uid}', methods=['GET'], cors=cors_config)
def get_treatment_by_id(uid):
    response = get_app_db().list_items_by_id(uid)
    return custom_responses.get_response(response, uid)


@app.route('/rates', methods=['GET'], cors=cors_config)
def get_treatment_rates():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table(RATES_TABLE_NAME)
    response = table.scan()
    return custom_responses.get_treatment_rates(response['Items'])


def get_app_db():
    global _DB
    if _DB is None:
        _DB = database.DynamoDBTreatments(
            boto3.Session().resource(service_name='dynamodb', region_name=AWS_DEFAULT_REGION).Table(TABLE_NAME)
        )
    return _DB

