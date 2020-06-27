import datetime
from uuid import uuid4
from chalicelib import calendar_api

import pytz
from boto3.dynamodb.conditions import Attr
import logging
import json
from chalicelib.validation import validate_appointment_fields, all_fields

logging.basicConfig()
logger = logging.getLogger(__name__)
DEFAULT_USERNAME = 'local'
EMPTY_FIELD = '-'


class AppointmentsDB(object):
    def list_items(self, username):
        pass

    def add_item(self, appointment, patient_uid, username):
        pass

    def get_item(self, uid, username):
        pass

    def delete_item(self, uid, username):
        pass

    def update_item(self, uid, body, username):
        pass


class DynamoDBAppointments(AppointmentsDB):
    def __init__(self, table_resource):
        self._table = table_resource

    def list_all_items(self, username=DEFAULT_USERNAME):
        logger.debug('Listing all appointments')
        response = self._table.scan()
        return response['Items']

    def list_items_by_id(self, patient_uid, username=DEFAULT_USERNAME):
        logger.debug(f'Getting appointments from patient {patient_uid}')
        response = self._table.scan(FilterExpression=Attr('patient_uid').eq(patient_uid))
        if 'Items' in response:
            return response['Items']
        logger.error(f'Patient {patient_uid} not found')
        return None

    def add_item(self, appointment, patient_uid, username=DEFAULT_USERNAME):
        logger.debug(f'Scheduling appointment for {patient_uid}')
        calendar_api.create_event(appointment)
        # new_appointment = make_appointment(appointment, patient_uid, username)
        # if validate_appointment_fields(new_appointment):
        #     new_appointment['event_link'] = calendar_api.create_event(new_appointment)
        #     logger.debug(f'Adding appointment: {json.dumps(new_appointment)}')
        #     self._table.put_item(
        #         Item=new_appointment
        #     )
        #     return new_appointment.get('uid')
        # else:
        #     logger.error('Contact creation is not valid')
        #     return None


def make_appointment(appointment, patient_uid, username):
    uid = str(uuid4())[:13]
    now = str(datetime.datetime.now(pytz.timezone('America/Guatemala')))
    new_appointment = {
        'uid': uid,
        'created_by': username,
        'modified_by': username,
        'created_timestamp': now,
        'modified_timestamp': now,
        'patient_uid': patient_uid,
        'attended': False,
    }
    for key in all_fields:
        value = appointment.get(key, EMPTY_FIELD)
        if isinstance(value, list):
            new_appointment[key] = value
        elif value is '':
            new_appointment[key] = EMPTY_FIELD
        else:
            new_appointment[key] = value.lower().strip()
    logger.debug("Making: " + json.dumps(new_appointment))
    return new_appointment
