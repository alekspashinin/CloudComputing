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

# GENERAL IMPORTS
import sys
import time
import boto3
import statistics
import SenderS3 as SS3


# CALCULATION OF MIN, MAX, AVERAGE AND MEDIAN
def mathCalculate(valuesList):
    answer = [min(valuesList), max(valuesList), sum(valuesList) / len(valuesList), statistics.median(valuesList)]
    return (answer)


# DELETE PREVIUS MESSAGES IF NEED IT
def resetMessages(queue):
    messages = queue.receive_messages()
    print('Number of messages received: ', len(messages))
    for message in messages:
        queue.purge()
        print('Number of messages received: ', len(messages))


# STRING TO LIST
def stringToList(entryList):
    workString = entryList
    workList = workString.split()
    mapObject = map(float, workList)
    resultList = list(mapObject)
    return resultList


# LIST TO STRING
def listToString(entryList):
    # initialize an empty string
    resultList = " "
    # return string
    return (resultList.join(map(str, entryList)))


# CREATE THE QUEUE, GET MESSAGE, CALCULATION AND SEND MESSAGE
sqs = boto3.resource('sqs')
s3 = boto3.resource('s3')
bucket = s3.Bucket('mybucketnumber1')
key = 'CloudLogs.txt'
print('Received: ')
queue = sqs.create_queue(QueueName='requestQueue3')
# resetMessages(queue)
while True:
    messages = queue.receive_messages()
    print('Number of messages received: ', len(messages))
    for message in messages:
        print('Received: ', message.body)
        time.sleep(5)
        resultList = stringToList(message.body)
        message.delete()
        print('Result of Calculation: ', mathCalculate(resultList))
        sendList = listToString(mathCalculate(resultList))
        print('Send Message: ', sendList)
        queue = sqs.get_queue_by_name(QueueName='responseQueue3')
        # Create a new message
        response = queue.send_message(MessageBody=sendList)
        SS3.write_logs(sendList, 'mybucketnumber1', key)
        sys.exit("Stop code")

# GENERAL MAIN
if __name__ == "__main__":
    print("Hello World!")
