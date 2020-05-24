import datetime
import json
import logging
from uuid import uuid4

import pytz
from boto3.dynamodb.conditions import Attr
from chalicelib.validation import validate_checkout_fields, all_fields

logging.basicConfig()
logger = logging.getLogger(__name__)
DEFAULT_USERNAME = 'local'
EMPTY_FIELD = '-'


class CheckoutDB(object):
    def list_items(self, username):
        pass

    def add_item(self, checkout, username):
        pass

    def get_item(self, uid, username):
        pass

    def delete_item(self, uid, username):
        pass

    def update_item(self, uid, body, username):
        pass


class DynamoDBCheckout(CheckoutDB):
    def __init__(self, table_resource):
        self._table = table_resource

    def list_unpaid_items(self, username=DEFAULT_USERNAME):
        logger.debug('Listing unpaid treatments in checkout')
        response = self._table.scan(FilterExpression=Attr('paid').eq(False))
        return response['Items']

    def list_paid_items(self, treatment_uid, username=DEFAULT_USERNAME):
        logger.debug('Listing paid treatments in checkout')
        response = self._table.scan(FilterExpression=Attr('paid').eq(True))
        return response['Items']

    def get_item(self, uid, username=DEFAULT_USERNAME):
        logger.debug(f'Getting checkout {uid}')
        response = self._table.get_item(
            Key={'uid': uid, }
        )
        if 'Item' in response:
            return response['Item']
        logger.error(f'Patient {uid} not found')
        return None

    def add_item(self, checkout, username=DEFAULT_USERNAME):
        logger.debug('Creating a new checkout')
        new_checkout = make_checkout(checkout, username)
        if validate_checkout_fields(new_checkout):
            logger.debug(f'Adding checkout: {json.dumps(new_checkout)}')
            self._table.put_item(
                Item=new_checkout
            )
            return new_checkout.get('uid')
        else:
            logger.error('Checkout creation is not valid')
            return None

    def pay_item(self, uid, username=DEFAULT_USERNAME):
        logger.debug(f'Paying checkout treatment {uid}')
        item = self.get_item(uid, username)
        if item is not None:
            item['paid'] = True
            now = str(datetime.datetime.now(pytz.timezone('America/Guatemala')))
            item['modified_by'] = username
            item['modified_timestamp'] = now
            response = self._table.put_item(Item=item)
            return response['ResponseMetadata']
        else:
            logger.error(f'Contact could not be inactivated')
            return 400


def make_checkout(checkout, username):
    uid = str(uuid4())[:13]
    now = str(datetime.datetime.now(pytz.timezone('America/Guatemala')))
    new_checkout = {
        'uid': uid,
        'created_by': username,
        'modified_by': username,
        'created_timestamp': now,
        'modified_timestamp': now,
        'paid': False,
    }
    for key in all_fields:
        value = checkout.get(key, EMPTY_FIELD)
        new_checkout[key] = value
    logger.debug("Making: " + json.dumps(new_checkout))
    return new_checkout
