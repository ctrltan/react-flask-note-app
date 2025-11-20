import pytest
from unittest.mock import MagicMock
from flask import Flask

def test_index_route(client):
    response = client.get('/')
    data = response.get_json()

    assert response.status_code == 200
    assert 'message' in data


