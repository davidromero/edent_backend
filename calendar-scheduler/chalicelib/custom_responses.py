
def get_appointments_list(appointment_list):
    if appointment_list is not None:
        return {
            'status':200,
            'body': {
                'status': 200,
                'payload': appointment_list
            }
        }
    else:
        return not_found(None)


def not_found(uid):
    message = '{} not found'.format(uid)
    return {
        'status':404,
        'body':{
            'status': 404,
            'payload': message
        }
    }

