from chalice import CORSConfig

TABLE_NAME = 'edent_patients_dev'
AWS_DEFAULT_REGION = 'us-east-1'

cors_config = CORSConfig(
    allow_origin='*',
    allow_headers=None,
    max_age=None,
    expose_headers=None,
    allow_credentials=True
)