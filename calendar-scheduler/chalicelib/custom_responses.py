def make_response(event_list):
    appointments = []
    for event in event_list:
        description = ''
        if 'description' in event:
            description = event['description']
        appointment = {
            'id': event['id'],
            'link': event['htmlLink'],
            'title': event['summary'],
            'description': description,
            'start': event['start'],
            'end': event['end'],
        }
        appointments.append(appointment)
    return appointments


def get_appointments_list(appointment_list):
    if appointment_list is not None:
        return {
            'status': 200,
            'body': appointment_list
        }
    else:
        return not_found(None)


def not_found(uid):
    message = '{} not found'.format(uid)
    return {
        'status': 404,
        'body': {
            message
        }
    }
