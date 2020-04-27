import os

from chalice import CORSConfig

TABLE_NAME = 'edent_messages_dev'
AWS_DEFAULT_REGION = 'us-east-1'
TWILIO_SID = os.environ['TWILIO_SID']
TWILIO_TOKEN = os.environ['TWILIO_TOKEN']

cors_config = CORSConfig(
    allow_origin='*'
)