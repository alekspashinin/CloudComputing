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
from PIL import Image, ImageEnhance  # NOT ERROR, PIL IS INSTALLED ON AWS SERVER
import sys
import boto3
import time

# GENERAL CODE WITH COMMENTS
sqs = boto3.resource('sqs')
s3 = boto3.resource('s3')
queue = sqs.create_queue(QueueName='outbox1')
while True:
    print("Wait for images...")
    messages = queue.receive_messages()
    for message in messages:
        # WATING FOR RECIEVING A REQUEST FROM WEB APP FOR IMAGE PROCCESING
        print("New request for image processing is recieved!")
        tempos = message.body
        resultList = list(tempos.split(" "))
        message.delete()
        key = resultList[0]
        bucketName = resultList[1]
        myBucket = s3.Bucket(bucketName)
        myBucket.download_file(key, 'image.jpg')
        time.sleep(5)

        # IMAGE PROCCESSING AND SAVING NEW IMAGE
        print("Image is downloaded and now it is under processing")
        im = Image.open('image.jpg')
        enh = ImageEnhance.Contrast(im)
        enh.enhance(1.8).save('new_image.jpg')
        time.sleep(5)

        # UPLOADING THE NEW IMAGE IN A NEW BUCKET WITH A NEW KEY
        print("Image processed and now it is being prepared to be stored in s3 bucket")
        new_key = "newImage1.jpg"
        myBucket.upload_file('new_image.jpg', new_key)
        time.sleep(1)

        # SENDING QUEUE TO WEB APP FOR INFORMING
        queue = sqs.get_queue_by_name(QueueName='inbox1')
        response = queue.send_message(MessageBody=new_key)
        time.sleep(1)
        print("The processed image is stored and the web app is informed")
        sys.exit("Stop code")

# GENERAL MAIN
if __name__ == "__main__":
    print("Hello World!")
