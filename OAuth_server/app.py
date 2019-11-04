from flask import Flask, request
from collections import namedtuple
from datetime import datetime, timedelta
import redis
import json
import jwt

app = Flask(__name__)

''' We assume that our client app already registered an account
    with information: 
         {'client_id': '1234',
          'client_secret': 'qwerty'} 
    This account is saved in database with the others '''

rdb = redis.Redis(host='redis', port=6379)
rdb.mset({
    '1234': 'qwerty',
    'id1': 'pass1',
    'id2': 'pass2',
    'id3': 'pass3'
})

@app.route('/home')
def home():
    return "This is OAuth server"

@app.route('/generate_token')
def generate_token():
    """ Generate access token and status for client app"""

    try:
        client_id = request.args.get('client_id')
        client_secret = request.args.get('client_secret')
        scope = request.args.get('scope')

        # Check if client_id matches client_secret
        if rdb.get(client_id).decode('utf-8') != client_secret:
            raise Exception('client_id does not match to client_secret')
        payload = {
        'exp': datetime.utcnow() + timedelta(seconds=5),
        'client_id': client_id,
        'scope': scope
        }
        encoded_token = jwt.encode(payload, key='encode_key', algorithm='HS256')
        return json.dumps({
            'access_token': encoded_token.decode('utf-8'),
            'status': 'OK'
        })
    except Exception as e:
        return json.dumps({
            'status': 'ERROR',
            'reason': e
        })

@app.route('/validate_token')
def validate_token():
    ''' Validate access token received from resource server'''

    try:
        payload = jwt.decode(request.headers['access_token'].encode('utf-8'), key='encode_key')
        return json.dumps({
            'client_id': payload['client_id'],
            'scope': payload['scope'],
            'status': 'OK'
        })
    except jwt.ExpiredSignatureError:
        return json.dumps({
            'status': 'ERROR',
            'reason': 'Access token expired'
        })
    except jwt.InvalidTokenError:
        return json.dumps({
            'status': 'ERROR',
            'reason': 'Invalid token'
        })

if __name__ == '__main__':
    app.run(port='8000')