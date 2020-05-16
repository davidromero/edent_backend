import boto3 as boto3
import logging
from chalice import Chalice

from chalicelib import database, custom_responses
from chalicelib.config import RATES_TABLE_NAME, TABLE_NAME, AWS_DEFAULT_REGION

app = Chalice(app_name='treatments')
app.log.setLevel(logging.DEBUG)
_DB = None


@app.route('/', methods=['GET'])
def index():
    return custom_responses.get_base_res()



@app.route('/rates')
def get_treatment_rates():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table(RATES_TABLE_NAME)
    response = table.scan()
    return custom_responses.get_treatment_rates(response['Items'])



def get_app_db():
    global _DB
    if _DB is None:
        _DB = database.DynamoDBContacts(
            boto3.Session().resource(service_name='dynamodb', region_name=AWS_DEFAULT_REGION).Table(TABLE_NAME)
        )
    return _DB

