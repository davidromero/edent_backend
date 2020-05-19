from chalice import Response

response_headers = {'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'}


def get_base_res():
    return Response(
        status_code=200,
        body={'status': 200, 'payload': 'eDent treatments service running...'},
        headers=response_headers
    )


def get_treatment_list(treatment_list):
    if treatment_list is not None:
        return Response(
            status_code=200,
            body={
                'status': 200,
                'payload': treatment_list
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


def get_treatment_rates(treatment_list):
    return Response(
        status_code=200,
        body={
            'status': 200,
            'payload': treatment_list
        },
        headers=response_headers
    )
