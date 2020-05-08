import datetime
import json

import pytz
from uuid import uuid4

from boto3.dynamodb.conditions import Attr
from chalicelib.validation import validate_contact_fields, all_fields, validate_update


DEFAULT_USERNAME = 'local'
EMPTY_FIELD = '-'


class ContactsDB(object):
    def list_items(self, username):
        pass

    def add_item(self, contact, username):
        pass

    def get_item(self, uid, username):
        pass

    def delete_item(self, uid, username):
        pass

    def update_item(self, uid, body, username):
        pass


class DynamoDBContacts(ContactsDB):
    def __init__(self, table_resource):
        self._table = table_resource

    def list_all_items(self, username=DEFAULT_USERNAME):
        response = self._table.scan()
        return response['Items']

    def list_active_items(self, username=DEFAULT_USERNAME):
        response = self._table.scan(FilterExpression=Attr('active').eq(True))
        return response['Items']

    def add_item(self, contact, username=DEFAULT_USERNAME):
        new_contact = make_contact(contact, username)
        if validate_contact_fields(new_contact):
            print("Inserting: " + json.dumps(new_contact))
            self._table.put_item(
                Item=new_contact
            )
            return new_contact.get('uid')
        else:
            return None

    def get_item(self, uid, username=DEFAULT_USERNAME):
        response = self._table.get_item(
            Key={'uid': uid, }
        )
        if 'Item' in response:
            return response['Item']
        return None

    def inactivate_item(self, uid, username=DEFAULT_USERNAME):
        items = self._table.scan(FilterExpression=Attr('patient_uid').eq(uid))['Items']
        item = items[0]
        if item is not None:
            item['active'] = False
            response = self._table.put_item(Item=item)
            return response['ResponseMetadata']
        else:
            return 404

    def update_item(self, uid, body, username=DEFAULT_USERNAME):
        if validate_update(body):
            item = self.get_item(uid, username)
            if item is not None:
                for key in body.keys():
                    item[key] = body[key].lower().strip()
                if validate_contact_fields(item):
                    now = str(datetime.datetime.now(pytz.timezone('America/Guatemala')))
                    item['modified_by'] = username
                    item['modified_timestamp'] = now
                    response = self._table.put_item(Item=item)
                    return response['ResponseMetadata']
                else:
                    return 400
            else:
                return 404
        else:
            return 400


def make_contact(contact, username):
    uid = contact['patient_uid']
    now = str(datetime.datetime.now(pytz.timezone('America/Guatemala')))
    new_contact = {
        'uid': uid,
        'active': True,
        'created_by': username,
        'modified_by': username,
        'created_timestamp': now,
        'modified_timestamp': now,
    }
    for key in all_fields:
        value = contact.get(key, EMPTY_FIELD)
        if isinstance(value, list):
            new_contact[key] = value
        elif value is '':
            new_contact[key] = '-'
        else:
            new_contact[key] = value.lower().strip()
    print("Making: " + json.dumps(new_contact))
    return new_contact
