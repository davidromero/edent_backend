import boto3 as boto3
from chalice import Chalice

from chalicelib import database, custom_responses
from chalicelib.config import TABLE_NAME, AWS_DEFAULT_REGION

app = Chalice(app_name='treatments')


@app.route('/')
def index():
    return {'hello': 'world'}



def get_app_db():
    global _DB
    if _DB is None:
        _DB = database.DynamoDBContacts(
            boto3.Session().resource(service_name='dynamodb', region_name=AWS_DEFAULT_REGION).Table(TABLE_NAME)
        )
    return _DB

