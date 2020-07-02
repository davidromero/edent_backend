import logging

import boto3
from chalice import Chalice
from chalicelib import custom_responses
from chalicelib.config import BUCKET_NAME

app = Chalice(app_name='image-storage')
app.log.setLevel(logging.DEBUG)

CONTENT_TYPES = ['image/jpeg', 'image/jpg', 'image/png']


@app.route('/', methods=['GET'])
def index():
    return custom_responses.get_base_res()


@app.route('/upload/{file_name}', methods=['PUT'], content_types=CONTENT_TYPES)
def upload_to_s3(file_name):
    body = app.current_request.raw_body

    tmp_file_name = '/tmp/' + file_name
    with open(tmp_file_name, 'wb') as tmp_file:
        tmp_file.write(body)

    s3_client, bucket = get_s3_resources()
    s3_client.upload_file(tmp_file_name, BUCKET_NAME, file_name)

    objs = list(bucket.objects.filter(Prefix=file_name))
    if len(objs) > 0 and objs[0].key == file_name:
        public_url = f'https://s3.amazonaws.com/{BUCKET_NAME}/{file_name}'
        return custom_responses.post_response(public_url)
    else:
        return custom_responses.post_response()


def get_s3_resources():
    s3_client = boto3.client('s3')
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)

    return s3_client, bucket
