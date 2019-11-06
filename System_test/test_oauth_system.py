import pytest
import requests
import json

def test_send_current_time_request(config):
    res = requests.get(config.oauth_client + '/current_time')
    res_json = res.json()
    assert res_json['status'] == config.valid