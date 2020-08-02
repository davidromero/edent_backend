import datetime
import json
import logging
from uuid import uuid4

import pytz
import requests
from boto3.dynamodb.conditions import Attr
from chalicelib.validation import validate_checkout_fields, all_fields

logger = logging.getLogger()
logger.setLevel(logging.INFO)
DEFAULT_USERNAME = 'local'
EMPTY_FIELD = '-'


class CheckoutDB(object):
    def list_items(self, username):
        pass

    def add_item(self, checkout, username):
        pass

    def get_item(self, uid, username):
        pass

    def update_item(self, uid, body, username):
        pass


class DynamoDBCheckout(CheckoutDB):
    def __init__(self, table_resource):
        self._table = table_resource

    def list_unpaid_items(self, username=DEFAULT_USERNAME):
        logger.info('Listing unpaid treatments in checkout')
        response = self._table.scan(FilterExpression=Attr('paid').eq(False))
        return response['Items']

    def list_paid_items(self, username=DEFAULT_USERNAME):
        logger.info('Listing paid treatments in checkout')
        response = self._table.scan(FilterExpression=Attr('paid').eq(True))
        return response['Items']

    def list_descr_by_id(self, patient_uid, username=DEFAULT_USERNAME):
        logger.info(f'Getting checkout description {patient_uid}')
        response = self._table.scan(FilterExpression=Attr('patient_uid').eq(patient_uid))
        response_item = {}
        response_list = []
        for res in response['Items']:
            for value in res.keys():
                if value == 'treatment_description':
                    response_item[value] = res.get(value)
                elif value == 'next_treatment':
                    response_item[value] = res.get(value)
                    response_item['created_timestamp'] = res['created_timestamp']
                    response_item['sorted_timestamp'] = res['created_timestamp']
            response_list.append(response_item)
            response_item = {}
        logger.info(response_list)
        if response_list:
            for key in response_list:
                key['sorted_timestamp'] = key['sorted_timestamp'].replace('-', '').replace(':', '').replace('T',
                                        '').replace(' ', '').replace('.', '')[:14]
            return sorted(response_list, key=lambda x: x['sorted_timestamp'], reverse=True)
        logger.error(f'Checkout Description for Patient {patient_uid} not found')
        return None

    def get_item(self, uid, username=DEFAULT_USERNAME):
        logger.info(f'Getting checkout {uid}')
        response = self._table.get_item(
            Key={'uid': uid, }
        )
        if 'Item' in response:
            return response['Item']
        logger.error(f'Patient {uid} not found')
        return None

    def add_item(self, checkout, username=DEFAULT_USERNAME):
        logger.info('Creating a new checkout')
        new_checkout = make_checkout(checkout, username)
        if validate_checkout_fields(new_checkout):
            add_treatments(new_checkout, checkout)
            logger.info(f'Adding checkout: {json.dumps(new_checkout)}')
            self._table.put_item(
                Item=new_checkout
            )
            return new_checkout.get('uid')
        else:
            logger.error('Checkout creation is not valid')
            return None

    def pay_item(self, uid, body, username=DEFAULT_USERNAME):
        payment_amount = int(body['payment_amount'])
        logger.info(f'Paying checkout treatment {uid} with {payment_amount}')
        item = self.get_item(uid, username)
        if item is not None:
            paid_amount, paid = make_payment(payment_amount, item)
            if paid_amount is None:
                return 400
            else:
                now = str(datetime.datetime.now(pytz.timezone('America/Guatemala')))
                item['modified_by'] = username
                item['modified_timestamp'] = now
                item['paid_amount'] = paid_amount
                item['paid'] = paid
                response = self._table.put_item(Item=item)
                return response['ResponseMetadata']
        else:
            logger.error(f'Checkout could not be payed')
            return 400


def make_payment(payment_amount, checkout):
    total = 0
    checkout_list = checkout['checkout']
    for treatment in checkout_list:
        total += int(treatment['price'])
    paid_amount = int(checkout['paid_amount'])
    if payment_amount <= (total - paid_amount):
        logger.info(f'New payment amount: {payment_amount}. Total: {total}')
        paid_amount += payment_amount
        return paid_amount, paid_amount == total
    else:
        logger.error(f'Not allowed amount: {payment_amount}. Total: {total}')
        return None, None


def add_treatments(new_checkout, checkout):
    uid = str(uuid4())[:13]
    treatments = checkout['checkout']
    patient = checkout['patient']
    for treatment in treatments:
        payload = {
            'uid': uid,
            'checkout_uid': new_checkout['uid'],
            'treatment_uid': treatment['uid'],
            'treatment_name': treatment['name'],
            'treatment_price': treatment['price'],
            'treatment_type': checkout['treatment_type'],
            'patient_uid': checkout['patient_uid']
        }
        for key in patient:
            value = patient.get(key, EMPTY_FIELD)
            payload[key] = value
        res = requests.post('https://hrtd76yb9b.execute-api.us-east-1.amazonaws.com/api/treatments',
                            data=json.dumps(payload),
                            headers={'Content-type': 'application/json', 'Accept': 'application/json'})
        if res.status_code is 201:
            logger.info('Treatment inserted')
        else:
            logger.info('Error' + res.text)


def make_checkout(checkout, username):
    uid = str(uuid4())[:13]
    now = str(datetime.datetime.now(pytz.timezone('America/Guatemala')))
    new_checkout = {
        'uid': uid,
        'patient_uid': checkout['patient_uid'],
        'created_by': username,
        'modified_by': username,
        'created_timestamp': now,
        'modified_timestamp': now,
        'paid': False,
        'paid_amount': 0,
        'treatment_description': checkout['treatment_description'],
        'next_treatment': checkout['next_treatment'],
    }
    for key in all_fields:
        value = checkout.get(key, EMPTY_FIELD)
        new_checkout[key] = value
        if isinstance(value, list):
            new_checkout[key] = value
        elif value is '':
            new_checkout[key] = EMPTY_FIELD
        else:
            if isinstance(new_checkout[key], dict):
                new_checkout[key] = dict((k.lower(), v.lower()) for k, v in new_checkout[key].items())
            else:
                new_checkout[key] = value.lower().strip()
    logger.info("Making: " + json.dumps(new_checkout))
    return new_checkout
