import datetime

mandatory_fields = ['first_name', 'last_name', 'birthday', 'sex', 'clinic_location', 'visit_reason', 'phone_number']
available_locations = ['chiquimula', 'jocotan', 'amatitlan', 'guatemala']
genders = ['male', 'female']
visit_reasons = ['ortodoncia', 'odontologia']
non_editables = ['uid', 'created_by', 'created_timestamp', 'modified_by', 'modified_timestamp', 'active']
all_fields = ['first_name', 'last_name', 'birthday', 'sex', 'clinic_location', 'visit_reason', 'phone_number', 'address', 'email']

def validate_patient_fields(new_patient):
    if not has_mandatory_fields(new_patient):
        return False
    if not validate_mandatory_fields(new_patient):
        return False
    return True


def validate_mandatory_fields(patient):
    if len(patient['first_name']) < 3 or len(patient['first_name']) > 99:
        return False
    if len(patient['last_name']) < 3 or len(patient['last_name']) > 99:
        return False
    if patient['clinic_location'] not in available_locations:
        print('Clinic location is invalid')
        return False
    if patient['sex'] not in genders:
        print('Sex is invalid')
        return False
    if patient['visit_reason'] not in visit_reasons:
        print('Visit reason is invalid')
        return False
    if not validate_birthday(patient['birthday']):
        return False
    return True


def validate_update(body):
    for key in body.keys():
        if key in non_editables:
            print('Non editable is being changed')
            return False
    return True


def has_mandatory_fields(patient):
    for mandatory_key in mandatory_fields:
        if mandatory_key not in patient.keys():
            print('Mandatory field missing: ' + mandatory_key)
            return False
        mandatory_value = patient[mandatory_key].strip()
        if mandatory_value is '' or None:
            print('Mandatory field is blank: ' + mandatory_key)
            return False
    return True


def validate_birthday(date_time_str):
    try:
        birthday_date = datetime.datetime.strptime(date_time_str, '%Y-%m-%d')
    except ValueError:
        print('Invalid birthday format')
        return False
    today = datetime.datetime.now()
    age = (today - birthday_date).days / 365
    if age < 1 or age > 100:
        print('Ages is inconsistent')
        return False
    return True
