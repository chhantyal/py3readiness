import boto3

s3_client = boto3.client('s3')

bucket = 'uhura.de.public'

metadata = {
    "Cache Control": "max-age=21600, public"  # 6 hours
}

BASE_URL = 'https://pypi.python.org/pypi'
