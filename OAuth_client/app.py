from flask import Flask
import requests
import json

app = Flask(__name__)

ID = '1234'
SECRET = 'qwerty'
OAUTH_SERVER = 'http://localhost:8000'
RESOURCE_SERVER = 'http://localhost:9000'

@app.route('/current_time')
def get_current_time():
    ''' Get current time of resource server'''

    # Request token from Oauth server
    params = {
        'client_id': ID,
        'client_secret': SECRET,
        'scope': 'current_time'
    }
    res_oauth = requests.get(OAUTH_SERVER + '/generate_token', params=params)
    res_oauth_json = res_oauth.json()
    if res_oauth_json['status'] == 'ERROR':
        return json.dumps(res_oauth_json)

    # Send request to resource server for current time
    res_resource = requests.get(RESOURCE_SERVER + '/current_time', headers={'access_token': res_oauth_json['access_token']})
    res_resource_json = res_resource.json()

    return json.dumps(res_resource_json)

@app.route('/epoch_time')
def get_epoch_time():
    ''' Get current epoch time of resource server'''

    # Request token from Oauth server
    params = {
        'client_id': ID,
        'client_secret': SECRET,
        'scope': 'epoch_time'
    }
    res_oauth = requests.get(OAUTH_SERVER + '/generate_token', params=params)
    res_oauth_json = res_oauth.json()
    if res_oauth_json['status'] == 'ERROR':
        return json.dumps(res_oauth_json)

    # Send request to resource server for current epoch time
    res_resource = requests.get(RESOURCE_SERVER + '/epoch_time', headers={'access_token': res_oauth_json['access_token']})
    res_resource_json = res_resource.json()

    return json.dumps(res_resource_json)

if __name__ == '__main__':
    app.run()