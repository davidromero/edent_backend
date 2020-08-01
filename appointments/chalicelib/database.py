import datetime
import json
import logging

import pytz
from boto3.dynamodb.conditions import Attr

logger = logging.getLogger()
logger.setLevel(logging.INFO)
DEFAULT_USERNAME = 'local'
EMPTY_FIELD = '-'


class AppointmentsDB(object):
    def list_items(self, username):
        pass

    def add_item(self, patient, username):
        pass

    def delete_item(self, uid, username):
        pass


class DynamoDBAppointments(AppointmentsDB):
    def __init__(self, table_resource):
        self._table = table_resource

    def list_all_items(self, username=DEFAULT_USERNAME):
        logger.info(f'Listing all unattended appointments')
        response = self._table.scan(
            FilterExpression=Attr('attended').eq(False)
        )
        return response['Items']

    def add_item(self, appointment, username=DEFAULT_USERNAME):
        new_appointment = make_appointment(appointment, username)
        logger.info(f'Adding appointment: {json.dumps(new_appointment)}')
        self._table.put_item(
            Item=new_appointment
        )
        return new_appointment.get('uid')

    def inactivate_item(self, uid):
        logger.info(f'Inactivating appointment {uid}')
        response = self._table.delete_item(Key={'uid': uid})
        logger.info('Response is:' + json.dumps(response))
        return response['ResponseMetadata']


def make_appointment(appointment, username):
    now = str(datetime.datetime.now(pytz.timezone('America/Guatemala')))
    new_appointment = {
        'uid': appointment['id'],
        'attended': False,
        'created_by': username,
        'modified_by': username,
        'created_timestamp': now,
        'modified_timestamp': now,
        'title': appointment['title'],
        'link': appointment['link'],
        'description': appointment['description'],
        'start': appointment['start']['dateTime'],
        'end': appointment['end']['dateTime'],
    }
    logger.info("Making: " + json.dumps(new_appointment))
    return new_appointment
