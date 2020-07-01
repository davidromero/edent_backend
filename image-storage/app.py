from boto3 import s3
from chalice import Chalice, Response
import boto3

app = Chalice(app_name='image-storage')

BUCKET = 'images.edent.backend'
s3_client = boto3.client('s3')
s3 = boto3.resource('s3')
bucket = s3.Bucket('images.edent.backend')


@app.route('/upload/{file_name}', methods=['PUT'],
           content_types=['image/jpeg', 'image/jpg'])
def upload_to_s3(file_name):
    # get raw body of PUT request
    body = app.current_request.raw_body

    # write body to tmp file
    tmp_file_name = '/tmp/' + file_name
    with open(tmp_file_name, 'wb') as tmp_file:
        tmp_file.write(body)

    # upload tmp file to s3 bucket
    s3_client.upload_file(tmp_file_name, BUCKET, file_name)

    # Check if file is uploaded
    objs = list(bucket.objects.filter(Prefix=file_name))
    if len(objs) > 0 and objs[0].key == file_name:
        public_url = 'https://s3.amazonaws.com/' + BUCKET + '/' + file_name
        return Response(body=public_url,
                        status_code=200,
                        headers={'Content-Type': 'text/plain'})
    else:
        return Response(body='Error Img not Uploaded',
                        status_code=404,
                        headers={'Content-Type': 'text/plain'})
