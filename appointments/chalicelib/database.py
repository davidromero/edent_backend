import datetime
import json
import logging
from uuid import uuid4

import pytz
import requests
from boto3.dynamodb.conditions import Attr

logger = logging.getLogger()
logger.setLevel(logging.INFO)
DEFAULT_USERNAME = 'local'
EMPTY_FIELD = '-'
from chalicelib.validation import validate_appointment_fields, validate_mandatory_fields, has_mandatory_fields, \
    validate_datetime


class AppointmentsDB(object):
    def list_items(self, username):
        pass


class DynamoDBAppointments(AppointmentsDB):
    def __init__(self, table_resource):
        self._table = table_resource

    def list_all_items(self, username=DEFAULT_USERNAME):
        logger.info('Listing all patients')
        response = self._table.scan()
        return response['Items']

    def add_item(self, appointment, username=DEFAULT_USERNAME):
        uid = 33333
        new_appointment = make_appointment(appointment, username, uid)
        logger.info(f'Adding Appointment: {json.dumps(new_appointment)}')
        self._table.put_item(
            Item=new_appointment
        )
        return new_appointment.get('uid')


def make_appointment(appointment, username, uid):
    now = str(datetime.datetime.now(pytz.timezone('America/Guatemala')))
    new_appointment = {
        'uid': '3gvcdf69e0ne03o1gla4f4444',
        'link': 'google.com',
        'title': 'Andrea Molina',
        'description': 'Tel: 02030105',
        'start': {
            'dateTime': now
        },
        'end': {
            'dateTime': now
        },
        'uid': uid,
        'active': True,
        'created_by': username,
        'modified_by': username,
        'created_timestamp': now,
        'modified_timestamp': now,
        'contact_uid': uid,
    }
    return new_appointment
