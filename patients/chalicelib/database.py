import datetime
import json
import logging
from uuid import uuid4

import pytz
import requests
from boto3.dynamodb.conditions import Attr
from chalicelib.validation import validate_patient_fields, all_fields, validate_update

logging.basicConfig()
logger = logging.getLogger(__name__)
DEFAULT_USERNAME = 'local'
EMPTY_FIELD = '-'


class PatientsDB(object):
    def list_items(self, username):
        pass

    def add_item(self, patient, username):
        pass

    def get_item(self, uid, username):
        pass

    def delete_item(self, uid, username):
        pass

    def update_item(self, uid, body, username):
        pass


class DynamoDBPatients(PatientsDB):
    def __init__(self, table_resource):
        self._table = table_resource

    def list_all_items(self, username=DEFAULT_USERNAME):
        logger.debug('Listing all patients')
        response = self._table.scan()
        return response['Items']

    def list_active_items(self, username=DEFAULT_USERNAME):
        logger.debug('Listing active patients')
        response = self._table.scan(FilterExpression=Attr('active').eq(True))
        return response['Items']

    def add_item(self, patient, username=DEFAULT_USERNAME):
        logger.debug('Adding new patient')
        uid = str(uuid4())[:13]
        new_patient = make_patient(patient, username, uid)
        if validate_patient_fields(new_patient):
            new_contact = make_contact(patient, username, uid)
            if new_contact is not None:
                logger.debug(f'Adding patient: {json.dumps(new_patient)}')
                self._table.put_item(
                    Item=new_patient
                )
                return new_patient.get('uid')
            else:
                logger.error('Contact could not be created')
                return None
        else:
            logger.error('Patient creation is not valid')
            return None

    def get_item(self, uid, username=DEFAULT_USERNAME):
        logger.debug(f'Getting patient {uid}')
        response = self._table.get_item(
            Key={'uid': uid, }
        )
        if 'Item' in response:
            return response['Item']
        logger.error(f'Patient {uid} not found')
        return None

    def inactivate_item(self, uid, username=DEFAULT_USERNAME):
        logger.debug(f'Inactivating patient {uid}')
        item = self.get_item(uid, username)
        if item is not None:
            res = inactivate_contact(item['contact_uid'])
            if res is not None:
                item['active'] = False
                now = str(datetime.datetime.now(pytz.timezone('America/Guatemala')))
                item['modified_by'] = username
                item['modified_timestamp'] = now
                response = self._table.put_item(Item=item)
                return response['ResponseMetadata']
            else:
                logger.error(f'Contact could not be inactivated')
                return 400
        else:
            logger.error(f'Patient {uid} not found')
            return 404

    def update_item(self, uid, body, username=DEFAULT_USERNAME):
        logger.debug(f'Updating patient {uid}')
        if validate_update(body):
            item = self.get_item(uid, username)
            if item is not None:
                for key in body.keys():
                    item[key] = body[key].lower().strip()
                res = update_contact(item['contact_uid'], body)
                if res is not None:
                    if validate_patient_fields(item):
                        logger.debug(f'Updating patient {json.dumps(item)}')
                        now = str(datetime.datetime.now(pytz.timezone('America/Guatemala')))
                        item['modified_by'] = username
                        item['modified_timestamp'] = now
                        response = self._table.put_item(Item=item)
                        return response['ResponseMetadata']
                    else:
                        logger.error(f'Patient update is not valid')
                        return 400
                else:
                    logger.error(f'Contact could not be updated')
                    return 400
            else:
                logger.error(f'Patient {uid} not found')
                return 404
        else:
            logger.error(f'Patient update is not valid')
            return 400


def make_contact(patient, username, uid):
    new_contact = {
        'patient_uid': uid,
        'first_name': patient['first_name'],
        'last_name': patient['last_name'],
        'clinic_location': patient['clinic_location'],
        'address': patient['address'],
        'email': patient['email'],
        'phone_number': patient['phone_number']
    }
    res = requests.post('https://9jtkflgqhe.execute-api.us-east-1.amazonaws.com/api/contacts',
                        data=json.dumps(new_contact),
                        headers={'Content-type': 'application/json', 'Accept': 'application/json'})
    if res.status_code is 201:
        return res.json()
    else:
        return None


def inactivate_contact(uid):
    res = requests.delete('https://9jtkflgqhe.execute-api.us-east-1.amazonaws.com/api/contacts/' + uid)
    if res.status_code is 204:
        return res
    else:
        return None


def update_contact(uid, body):
    res = requests.put('https://9jtkflgqhe.execute-api.us-east-1.amazonaws.com/api/contacts/' + uid,
                       data=json.dumps(body),
                       headers={'Content-type': 'application/json', 'Accept': 'application/json'})
    if res.status_code is 204:
        return res
    else:
        return None


def make_patient(patient, username, uid):
    now = str(datetime.datetime.now(pytz.timezone('America/Guatemala')))
    new_patient = {
        'uid': uid,
        'active': True,
        'created_by': username,
        'modified_by': username,
        'created_timestamp': now,
        'modified_timestamp': now,
        'contact_uid': uid,
    }
    for key in all_fields:
        value = patient.get(key, EMPTY_FIELD)
        if isinstance(value, list):
            new_patient[key] = value
        elif value is '':
            new_patient[key] = '-'
        else:
            new_patient[key] = value.lower().strip()
    return new_patient
