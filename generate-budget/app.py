import logging
import boto3
import pytz
from datetime import datetime, timedelta
from chalice import Chalice
from chalicelib import custom_responses
from chalicelib.create_pdf import create_pdf
from chalicelib.config import BUCKET_NAME, BUCKET_PREFIX, cors_config

app = Chalice(app_name='generate-budget')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


@app.route('/', methods=['GET'])
def index():
    return custom_responses.get_base_res()


@app.route('/pdf', methods=['POST'], cors=cors_config, content_types=['application/json'])
def add_budget():
    filename = (datetime.now(pytz.timezone('America/Guatemala')) + timedelta(365)).strftime(
        '%d-%m-%Y,%H:%M:%S') + '.pdf'
    body = app.current_request.json_body
    logger.info(body)
    create_pdf(filename, body)

    s3_client, bucket = get_s3_resources()
    s3_client.upload_file('/tmp/' + filename, BUCKET_NAME, filename)

    objs = list(bucket.objects.filter(Prefix=filename))
    if len(objs) > 0 and objs[0].key == filename:
        public_url = f'{BUCKET_PREFIX}/{BUCKET_NAME}/{filename}'
        logger.info(f'Budget successfully saved in {public_url}')
        return custom_responses.post_response(public_url)
    else:
        logger.info('Budget could not be saved')
        return custom_responses.post_response()


def get_s3_resources():
    s3_client = boto3.client('s3')
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)
    return s3_client, bucket
