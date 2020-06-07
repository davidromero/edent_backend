import datetime
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)

mandatory_fields = ['first_name', 'last_name', 'patient_uid', 'clinic_location', 'start_time']
available_locations = ['chiquimula', 'jocotan']
non_editables = ['uid', 'created_by', 'created_timestamp', 'modified_by', 'modified_timestamp']
all_fields = ['patient_uid', 'first_name', 'last_name', 'clinic_location', 'start_time', 'duration', 'treatment_name']


def validate_appointment_fields(new_appointment):
    if not has_mandatory_fields(new_appointment):
        return False
    if not validate_mandatory_fields(new_appointment):
        return False
    return True


def validate_mandatory_fields(appointment):
    if len(appointment['first_name']) < 3 or len(appointment['first_name']) > 99:
        logger.error('First name is invalid')
        return False
    if len(appointment['last_name']) < 3 or len(appointment['last_name']) > 99:
        logger.error('Last name is invalid')
        return False
    if appointment['clinic_location'] not in available_locations:
        logger.error('Clinic location is invalid')
        return False
    if not validate_datetime(appointment['start_time']):
        return False
    return True


def has_mandatory_fields(treatment):
    for mandatory_key in mandatory_fields:
        if mandatory_key not in treatment.keys():
            logger.error('Mandatory field missing: ' + mandatory_key)
            return False
        mandatory_value = treatment[mandatory_key].strip()
        print(mandatory_value)
        if mandatory_value == '-' or None:
            logger.error('Mandatory field is blank: ' + mandatory_key)
            return False
    return True


def validate_datetime(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%dT%H:%M:%S')
        return True
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DDTHH:mm:ss")
