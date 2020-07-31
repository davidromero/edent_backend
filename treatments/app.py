import boto3 as boto3
from boto3.dynamodb.conditions import Attr
from chalice import Chalice
from chalicelib import database, custom_responses
from chalicelib.config import RATES_TABLE_NAME, TABLE_NAME, AWS_DEFAULT_REGION, cors_config

app = Chalice(app_name='treatments')
_DB = None


@app.route('/', methods=['GET'])
def index():
    return custom_responses.get_base_res()


@app.route('/treatments', methods=['GET'])
def get_all_treatments():
    treatment_list = get_app_db().list_all_items()
    return custom_responses.get_treatments_list(treatment_list)


# TODO: Refactor, delete not used services ?

# Get treatments per patientuid
@app.route('/treatments/{uid}', methods=['GET'])
def get_treatment_by_patient_uid(uid):
    response = get_app_db().list_items_by_id(uid)
    return custom_responses.get_response(response, uid)


@app.route('/treatments', methods=['POST'], cors=cors_config)
def add_new_treatments():
    body = app.current_request.json_body
    new_item_id = get_app_db().add_item(treatment=body)
    return custom_responses.post_response(new_item_id)


@app.route('/rates', methods=['GET'])
def get_treatment_rates():
    params = app.current_request.query_params
    dynamodb = boto3.resource('dynamodb', region_name=AWS_DEFAULT_REGION)
    table = dynamodb.Table(RATES_TABLE_NAME)
    if params:
        response = table.scan(FilterExpression=Attr('type').eq(params['type']))
    else:
        response = table.scan()
    return custom_responses.get_treatment_rates(response['Items'])


def get_app_db():
    global _DB
    if _DB is None:
        _DB = database.DynamoDBTreatments(
            boto3.Session().resource(service_name='dynamodb', region_name=AWS_DEFAULT_REGION).Table(TABLE_NAME)
        )
    return _DB
