from chalice import CORSConfig

TABLE_NAME = 'edent_checkout_dev'
AWS_DEFAULT_REGION = 'us-east-1'


cors_config = CORSConfig(
    allow_origin='*'
)