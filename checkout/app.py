import boto3 as boto3
from chalice import Chalice

from chalicelib import database, custom_responses
from chalicelib.config import TABLE_NAME, AWS_DEFAULT_REGION, cors_config

app = Chalice(app_name='checkout')

_DB = None


@app.route('/')
def index():
    return custom_responses.get_base_res()


@app.route('/checkout', methods=['GET'])
def get_all_checkouts():
    checkout_list = get_app_db().list_unpaid_items()
    return custom_responses.get_appointments_list(checkout_list)


@app.route('/checkout', methods=['POST'], cors=cors_config)
def checkout_treatments():
    body = app.current_request.json_body
    new_item_id = get_app_db().add_item(checkout=body)
    return custom_responses.post_response(new_item_id)


@app.route('/checkout/{uid}', methods=['DELETE'], cors=cors_config)
def pay_checkout(uid):
    response = get_app_db().pay_item(uid)
    return custom_responses.edit_response(response, uid)


def get_app_db():
    global _DB
    if _DB is None:
        _DB = database.DynamoDBCheckout(
            boto3.Session().resource(service_name='dynamodb', region_name=AWS_DEFAULT_REGION).Table(TABLE_NAME)
        )
    return _DB