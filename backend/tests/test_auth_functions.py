import pytest
from unittest.mock import MagicMock
from flask_jwt_extended import decode_token, create_access_token
from datetime import timedelta


def test_email_encryption_success(mocker):
    mock_redis_manager = MagicMock()
    mocker.patch('note_app.helpers.auth_functions.RedisManager', return_value=mock_redis_manager)
    
    test_email = 'janedoe@email.com'

    from note_app.helpers.auth_functions import email_encryption

    encrypted_email = email_encryption(test_email)

    assert encrypted_email != test_email
    assert type(encrypted_email) == str

def test_email_encryption_incorrect_input_failure(mocker):
    mock_redis_manager = MagicMock()
    mocker.patch('note_app.helpers.auth_functions.RedisManager', return_value=mock_redis_manager)

    test_email = 1

    from note_app.helpers.auth_functions import email_encryption
    
    with pytest.raises(Exception):
        email_encryption(test_email)

def test_token_creator_success(client, mocker):
    mock_redis_manager = MagicMock()
    mocker.patch('note_app.helpers.auth_functions.RedisManager', return_value=mock_redis_manager)

    test_payload = {'user_id': '123', 'session_id': '456', 'username': 'janedoe'}

    from note_app.helpers.auth_functions import token_creator

    refresh_token, access_token = token_creator(test_payload)
    refresh_token_payload = decode_token(refresh_token)
    access_token_payload = decode_token(access_token)

    assert 'sub' in refresh_token_payload and refresh_token_payload['sub'] == test_payload['session_id']
    assert 'sub' in access_token_payload and access_token_payload['sub'] == test_payload['user_id']
    assert 'user_id' in access_token_payload and access_token_payload['user_id'] == test_payload['user_id']
    assert 'session_id' in access_token_payload and access_token_payload['session_id'] == test_payload['session_id']
    assert 'username' in access_token_payload and access_token_payload['username'] == test_payload['username']

def test_token_creator_incomplete_payload_failure(client, mocker):
    mock_redis_manager = MagicMock()
    mocker.patch('note_app.helpers.auth_functions.RedisManager', return_value=mock_redis_manager)

    test_payload = {'username': 'janedoe'}

    from note_app.helpers.auth_functions import token_creator

    with pytest.raises(Exception):
        token_creator(test_payload)

def test_token_decoder_success(client, mocker):
    mock_redis_manager = MagicMock()
    mocker.patch('note_app.helpers.auth_functions.RedisManager', return_value=mock_redis_manager)

    test_claims = {'user_id': '123', 'session_id': '456', 'username': 'janedoe'}

    access_token = create_access_token(test_claims['user_id'], expires_delta=timedelta(minutes=10), additional_claims=test_claims)

    from note_app.helpers.auth_functions import token_decoder

    payload = token_decoder(access_token)

    assert type(payload) == dict
    assert 'sub' in payload and payload['sub'] == test_claims['user_id']
    assert 'user_id' in payload and payload['user_id'] == test_claims['user_id']
    assert 'session_id' in payload and payload['session_id'] == test_claims['session_id']
    assert 'username' in payload and payload['username'] == test_claims['username']

def test_token_decoder_success_with_expired_token(client, mocker):
    mock_redis_manager = MagicMock()
    mocker.patch('note_app.helpers.auth_functions.RedisManager', return_value=mock_redis_manager)

    test_claims = {'user_id': '123', 'session_id': '456', 'username': 'janedoe'}

    access_token = create_access_token(test_claims['user_id'], expires_delta=timedelta(seconds=-1), additional_claims=test_claims)

    from note_app.helpers.auth_functions import token_decoder

    payload = token_decoder(access_token)

    assert type(payload) == dict
    assert 'sub' in payload and payload['sub'] == test_claims['user_id']
    assert 'user_id' in payload and payload['user_id'] == test_claims['user_id']
    assert 'session_id' in payload and payload['session_id'] == test_claims['session_id']
    assert 'username' in payload and payload['username'] == test_claims['username']

def test_token_decoder_invalid_token(client, mocker):
    mock_redis_manager = MagicMock()
    mocker.patch('note_app.helpers.auth_functions.RedisManager', return_value=mock_redis_manager)

    from note_app.helpers.auth_functions import token_decoder

    payload = token_decoder('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NjM2NDQ5MDcsImV4cCI6MTc2MzY0ODUwNywianRpIjoiYzI0MGFkMDctMjM1Ni00YTVhLWIwZWUtZDU3ZGUwMjJkMjQ1IiwiaXNzIjoiYXBpLmV4YW1wbGUuY29tIiwic3ViIjoidXNlcl8xMjM4IiwiYXVkIjoiaHR0cHM6Ly9leGFtcGxlLmNvbSJ9.xu2NS1hEiVne72j8sLeRa7n5tKrxqfYtGCdnynwZ5so')

    assert payload == None

def test_decoder_empty_token(client, mocker):
    mock_redis_manager = MagicMock()
    mocker.patch('note_app.helpers.auth_functions.RedisManager', return_value=mock_redis_manager)

    from note_app.helpers.auth_functions import token_decoder

    payload = token_decoder('')

    assert payload == None

def test_create_session_success(mocker):
    mock_redis_manager = MagicMock()
    mocker.patch('note_app.helpers.auth_functions.RedisManager', return_value=mock_redis_manager)
    mock_redis_manager.add_session_key.side_effect = None

    test_session = {'session_id': '123', 'user_id': '456', 'refresh_token': 'token'}

    from note_app.helpers.auth_functions import create_session

    res = create_session(test_session['session_id'], test_session['user_id'], test_session['refresh_token'])

    assert res == True

def test_create_session_failure(mocker):
    mock_redis_manager = MagicMock()
    mocker.patch('note_app.helpers.auth_functions.RedisManager', return_value=mock_redis_manager)
    mock_redis_manager.add_session_key.side_effect = Exception

    test_session = {'session_id': '123', 'user_id': '456', 'refresh_token': 'token'}

    from note_app.helpers.auth_functions import create_session

    res = create_session(test_session['session_id'], test_session['user_id'], test_session['refresh_token'])

    assert res == False

def test_remove_session_success(mocker):
    mock_redis_manager = MagicMock()
    mocker.patch('note_app.helpers.auth_functions.RedisManager', return_value=mock_redis_manager)
    mock_redis_manager.valid_session.return_value = True
    mock_redis_manager.delete_session.return_value = True

    from note_app.helpers.auth_functions import remove_session

    res = remove_session('123')

    assert res == True

def test_remove_session_success_if_session_nonexistent(mocker):
    mock_redis_manager = MagicMock()
    mocker.patch('note_app.helpers.auth_functions.RedisManager', return_value=mock_redis_manager)
    mock_redis_manager.valid_session.return_value = False

    from note_app.helpers.auth_functions import remove_session
    
    res = remove_session('123')

    assert res == True

def test_is_valid_session_success(mocker):
    mock_redis_manager = MagicMock()
    mocker.patch('note_app.helpers.auth_functions.RedisManager', return_value=mock_redis_manager)
    mock_redis_manager.valid_session.return_value = True

    from note_app.helpers.auth_functions import remove_session

    res = remove_session('123')

    assert res == True

def test_is_valid_session_failure(mocker):
    mock_redis_manager = MagicMock()
    mocker.patch('note_app.helpers.auth_functions.RedisManager', return_value=mock_redis_manager)
    mock_redis_manager.valid_session.return_value = False

    from note_app.helpers.auth_functions import remove_session

    with pytest.raises(Exception):
        res = remove_session('123')
        assert res == False