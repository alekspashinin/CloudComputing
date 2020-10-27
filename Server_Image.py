from PIL import Image, ImageEnhance 
import sys
import boto3
import time
# Create the queue. This returns an SQS.Queue instance
sqs = boto3.resource('sqs')
s3 = boto3.resource('s3')
queue = sqs.create_queue(QueueName='outbox')
# resetMessages(queue)
while True:
    messages = queue.receive_messages()
    for message in messages:
        
        #WATING FOR RECIEVING A REQUEST FROM WEB APP FOR IMAGE PROCCESING
        print("New request for image processing is recieved!")
        resultList = message.body.split()
        message.delete()
        key = resultList[0]
        bucket = s3.Bucket(resultList[1])
        bucket.download_file(Key=key, Filename='/home/ubuntu/CloudComputing')
        time.sleep(1)
        
        #IMAGE PROCCESSING AND SAVING NEW IMAGE 
        print("Image is downloaded and now it is under processing")
        im = Image.open( 'image.jpg' )
        enh = ImageEnhance.Contrast(im)
        enh.enhance(1.8).save('new_image.jpg')
        time.sleep(1)
        
      #UPLOADING THE NEW IMAGE IN A NEW BUCKET WITH A NEW KEY  
        print("Image processed and now it is being prepared to be stored in s3 bucket")
        new_key="new key for inbox"
        new_bucket = s3.Bucket('new bucket for input')
        new_bucket.upload_file(Filename='new_image.jpg',Key=new_key)
        time.sleep(1)
        
     #SENDING QUEUE TO WEB APP FOR INFORMING 
        queue = sqs.get_queue_by_name(QueueName='inbox')
        response = queue.send_message(MessageBody=[new_key,resultList[1]])
        time.sleep(1)
        print("The processed image is stored and the web app is informed")
        sys.exit("Stop code")

if __name__ == "__main__":
    print("Hello World!")
