import logging

logging.basicConfig()
logger = logging.getLogger(__name__)

mandatory_fields = ['first_name', 'last_name', 'patient_uid', 'clinic_location', 'treatment_type', 'treatment_name',
                    'treatment_price', 'treatment_uid']
available_locations = ['chiquimula', 'jocotan']
treatment_type = ['operatoria', 'endodoncia', 'cirugia', 'seguro']
non_editables = ['uid', 'created_by', 'created_timestamp', 'modified_by', 'modified_timestamp']
all_fields = ['patient_uid', 'first_name', 'last_name', 'clinic_location', 'treatment_type', 'treatment_name',
              'treatment_price', 'treatment_uid', 'checkout_uid']


def validate_treatment_fields(new_treatment):
    if not has_mandatory_fields(new_treatment):
        return False
    if not validate_mandatory_fields(new_treatment):
        return False
    return True


def validate_mandatory_fields(treatment):
    if len(treatment['first_name']) < 3 or len(treatment['first_name']) > 99:
        logger.error('First name is invalid')
        return False
    if len(treatment['last_name']) < 3 or len(treatment['last_name']) > 99:
        logger.error('Last name is invalid')
        return False
    if treatment['clinic_location'] not in available_locations:
        logger.error('Clinic location is invalid')
        return False
    if treatment['treatment_type'] not in treatment_type:
        logger.error('Treatment type is invalid')
        return False
    if len(treatment['treatment_name']) < 3 or len(treatment['treatment_name']) > 50:
        logger.error('Treatment name is invalid')
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
