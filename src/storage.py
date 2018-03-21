import boto3

s3_client = boto3.client('s3')

bucket = 'py3readiness'

metadata = {
    "CacheControl": "max-age=21600, public"  # 6 hours
}
