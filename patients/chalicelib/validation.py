import datetime
import logging

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

mandatory_fields = ['first_name', 'last_name', 'sex', 'birthday', 'clinic_location', 'visit_reason', 'phone_number', 'doctor_names']
available_locations = ['chiquimula', 'jocotan']
genders = ['male', 'female']
doctor_names = ['dra. hilda peralta', 'dra. rocio peralta']
visit_reasons = ['operatoria', 'ortodoncia', 'endodoncia', 'cirugia', 'seguro']
non_editables = ['uid', 'created_by', 'created_timestamp', 'modified_by', 'modified_timestamp', 'active']
all_fields = ['first_name', 'last_name', 'birthday', 'sex', 'clinic_location', 'visit_reason', 'phone_number',
              'address', 'email', 'doctor_names']


def validate_patient_fields(new_patient):
    if not has_mandatory_fields(new_patient):
        return False
    if not validate_mandatory_fields(new_patient):
        return False
    return True


def validate_mandatory_fields(patient):
    if len(patient['first_name']) < 3 or len(patient['first_name']) > 99:
        logger.error('First name is invalid')
        return False
    if len(patient['last_name']) < 3 or len(patient['last_name']) > 99:
        logger.error('Last name is invalid')
        return False
    if patient['clinic_location'] not in available_locations:
        logger.error('Clinic location is invalid')
        return False
    if patient['sex'] not in genders:
        logger.error('Sex is invalid')
        return False
    if patient['visit_reason'] not in visit_reasons:
        logger.error('Visit reason is invalid')
        return False
    for doctor_name in patient['doctor_names']:
        if doctor_name.lower() not in doctor_names:
            logger.error(f'Doctor name is invalid: {doctor_name}')
            return False
    if not validate_birthday(patient['birthday']):
        logger.error('Birthday is invalid')
        return False
    return True


def validate_update(body):
    for key in body.keys():
        if key in non_editables:
            logger.error('Non editable is being changed')
            return False
    return True


def has_mandatory_fields(patient):
    for mandatory_key in mandatory_fields:
        if mandatory_key not in patient.keys():
            logger.error('Mandatory field missing: ' + mandatory_key)
            return False
        if isinstance(patient[mandatory_key], list):
            mandatory_value = patient[mandatory_key]
        else:
            mandatory_value = patient[mandatory_key].strip()
        if mandatory_value == '-' or None:
            logger.error('Mandatory field is blank: ' + mandatory_key)
            return False
    return True


def validate_birthday(date_time_str):
    if date_time_str == '-':
        return True
    try:
        birthday_date = datetime.datetime.strptime(date_time_str, '%Y-%m-%d')
    except ValueError:
        logger.error('Invalid birthday format')
        return False
    today = datetime.datetime.now()
    age = (today - birthday_date).days / 365
    if age < 1 or age > 100:
        logger.error('Age is inconsistent')
        return False
    return True
