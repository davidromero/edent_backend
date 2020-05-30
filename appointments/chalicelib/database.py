from boto3.dynamodb.conditions import Attr
import logging
from chalicelib.validation import validate_appointment_fields, all_fields

logging.basicConfig()
logger = logging.getLogger(__name__)
DEFAULT_USERNAME = 'local'
EMPTY_FIELD = '-'


class AppointmentsDB(object):
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


class DynamoDBAppointments(AppointmentsDB):
    def __init__(self, table_resource):
        self._table = table_resource

    def list_all_items(self, username=DEFAULT_USERNAME):
        logger.debug('Listing all appointments')
        response = self._table.scan()
        return response['Items']

    def list_items_by_id(self, treatment_uid, username=DEFAULT_USERNAME):
        logger.debug(f'Getting treatments from treatment {treatment_uid}')
        response = self._table.scan(FilterExpression=Attr('patient_uid').eq(treatment_uid))
        if 'Items' in response:
            return response['Items']
        logger.error(f'Treatment {treatment_uid} not found')
        return None