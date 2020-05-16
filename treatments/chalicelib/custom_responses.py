from chalice import Response

response_headers = {'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'}


def get_base_res():
    return Response(
        status_code=200,
        body={'status': 200, 'payload': 'eDent treatments service running...'},
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
