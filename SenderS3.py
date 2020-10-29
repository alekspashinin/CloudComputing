import atexit
from datetime import datetime

import boto3


def write_logs(body, bucket, key):
    s3 = boto3.client("s3")
    now = datetime.now()
    dataTime = now.strftime("%d/%m/%Y %H:%M:%S")
    content = "{} {}".format(dataTime, body)
    response = s3.put_object(
        Bucket=bucket,
        Body=content,
        Key=key
    )