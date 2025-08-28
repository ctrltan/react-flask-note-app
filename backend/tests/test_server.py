import pytest, pytest_pgsql
from pytest_mock import MockerFixture
from flask import Flask

"""
Home page route
    - 

DB Decorator
    -

"""

@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

def test_index_route(client):
    response = client.get('/')

    assert response.status_code == 200
    assert 'message' in response.data


