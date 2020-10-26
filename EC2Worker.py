#######################################
#                                     #
#      ***   UJM * EMSE   ***         #
#                                     #
#   Aleksei PASHININ * Hamed RAHIMI   #
#         Jonathan MALLET             #
#                                     #
#         Cloud Computing             #
#             PROJECT                 #
#                                     #
#######################################
import sys
import time
import boto3
import statistics
import SenderS3 as SS3


def mathCalculate(valuesList):
    answer = [min(valuesList), max(valuesList), sum(valuesList) / len(valuesList), statistics.median(valuesList)]
    return (answer)


def resetMessages(queue):
    messages = queue.receive_messages()
    print('Number of messages received: ', len(messages))
    for message in messages:
        queue.purge()
        print('Number of messages received: ', len(messages))


def stringToList(entryList):
    workString = entryList
    workList = workString.split()
    mapObject = map(int, workList)
    resultList = list(mapObject)
    return resultList


def listToString(entryList):
    # initialize an empty string
    resultList = " "
    # return string
    return (resultList.join(map(str, entryList)))


# Starting Project
# TEST PART
# s3 = boto3.resource('s3')
# for bucket in s3.buckets.all():
#    print(bucket.name)
# data = open('clouds.jpg', 'rb')
# s3.Bucket('mybucketnumber1').put_object(Key='clouds.jpg', Body=data)

# Create the queue. This returns an SQS.Queue instance
sqs = boto3.resource('sqs')
s3 = boto3.resource('s3')
bucket = s3.Bucket('mybucketnumber1')
key = 'logs1.txt'
print('Received: ')
queue = sqs.create_queue(QueueName='CloudComputingProject7')
# resetMessages(queue)
while True:
    messages = queue.receive_messages()
    print('Number of messages received: ', len(messages))
    for message in messages:
        print('Received: ', message.body)
        resultList = stringToList(message.body)
        print('Result of Calculation: ', mathCalculate(resultList))
        sendList = listToString(mathCalculate(resultList))
        print('Send Message: ', sendList)
        message.delete()
        queue = sqs.get_queue_by_name(QueueName='CloudComputingProject8')
        # Create a new message
        response = queue.send_message(MessageBody=sendList)
        SS3.writefile(sendList, bucket, key)
        sys.exit("Stop code")

if __name__ == "__main__":
    print("Hello World!")
