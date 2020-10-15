from datetime import time
import boto3


#FOR TEST MESSAGE
SESSIONS_ACCESS_KEY = "key"
SESSIONS_SECRET_KEY = "key"
sess = boto3.session.Session(region_name='us-east-1b',
                             aws_access_key_id=SESSIONS_ACCESS_KEY,
                             aws_secret_access_key=SESSIONS_SECRET_KEY
                             )
sqs = sess.resource("sqs")

queue = sqs.get_queue_by_name(QueueName='myTestQueue.fifo')


while True:
    messages = queue.receive_messages()
    print('Number of messages received: ',len(messages))
    for message in messages:
        print('msg:',message.body)
        message.delete()
    time.sleep(5)