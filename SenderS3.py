import boto3

s3 = boto3.resource(
    's3',
    region_name='us-east-1b',
    aws_access_key_id='KEY_ID',
    aws_secret_access_key='ACCESS_KEY'
)
content="String content to write to a new S3 file"
s3.Object('CloudProject1bucket', 'log.txt').put(Body=content)