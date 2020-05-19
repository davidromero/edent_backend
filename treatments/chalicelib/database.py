from boto3.dynamodb.conditions import Attr
import json
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
DEFAULT_USERNAME = 'local'


class TreatmentsDB(object):
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


class DynamoDBTreatments(TreatmentsDB):
    def __init__(self, table_resource):
        self._table = table_resource

    def list_all_items(self, username=DEFAULT_USERNAME):
        logger.debug('Listing all treatments')
        response = self._table.scan()
        return response['Items']

    def list_items_by_id(self, patient_uid, username=DEFAULT_USERNAME):
        logger.debug(f'Getting treatments from patient {patient_uid}')
        response = self._table.scan(FilterExpression=Attr('patient_uid').eq(patient_uid))
        if 'Items' in response:
            return response['Items']
        logger.error(f'Patient {patient_uid} not found')
        return None
