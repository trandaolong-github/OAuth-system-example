import pytest
import requests

class Config(object):
    def __init__(self):
        self.oauth_client = 'http://oauth_client:5000'
        self.valid = 'OK'

@pytest.fixture(scope='session')
def config():
    config = Config()
    return config