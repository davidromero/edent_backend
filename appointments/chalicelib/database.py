import datetime
import json
import logging
from boto3.dynamodb.conditions import Attr

import pytz

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
        start = str(datetime.datetime.now(pytz.timezone('America/Guatemala')))[:10]
        logger.info(f'Listing all patients of {start}')
        response = self._table.scan(
            FilterExpression=Attr('start').gte(start)
        )
        return response['Items']

    def add_item(self, appointment, username=DEFAULT_USERNAME):
        new_appointment = make_appointment(appointment, username)
        logger.info(f'Adding Appointment: {json.dumps(new_appointment)}')
        self._table.put_item(
            Item=new_appointment
        )
        return new_appointment.get('uid')


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
