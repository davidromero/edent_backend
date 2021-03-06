import logging
import re

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

mandatory_fields = ['first_name', 'last_name', 'clinic_location', 'phone_number']
available_locations = ['chiquimula', 'jocotan', 'amatitlan', 'guatemala']
non_editables = ['uid', 'created_by', 'created_timestamp', 'modified_by', 'modified_timestamp', 'active']
all_fields = ['patient_uid', 'first_name', 'last_name', 'clinic_location', 'address', 'email', 'phone_number', 'secondary_phone']


def validate_contact_fields(new_contact):
    if not has_mandatory_fields(new_contact):
        return False
    if not validate_mandatory_fields(new_contact):
        return False
    if not validate_optional_fields(new_contact):
        return False
    return True


def validate_mandatory_fields(contact):
    if len(contact['first_name']) < 3 or len(contact['first_name']) > 99:
        logger.error('First name is invalid')
        return False
    if len(contact['last_name']) < 3 or len(contact['last_name']) > 99:
        logger.error('Last name is invalid')
        return False
    if contact['clinic_location'] not in available_locations:
        logger.error('Clinic location is invalid')
        return False
    if 'phone_number' in contact.keys() and not validate_phone_number(contact['phone_number']):
        return False
    return True


def validate_optional_fields(contact):
    if 'email' in contact.keys() and not validate_email(contact['email']):
        logger.error("Invalid email")
        return False
    return True


def validate_update(body):
    for key in body.keys():
        if key in non_editables:
            logger.error('Non editable is being changed')
            return False
    return True


def has_mandatory_fields(contact):
    for mandatory_key in mandatory_fields:
        if mandatory_key not in contact.keys():
            logger.error('Mandatory field missing: ' + mandatory_key)
            return False
        mandatory_value = contact[mandatory_key].strip()
        if mandatory_value == '-' or None:
            logger.error('Mandatory field is blank: ' + mandatory_key)
            return False
    return True


def validate_email(email):
    if email == '-' or None:
        return True
    if re.match(r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email, re.IGNORECASE):
        return True
    return False


def validate_phone_number(phone_number):
    phone_number = str(phone_number).strip(' ')
    if phone_number.isdigit() and len(phone_number) == 8:
        return True
    return False
