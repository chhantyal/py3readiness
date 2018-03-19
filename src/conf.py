import os

import boto3
from botocore.client import Config

s3_client = boto3.client('s3',
                         aws_access_key_id=os.environ['S3_ACCESS_KEY'],
                         aws_secret_access_key=os.environ['S3_ACCESS_KEY'],
                         config=Config(signature_version='s3v4')
                         )

bucket = 'py3readiness'

metadata = {
    "CacheControl": "max-age=21600, public"  # 6 hours
}

BASE_URL = 'https://pypi.python.org/pypi'
