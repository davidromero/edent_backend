from chalice import Response


def get_active_contacts(contact_list):
    if contact_list is not None:
        return Response(
            status_code=200,
            body={
                'status': 200,
                'payload': contact_list
            },
            headers={
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': 'http://localhost:3000'
            }
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
        headers={
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': 'http://localhost:3000'
        }
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
        headers={
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': 'http://localhost:3000'
        }
    )


def post_fail():
    return Response(
        status_code=400,
        body={
            'status': 400,
            'payload': 'Contact could not be inserted.'
        },
        headers={
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': 'http://localhost:3000'
        }
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
        headers={
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': 'http://localhost:3000'
        }
    )


def edit_fail(uid):
    message = '{} failed to edit'.format(uid)
    return Response(
        status_code=400,
        body={
            'status': 400,
            'payload': message
        },
        headers={
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': 'http://localhost:3000'
        }
    )


def not_found(uid):
    message = '{} not found'.format(uid)
    return Response(
        status_code=404,
        body={
            'status': 404,
            'payload': message
        },
        headers={
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': 'http://localhost:3000'
        }
    )


def get_base_res():
    return Response(
        status_code=200,
        body={'status': 200, 'payload': 'eDent patients service running...'},
        headers={
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': 'http://localhost:3000'
        }
    )
