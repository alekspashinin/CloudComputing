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
import queue

from flask import Flask, render_template, request, send_from_directory, redirect
import time
import boto3
from threading import Thread
from werkzeug.utils import secure_filename



app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# function to check file extension
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def stringToList(entryList):
    workString = entryList
    workList = workString.split()
    mapObject = map(int, workList)
    resultList = list(mapObject)
    return resultList


@app.route('/')
def main():
    return render_template('app.html')

@app.route('/part1')
def part1():
    return render_template('part1.html')

@app.route('/part1wait', methods=['POST'])
def part1wait():
    print("START RUN")
    sqs = boto3.resource('sqs')
    queue = sqs.create_queue(QueueName='CloudComputingProject8')
    print("START RECEIVE")
    messages = queue.receive_messages()
    while True:
        for message in messages:
            tempos = message.body
            data = list(tempos.split(" "))
            message.delete()
            finalMessage = "<<<<< Received >>>>> Min: {}, Max: {}, Average: {}, Median: {}".format(data[0], data[1], data[2], data[3])
        return render_template('answerpart1.html', message=finalMessage)
    return render_template('part2wait.html', message="Wait answer. Answers for this moment: 0 ")

@app.route('/part2wait', methods=['POST'])
def part2wait():
    print("START RUN")
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName='inbox1')
    print("START RECEIVE")
    messages = queue.receive_messages()
    while True:
        for message in messages:
            tempos = message.body
            message.delete()
            s3 = boto3.client('s3')
            s3.download_file('mybucketnumber1', tempos, tempos)
            finalMessage = "<<<<< Received >>>>> Modified file name: {}, Image downloaded".format(tempos)
        return render_template('answerpart2.html', message=finalMessage)
    return render_template('part2wait.html', message="Wait answer. Answers for this moment: 0 ")

@app.route('/part2')
def part2():
    return render_template('part2.html')

@app.route('/answerpart1')
def answerpart1():
    return render_template('answerpart1.html')

@app.route('/answerpart2')
def answerpart2():
    return render_template('answerpart2.html')

@app.route("/part2", methods=["POST"])
def create():
    # check whether an input field with name 'user_file' exist
    if 'user_file' not in request.files:
        return render_template('part2.html', message='No user_file key in request.files')

    # after confirm 'user_file' exist, get the file from input
    file = request.files['user_file']
    keyfile = request.form['keyfile']
    print(keyfile)
    if keyfile is None:
        return render_template('part2.html', message='No keyfile in request.form')
    # check whether a file is selected
    if file.filename == '':
        return render_template('part2.html', message='No selected file')

    # check whether the file extension is allowed (eg. png,jpeg,jpg,gif)
    if file and allowed_file(file.filename):
        #output = upload_file_to_s3(file)
        if request.method == 'POST':
            if file:
                filename = secure_filename(file.filename)
                file.save(filename)
                print(keyfile)
                s3 = boto3.client('s3')
                s3.upload_file(
                    Bucket='mybucketnumber1',
                    Filename=filename,
                    Key=keyfile
                )
                sqs = boto3.resource('sqs')
                message = "{} mybucketnumber1".format(keyfile)
                queue = sqs.get_queue_by_name(QueueName='outbox1')
                response = queue.send_message(MessageBody=message)
                s3 = boto3.resource('s3')
                queue = sqs.create_queue(QueueName='inbox1')
                return render_template('part2wait.html', message='Success upload!!! Wait for key...')

        # upload failed, redirect to upload page
        else:
            return render_template('part2.html', message='Unable to upload, try again')

    # if file extension not allowed
    else:
        return render_template('part2.html', message="File type not accepted,please try again")

@app.route('/send', methods=['POST'])
def send():
    if request.method == 'POST':
        sqs = boto3.resource('sqs')
        StringFromUser = request.form['num1']
        queue = sqs.get_queue_by_name(QueueName='CloudComputingProject7')

        # Create a new message
        response = queue.send_message(MessageBody=StringFromUser)
        return render_template('part1wait.html', message="Wait answer. Answers for this moment: 0 ")


if __name__ == ' __main__':
    app.debug = True
    app.run()