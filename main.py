import boto3

sqs = boto3.client('sqs', region_name="us-east-1b",
                   aws_access_key_id='KEY_ID',
                   aws_secret_access_key='ACCESS_KEY'
        )
queue_url = ''

#FOR TEST MESSAGE
response = sqs.receive_message(
    QueueUrl=queue_url,
    AttributeNames=[
        'SentTimestamp'
    ],
    MaxNumberOfMessages=1,
    MessageAttributeNames=[
        'All'
    ],
    VisibilityTimeout=0,
    WaitTimeSeconds=0
)

message = response['Messages'][0]
receipt_handle = message['ReceiptHandle']

sqs.delete_message(
    QueueUrl=queue_url,
    ReceiptHandle=receipt_handle
)
print('Received and deleted message: %s' % message)