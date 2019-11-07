import pytest
import requests

class Config(object):
    def __init__(self):
        self.oauth_client = 'http://oauth_client:5000'
        self.oauth_server = 'http://oauth_server:8000'
        self.valid = 'OK'
        self.error = 'ERROR'
        self.client_id = '1234'
        self.client_secret = 'qwerty'
        self.wrong_secret_msg = 'client_id does not match to client_secret'
        self.expired_token_msg = 'Access token expired'

@pytest.fixture(scope='session')
def config():
    config = Config()
    return config