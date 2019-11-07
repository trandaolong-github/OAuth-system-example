from datetime import datetime, timedelta
import pytest
import requests
import json
import time


def test_send_epoch_time_request_to_client_app(config):
    res = requests.get(config.oauth_client + '/epoch_time')
    res_json = res.json()
    assert res_json['status'] == config.valid
    assert time.time() - res_json['epoch_time'] < 0.01


def test_send_current_time_request_to_client_app(config):
    res = requests.get(config.oauth_client + '/current_time')
    res_json = res.json()
    assert res_json['status'] == config.valid
    current_time = datetime.strptime(res_json['current_time'], '%Y-%m-%dT%H:%M:%S.%f')
    assert datetime.today() - current_time < timedelta(seconds=0.05)


def test_send_token_request_to_oauth_server_with_wrong_client_secret(config):
    params = {
        'client_id': config.client_id,
        'client_secret': 'wrongsecret',
        'scope': 'current_time'
    }
    res_oauth = requests.get(config.oauth_server + '/generate_token', params=params)
    res_oauth_json = res_oauth.json()
    assert res_oauth_json['status'] == config.error
    assert res_oauth_json['reason'] == config.wrong_secret_msg


def test_expired_token(config):
    params = {
        'client_id': config.client_id,
        'client_secret': config.client_secret,
        'scope': 'current_time'
    }
    res = requests.get(config.oauth_server + '/generate_token', params=params)
    res_json = res.json()
    # Sleep more than 5s to make token expired
    time.sleep(6)
    res = requests.get(config.oauth_server + '/validate_token', headers={'access_token': res_json['access_token']})
    res_json = res.json()
    assert res_json['status'] == config.error
    assert res_json['reason'] == config.expired_token_msg