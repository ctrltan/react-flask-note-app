from dotenv import load_dotenv
import os
import pytest
from note_app.server import create_app
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta

def pytest_configure():
    if os.getenv('CI') != 'true':
        dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.test.env')
        load_dotenv(dotenv_path=dotenv_path, override=True)

@pytest.fixture(scope='session')
def client():
    app = create_app(testing=True)
    
    with app.test_client() as client:
        with app.app_context():
            yield client

@pytest.fixture
def cookies():
    access_claims = {'user_id': 1, 'session_id': 1, 'username': 'janedoe'}
    
    access_token = create_access_token('1', expires_delta=timedelta(minutes=15), additional_claims=access_claims)
    refresh_token = create_refresh_token('1', expires_delta=False)

    return refresh_token, access_token

@pytest.fixture
def invalid_cookies():
    access_claims = {'user_id': 1, 'session_id': None, 'username': 'janedoe'}
    
    access_token = create_access_token('1', expires_delta=timedelta(minutes=15), additional_claims=access_claims)
    refresh_token = create_refresh_token(None, expires_delta=False)

    return refresh_token, access_token
