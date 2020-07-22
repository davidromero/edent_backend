import logging

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

available_locations = ['chiquimula', 'jocotan']
treatment_type = ['operatoria', 'endodoncia', 'cirugia', 'seguro', 'ortodoncia']
all_fields = ['patient', 'treatment_type', 'checkout']


def validate_checkout_fields(new_treatment):
    if not validate_mandatory_fields(new_treatment):
        return False
    return True


def validate_mandatory_fields(checkout):
    patient = checkout['patient']
    treatments = checkout['checkout']
    if len(patient['first_name']) < 3 or len(patient['first_name']) > 99:
        logger.error('First name is invalid')
        return False
    if len(patient['last_name']) < 3 or len(patient['last_name']) > 99:
        logger.error('Last name is invalid')
        return False
    if patient['clinic_location'] not in available_locations:
        logger.error('Clinic location is invalid')
        return False
    if checkout['treatment_type'] not in treatment_type:
        logger.error('Treatment type is invalid')
        return False
    if len(treatments) == 0:
        logger.error('Treatment list is empty')
        return False
    return True
