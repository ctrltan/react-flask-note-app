import pytest
from unittest.mock import MagicMock
from note_app.server import bcrypt

def test_signup_success(client, mocker):
    mock_cursor = MagicMock()
    mock_redis_manager = MagicMock()

    mock_cursor.fetchone.return_value = (1, 'janedoe', 'Janepassword1!', 'janedoe@email.com')
    mock_cursor.fetchall.return_value = ()

    mocker.patch('note_app.helpers.decorators.psycopg2.connect').return_value.cursor.return_value = mock_cursor
    mocker.patch('note_app.helpers.auth_functions.RedisManager', return_value=mock_redis_manager)

    response = client.post('/signup', json={'username': 'janedoe', 'password': 'Janepassword1!', 'email': 'janedoe@email.com'})

    assert response.status_code == 200
    assert response.json['message'] == {'user_id': 1, 'username': 'janedoe'}
    assert 'Set-Cookie' in response.headers

def test_signup_account_exists(client, mocker):
    mock_cursor = MagicMock()
    mock_redis_manager = MagicMock()

    mock_cursor.fetchone.return_value = (1, 'janedoe', 'Janepassword1!', 'janedoe@email.com')
    mock_cursor.fetchall.return_value = (1, 'janedoe', 'Janepassword1!', 'janedoe@email.com')

    mocker.patch('note_app.helpers.decorators.psycopg2.connect').return_value.cursor.return_value = mock_cursor
    mocker.patch('note_app.helpers.auth_functions.RedisManager', return_value=mock_redis_manager)

    response = client.post('/signup', json={'username': 'janedoe', 'password': 'Janepassword1!', 'email': 'janedoe@email.com'})

    assert response.json['status'] == 500
    assert response.json['message'] == 'Username or email already in use!'

def test_signup_password_invalid(client, mocker):
    mock_cursor = MagicMock()
    mock_redis_manager = MagicMock()

    mock_cursor.fetchone.return_value = (1, 'janedoe', 'Janepassword1!', 'janedoe@email.com')
    mock_cursor.fetchall.return_value = ()

    mocker.patch('note_app.helpers.decorators.psycopg2.connect').return_value.cursor.return_value = mock_cursor
    mocker.patch('note_app.helpers.auth_functions.RedisManager', return_value=mock_redis_manager)

    response = client.post('/signup', json={'username': 'janedoe', 'password': 'Janepassword1', 'email': 'janedoe@email.com'})

    assert response.json['status'] == 500
    assert response.json['message'] == 'Invalid password'

def test_signup_user_id_not_found(client, mocker):
    mock_cursor = MagicMock()
    mock_redis_manager = MagicMock()

    mock_cursor.fetchone.return_value = ()
    mock_cursor.fetchall.return_value = ()

    mocker.patch('note_app.helpers.decorators.psycopg2.connect').return_value.cursor.return_value = mock_cursor
    mocker.patch('note_app.helpers.auth_functions.RedisManager', return_value=mock_redis_manager)

    response = client.post('/signup', json={'username': 'janedoe', 'password': 'Janepassword1!', 'email': 'janedoe@email.com'})

    assert response.json['status'] == 500
    assert response.json['message'] == 'Could not create this account. Try again later'


def test_login_success(client, mocker):
    mock_cursor = MagicMock()
    mock_redis_manager = MagicMock()
    
    encrypted_password = bcrypt.generate_password_hash('Janepassword1!').decode('utf-8')

    mock_cursor.fetchone.return_value = (1, 'janedoe', 'janedoe@email.com', encrypted_password)

    mocker.patch('note_app.helpers.decorators.psycopg2.connect').return_value.cursor.return_value = mock_cursor
    mocker.patch('note_app.helpers.auth_functions.RedisManager', return_value=mock_redis_manager)

    response = client.post('/login', json={'username': 'janedoe', 'password': 'Janepassword1!'})

    assert response.status_code == 200
    assert response.json['message'] == {'user_id': 1, 'username': 'janedoe'}
    assert 'Set-Cookie' in response.headers

def test_login_user_does_not_exist(client, mocker):
    mock_cursor = MagicMock()
    mock_redis_manager = MagicMock()
    
    mock_cursor.fetchone.return_value = None

    mocker.patch('note_app.helpers.decorators.psycopg2.connect').return_value.cursor.return_value = mock_cursor
    mocker.patch('note_app.helpers.auth_functions.RedisManager', return_value=mock_redis_manager)

    response = client.post('/login', json={'username': 'janedoe', 'password': 'Janepassword1!'})

    assert response.json['message'] == 'Account does not exist'

def test_login_password_does_not_match(client, mocker):
    mock_cursor = MagicMock()
    mock_redis_manager = MagicMock()
    
    encrypted_password = bcrypt.generate_password_hash('Janepassword1!').decode('utf-8')

    mock_cursor.fetchone.return_value = (1, 'janedoe', 'janedoe@email.com', encrypted_password)

    mocker.patch('note_app.helpers.decorators.psycopg2.connect').return_value.cursor.return_value = mock_cursor
    mocker.patch('note_app.helpers.auth_functions.RedisManager', return_value=mock_redis_manager)

    response = client.post('/login', json={'username': 'janedoe', 'password': 'Janepassword2!'})

    assert response.json['message'] == 'Incorrect credentials'

def test_logout_success(client, mocker, cookies):
    mock_redis_manager = MagicMock()
    mocker.patch('note_app.helpers.auth_functions.RedisManager', return_value=mock_redis_manager)

    client.set_cookie('access_token', cookies[0])
    client.set_cookie('refresh_token', cookies[1])

    response = client.post('/logout')

    assert response.status_code == 200
    assert 'Set-Cookie' not in response.headers
    assert 'access_token' not in client._cookies
    assert 'refresh_token' not in client._cookies

def test_refresh_success(client, mocker, cookies):
    mock_redis_manager = MagicMock()
    mocker.patch('note_app.helpers.auth_functions.RedisManager', return_value=mock_redis_manager)

    client.set_cookie('refresh_token', cookies[1])

    response = client.post('/auth/refresh', json={'user_id': 1, 'username': 'janedoe'})
    
    assert response.status_code == 200
    assert 'Set-Cookie' in response.headers
    assert 'access_token' in response.headers['Set-Cookie']

def test_refresh_no_token_failure(client, mocker):
    mock_redis_manager = MagicMock()
    mocker.patch('note_app.helpers.auth_functions.RedisManager', return_value=mock_redis_manager)

    client.delete_cookie('refresh_token')

    response = client.post('/auth/refresh', json={'user_id': 1, 'username': 'janedoe'})
    
    assert response.status_code == 401
    assert response.json['message'] == 'Invalid refresh token'
    assert 'Set-Cookie' not in response.headers
    

