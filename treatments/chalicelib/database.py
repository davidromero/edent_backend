import datetime
import json
import logging
from uuid import uuid4

import pytz
from boto3.dynamodb.conditions import Attr
from chalicelib.validation import validate_treatment_fields, all_fields

logger = logging.getLogger()
logger.setLevel(logging.INFO)
DEFAULT_USERNAME = 'local'
EMPTY_FIELD = '-'


class TreatmentsDB(object):
    def list_items(self, username):
        pass

    def add_item(self, treatment, username):
        pass

    def get_item(self, uid, username):
        pass

    def delete_item(self, uid, username):
        pass

    def update_item(self, uid, body, username):
        pass


class DynamoDBTreatments(TreatmentsDB):
    def __init__(self, table_resource):
        self._table = table_resource

    def list_all_items(self, username=DEFAULT_USERNAME):
        logger.info('Listing all treatments')
        response = self._table.scan()
        return response['Items']

    def list_items_by_id(self, treatment_uid, username=DEFAULT_USERNAME):
        logger.info(f'Getting treatments from treatment {treatment_uid}')
        response = self._table.scan(FilterExpression=Attr('patient_uid').eq(treatment_uid))
        if 'Items' in response:
            return response['Items']
        logger.error(f'Treatment {treatment_uid} not found')
        return None

    def add_item(self, treatment, username=DEFAULT_USERNAME):
        logger.info('Adding new treatment')
        uid = str(uuid4())[:13]
        new_treatment = make_treatment(treatment, username)
        if validate_treatment_fields(new_treatment):
            logger.info(f'Adding treatment: {json.dumps(new_treatment)}')
            self._table.put_item(
                Item=new_treatment
            )
            return new_treatment.get('uid')
        else:
            logger.error('Treatment creation is not valid')
            return None


def make_treatment(treatment, username):
    uid = str(uuid4())[:13]
    now = str(datetime.datetime.now(pytz.timezone('America/Guatemala')))
    new_treatment = {
        'uid': uid,
        'created_by': username,
        'modified_by': username,
        'created_timestamp': now,
        'modified_timestamp': now,
    }
    for key in all_fields:
        value = treatment.get(key, EMPTY_FIELD)
        if isinstance(value, list):
            new_treatment[key] = value
        elif value is '':
            new_treatment[key] = EMPTY_FIELD
        else:
            new_treatment[key] = value.lower().strip()
    logger.info("Making: " + json.dumps(new_treatment))
    return new_treatment
