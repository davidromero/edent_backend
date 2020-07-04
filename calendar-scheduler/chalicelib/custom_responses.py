def make_response(event_list):
    appointments = []
    for event in event_list:
        appointment = {
            'id': event['id'],
            'link': event['htmlLink'],
            'title': event['summary'],
            'start': event['start'],
            'end': event['end'],
        }
        appointments.append(appointment)
    return appointments


def get_appointments_list(appointment_list):
    if appointment_list is not None:
        return {
            'status': 200,
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
        'status': 404,
        'body': {
            'status': 404,
            'payload': message
        }
    }
