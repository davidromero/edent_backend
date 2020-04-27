from chalice import Response

response_headers = {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type'}


def get_base_res():
    return Response(
        status_code=200,
        body={'status': 200, 'payload': 'eDent whatsapp service running...'},
        headers=response_headers
    )
