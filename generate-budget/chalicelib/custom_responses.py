from chalice import Response

response_headers = {'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type'}


def post_response(new_item_id):
    if new_item_id is not None:
        return post_success(new_item_id)
    else:
        return post_fail()


def post_success(url):
    return Response(
        status_code=201,
        body={
            'status': 201,
            'payload': url
        },
        headers=response_headers
    )


def post_fail():
    return Response(
        status_code=400,
        body={
            'status': 400,
            'payload': 'Budget could not be inserted.'
        },
        headers=response_headers
    )


def get_base_res():
    return Response(
        status_code=200,
        body={'status': 200, 'payload': 'eDent generate-budget service running...'},
        headers=response_headers
    )
