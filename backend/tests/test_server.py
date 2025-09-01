import pytest
from pytest_mock import MockerFixture
from flask import Flask
from note_app.server import app

"""
Home page route
    - 

DB Decorator
    -

"""

@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

def test_index_route(client):
    response = client.get('/')
    data = response.get_json()

    assert response.status_code == 200
    assert 'message' in data


