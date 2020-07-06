from os import environ

from chalice import CORSConfig

RATES_TABLE_NAME = environ.get('RATES_TABLE_NAME')
TABLE_NAME = environ.get('TABLE_NAME')
AWS_DEFAULT_REGION = environ.get('AWS_DEFAULT_REGION')

cors_config = CORSConfig(
    allow_origin='*'
)