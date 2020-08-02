from chalice import Response

response_headers = {'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'}


def get_base_res():
    return Response(
        status_code=200,
        body={'status': 200, 'payload': 'eDent appointments service running...'},
        headers=response_headers
    )


def get_appointments_list(appointment_list):
    if appointment_list is not None:
        return Response(
            status_code=200,
            body={
                'status': 200,
                'payload': appointment_list
            },
            headers=response_headers
        )
    else:
        return not_found(None)


def get_response(response, uid):
    if response is None:
        return not_found(uid)
    else:
        return get_success(response)


def get_success(response):
    return Response(
        status_code=200,
        body={
            'status': 200,
            'payload': response
        },
        headers=response_headers
    )


def not_found(uid):
    message = '{} not found'.format(uid)
    return Response(
        status_code=404,
        body={
            'status': 404,
            'payload': message
        },
        headers=response_headers
    )


def post_response(new_item_id):
    if new_item_id is not None:
        return post_success(new_item_id)
    else:
        return post_fail()


def post_success(uid):
    return Response(
        status_code=201,
        body={
            'status': 201,
            'payload': uid
        },
        headers=response_headers
    )


def post_fail():
    return Response(
        status_code=400,
        body={
            'status': 400,
            'payload': 'Appointment could not be inserted.'
        },
        headers=response_headers
    )


def delete_response(response, uid):
    if isinstance(response, int):
        if response == 404:
            return not_found(uid)
        elif response == 400:
            return delete_fail(uid)
    else:
        if response['HTTPStatusCode'] == 200:
            return delete_success(uid)
    return delete_fail(uid)


def delete_success(uid):
    message = '{} was correctly deleted'.format(uid)
    return Response(
        status_code=204,
        body={
            'status': 204,
            'payload': message
        },
        headers=response_headers
    )


def delete_fail(uid):
    message = '{} failed to delete'.format(uid)
    return Response(
        status_code=400,
        body={
            'status': 400,
            'payload': message
        },
        headers=response_headers
    )

def edit_response(response, uid):
    if isinstance(response, int):
        if response == 404:
            return not_found(uid)
        elif response == 400:
            return edit_fail(uid)
    else:
        if response['HTTPStatusCode'] == 200:
            return edit_success(uid)
    return edit_fail(uid)


def edit_success(uid):
    message = '{} was correctly edited'.format(uid)
    return Response(
        status_code=204,
        body={
            'status': 204,
            'payload': message
        },
        headers=response_headers
    )


def edit_fail(uid):
    message = '{} failed to edit'.format(uid)
    return Response(
        status_code=400,
        body={
            'status': 400,
            'payload': message
        },
        headers=response_headers
    )
