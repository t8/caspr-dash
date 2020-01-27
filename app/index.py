import os
import time
import json
from flask import Flask, render_template, make_response
from functools import wraps, update_wrapper
from datetime import datetime
from flask_socketio import SocketIO, emit
from serialCommunicationCommands import * as sCommands

app = Flask(__name__)
socketio = SocketIO(app)

global stepperSpeed
global stepperDirection


@socketio.on('updateSettings')  # Decorator to catch an event called "my event":
def receive(data):  # test_message() is the event callback function.
    #    print(map(lambda x: x.encode('utf-8'), data))
    fixedData = json.loads(json.dumps(eval(json.dumps(data))))
    newSpeed = float(fixedData['stepperSpeed'])
    print(fixedData["stepperSpeed"])
    testdata = ["<BOTHSTEP," + str(newSpeed) + ",FOR>"]
    sCommands.runTest(testdata)
    emit('response', {'data': 'got it!'})  # Trigger a new event called "my response"


# @app.before_first_request
# def activate_job():
#    def run_job():
#        while True:
#            refreshControls()
#            print("refreshing controls")
#            time.sleep(3)
#
#    thread = threading.Thread(target=run_job)
#    thread.start()

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, view)


@app.route('/')
@nocache
def home():
    return render_template('dashboard.html', speed=0, direction=90)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=80, debug=True)
#    app.run(host='0.0.0.0', port=80, debug=True)

#
#
#    testData = []
#    testData.append("<LEFTSTEP,3000.0,FOR>")
#    testData.append("<RIGHTSTEP,3000.0,FOR>")
#    testData.append("<HALT,0,ARB>")
#    testData.append("<BOTHSTEP,3000.0,BCK>")
#
#    runTest(testData)
#
#
#    ser.close
