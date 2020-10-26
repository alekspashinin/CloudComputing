import atexit
import io
import logging

import boto3


def write_logs(body, bucket, key):
    s3 = boto3.client("s3")
    s3.put_object(Body=body, Bucket=bucket, Key=key)


log = logging.getLogger("S3 Logs")
log_stringio = io.StringIO()
handler = logging.StreamHandler(log_stringio)
log.addHandler(handler)

atexit.register(write_logs, body=log_stringio.getvalue(), bucket="testName", key="testKey")

log.info("S3 Test")

quit()