from chalice import CORSConfig

RATES_TABLE_NAME = 'treatment_rates_chiquimula'
TABLE_NAME = 'edent_treatments_dev'
AWS_DEFAULT_REGION = 'us-east-1'


cors_config = CORSConfig(
    allow_origin='*'
)