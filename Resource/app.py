from flask import Flask, request
from datetime import datetime
import requests
from time import time
import json

app = Flask(__name__)

OAUTH_SERVER = 'http://oauth_server:8000'

@app.route('/home')
def home():
    return "This is Resource server"

@app.route('/current_time')
def get_current_time():
    ''' Return current time to client app'''

    # Get access_token from client app and send validate request to oauth server
    access_token = request.headers['access_token']
    res = requests.get(OAUTH_SERVER + '/validate_token', headers={'access_token': access_token})
    res_json = res.json()

    if res_json['status'] == 'ERROR':
        return json.dumps(res_json)

    return json.dumps({
        'status': 'OK',
        'current_time': datetime.today().isoformat()
    })

@app.route('/epoch_time')
def get_epoch_time():
    ''' Return current epoch time to client app'''

    # Get access_token from client app and send validate request to oauth server
    access_token = request.headers['access_token']
    res = requests.get(OAUTH_SERVER + '/validate_token', headers={'access_token': access_token})
    res_json = res.json()

    if res_json['status'] == 'ERROR':
        return json.dumps(res_json)

    return json.dumps({
        'status': 'OK',
        'epoch_time': time()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='9000')