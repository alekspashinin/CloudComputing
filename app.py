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

class Compute2(Thread):
    def __init__(self, request):
        Thread.__init__(self)
        self.request = request

    def download(self):
        s3 = boto3.client('s3')
        s3.download_file('your_bucket',self,'/Users/Aleksei Pashinin/Desktop'+self)
        data="Downloaded! Saved in /Users/Aleksei Pashinin/Desktop"
        return render_template('part2.html', message=data)

class Compute1(Thread):
    def __init__(self, request):
        Thread.__init__(self)
        self.request = request

    def receive(self):
        messages = queue.receive_messages()
        while True:
            for message in messages:
                data = stringToList(message.body)
                message.delete()
            return (data)

    def run(self):
        sqs = boto3.resource('sqs')
        queue = sqs.create_queue(QueueName='CloudComputingProject8')
        data = receive()
        thread_b = Compute2(request.__copy__(data))
        thread_b.start()
        return render_template('part2.html', message=data)


@app.route('/')
def main():
    return render_template('app.html')

@app.route('/part1')
def part1():
    return render_template('part1.html')

@app.route('/part2')
def part2():
    return render_template('part2.html')

@app.route("/part2", methods=["POST"])
def receive():
    messages = queue.receive_messages()
    while True:
            for message in messages:
                data = stringToList(message.body)
                message.delete()
            return(data)

def create():
    # check whether an input field with name 'user_file' exist
    if 'user_file' not in request.files:
        return render_template('part2.html', message='No user_file key in request.files')

    if 'keyfile' not in request.form:
        return render_template('part2.html', message='No keyfile in request.form')

    # after confirm 'user_file' exist, get the file from input
    file = request.files['user_file']
    keyfile = request.form['keyfile']
    print(keyfile)
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
                s3.upload_file(
                    Bucket='mybucketnumber1',
                    Filename=filename,
                    Key=keyfile
                )
                thread_a = Compute1(request.__copy__())
                thread_a.start()
                return render_template('part2.html', message='Success upload!!! Wait for key...')

        # upload failed, redirect to upload page
        else:
            return render_template('part2.html', message='Unable to upload, try again')

    # if file extension not allowed
    else:
        return render_template('part2.html', message="File type not accepted,please try again")

@app.route('/send', methods=['POST'])
def send(sum=sum):
    if request.method == 'POST':
        sqs = boto3.resource('sqs')
        StringFromUser = request.form['num1']
        queue = sqs.get_queue_by_name(QueueName='CloudComputingProject7')

        # Create a new message
        response = queue.send_message(MessageBody=StringFromUser)
        return render_template('app.html', sum="Wait answer. Answers for this moment: 0 ")

@app.route('/result', methods=['POST'])
def result(sum=sum):
    if request.method == 'POST':
         sqs = boto3.resource('sqs')
         StringFromUser = request.form['num1']
         queue = sqs.get_queue_by_name(QueueName='CloudComputingProject7')

         # Create a new message
         response = queue.send_message(MessageBody=StringFromUser)
         return render_template('app.html', sum="Wait answer. Answers for this moment: 0 ")

@app.route('/flash/<message>')
def flash(message):
        return render_template('flash.html', msg=message)

        """queue = sqs.create_queue(QueueName='CloudComputingProject8')
        time.sleep(3)
        while True:
            messages = queue.receive_messages()
            print('Wait answer. Answers for this moment: ', len(messages))
            print('Received >>>', messages)
            for message in messages:
                print('Received >>>', message.body)
                resultList = stringToList(message.body)
                message.delete()
                print('Received >>> Min: ', resultList[0], 'Max: ', resultList[1], 'Average: ', resultList[2],
                      'Median: ', resultList[3])
                print('Work done')

        num2 = request.form['num2']
        operation = request.form['operation']

        if operation == 'add':
            sum = float(num1) + float(num2)
            return render_template('app.html', sum=sum)

        elif operation == 'subtract':
            sum = float(num1) - float(num2)
            return render_template('app.html', sum=sum)

        elif operation == 'multiply':
            sum = float(num1) * float(num2)
            return render_template('app.html', sum=sum)

        elif operation == 'divide':
            sum = float(num1) / float(num2)
            return render_template('app.html', sum=sum)
        else:
            return render_template('app.html')
            
            
            
            
                                                    <label for="Operation">Operation</label>
                                        <select class="u-full-width" name="operation">
                                          <option value="add">Add</option>
                                          <option value="subtract">Subtract</option>
                                          <option value="multiply">Multiply</option>
                                          <option value="divide">Divide</option>
                                        </select>
                                        
                                        
                                        
                                        """


if __name__ == ' __main__':
    app.debug = True
    app.run()