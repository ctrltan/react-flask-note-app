from unittest.mock import MagicMock
from datetime import datetime, timezone
from psycopg2.errors import OperationalError
import pytest

@pytest.fixture
def client_note_data():
    iso_curr_date = datetime.isoformat(datetime.now(timezone.utc))
    test_note = {'note_id': 1, 'title': 'Test', 'contents': 'this is a test note', 'last_accessed': iso_curr_date, 'created_by': 'testuser', 'shared': False}

    return test_note

@pytest.fixture
def raw_note_data():
    curr_date = datetime.now(timezone.utc)
    test_note = {'note_id': 1, 'title': 'Test', 'contents': 'this is a test note', 'last_accessed': curr_date, 'created_by': 'testuser', 'shared': False}

    return test_note

def test_before_request_valid(authenticated_client, mocker):
    mock_cursor = MagicMock()
    mock_redis_manager = MagicMock()

    mock_cursor.fetchall_return_value = []

    mocker.patch('note_app.helpers.decorators.psycopg2.connect').return_value.cursor.return_value = mock_cursor
    mocker.patch('note_app.helpers.caching_functions.RedisManager', return_value=mock_redis_manager)
    
    response = authenticated_client.get('/notes')

    assert response.status_code == 200
    assert response.json['message'] == {}

def test_before_request_valid_with_options(authenticated_client, client_note_data, mocker):
    mock_redis_manager = MagicMock()

    mocker.patch('note_app.helpers.caching_functions.RedisManager', return_value=mock_redis_manager)

    response = authenticated_client.open('/notes/auto-save', json=client_note_data, method='OPTIONS')

    assert response.status_code == 200
    assert 'POST' in response.headers['Allow']
    assert 'OPTIONS' in response.headers['Allow']

def test_before_request_invalid_without_tokens(client, mocker):
    mock_cursor = MagicMock()
    mock_redis_manager = MagicMock()

    mock_cursor.fetchall_return_value = []

    mocker.patch('note_app.helpers.decorators.psycopg2.connect').return_value.cursor.return_value = mock_cursor
    mocker.patch('note_app.helpers.caching_functions.RedisManager', return_value=mock_redis_manager)

    response = client.get('/notes')

    assert response.status_code == 401
    assert response.json['message'] == 'Invalid access token'

def test_before_request_valid_with_options_without_tokens(client, client_note_data, mocker):
    mock_redis_manager = MagicMock()

    mocker.patch('note_app.helpers.caching_functions.RedisManager', return_value=mock_redis_manager)

    response = client.open('/notes/auto-save', json=client_note_data, method='OPTIONS')

    assert response.status_code == 200
    assert 'POST' in response.headers['Allow']
    assert 'OPTIONS' in response.headers['Allow']

def test_get_all_notes_success_cache_miss(authenticated_client, raw_note_data, mocker):
    mock_cursor = MagicMock()
    mock_redis_manager = MagicMock()

    mock_cursor.fetchall.side_effect = [[(1,)], [tuple(raw_note_data.values())]]
    mock_redis_manager.get_hset.return_value = None
    
    mocker.patch('note_app.helpers.decorators.psycopg2.connect').return_value.cursor.return_value = mock_cursor
    mocker.patch('note_app.helpers.caching_functions.RedisManager', return_value=mock_redis_manager)

    response = authenticated_client.get('/notes')

    raw_note_data['last_accessed'] = datetime.isoformat(raw_note_data['last_accessed'])
    id_string = str(raw_note_data['note_id'])
    del raw_note_data['note_id']

    assert response.status_code == 200
    assert id_string in response.json['message'].keys()
    assert response.json['message'][id_string] == raw_note_data

def test_get_all_notes_success_cache_hit(authenticated_client, client_note_data, mocker):
    mock_cursor = MagicMock()
    mock_redis_manager = MagicMock()

    mock_cursor.fetchall.side_effect = [[(1,)], []]

    client_note_data['shared'] = str(client_note_data['shared'])
    mock_redis_manager.get_hset.return_value = client_note_data
    
    mocker.patch('note_app.helpers.decorators.psycopg2.connect').return_value.cursor.return_value = mock_cursor
    mocker.patch('note_app.helpers.caching_functions.RedisManager', return_value=mock_redis_manager)

    response = authenticated_client.get('/notes')

    id_string = str(client_note_data['note_id'])

    assert response.status_code == 200
    assert id_string in response.json['message']
    assert response.json['message'][id_string] == client_note_data

def test_get_all_notes_success_no_notes(authenticated_client, mocker):
    mock_cursor = MagicMock()
    mock_redis_manager = MagicMock()

    mock_cursor.fetchall.side_effect = [[], []]
    mock_redis_manager.get_hset.return_value = None
    
    mocker.patch('note_app.helpers.decorators.psycopg2.connect').return_value.cursor.return_value = mock_cursor
    mocker.patch('note_app.helpers.caching_functions.RedisManager', return_value=mock_redis_manager)

    response = authenticated_client.get('/notes')

    assert response.status_code == 200
    assert response.json['message'] == {}

def test_get_all_notes_failure_incomplete_data(authenticated_client, raw_note_data, mocker):
    mock_cursor = MagicMock()
    mock_redis_manager = MagicMock()

    raw_note_data['shared']

    mock_cursor.fetchall.side_effect = [[(1,)], [tuple(raw_note_data.values())]]
    mock_redis_manager.get_hset.return_value = None
    
    mocker.patch('note_app.helpers.decorators.psycopg2.connect').return_value.cursor.return_value = mock_cursor
    mocker.patch('note_app.helpers.caching_functions.RedisManager', return_value=mock_redis_manager)

    response = authenticated_client.get('/notes')

    with pytest.raises(Exception):
        assert response.status_code == 200
        assert response.json['message'] == "Sorry! We couldn't get your notes at this time. Try this page later"

def test_create_new_note_success(authenticated_client, raw_note_data, mocker):
    mock_cursor = MagicMock()

    raw_note_data['title'] = 'Untitled'
    mock_cursor.fetchone.return_value = tuple(raw_note_data.values())

    mocker.patch('note_app.helpers.decorators.psycopg2.connect').return_value.cursor.return_value = mock_cursor

    response = authenticated_client.get('/notes/new-note')

    assert response.status_code == 200
    assert response.json['message'] == {'note_id': raw_note_data['note_id'], 'title': raw_note_data['title']}

def test_create_new_note_failure_could_not_connect(authenticated_client, mocker):
    mock_cursor = MagicMock()

    mock_cursor.execute.return_value = OperationalError

    response = authenticated_client.get('/notes/new_note')

    with pytest.raises(Exception):
        assert response.status_code == 200
        assert response.json['message'] == "Sorry! We couldn't create your note at this moment. Try again later"

def test_get_note_success_cache_hit(authenticated_client, client_note_data, mocker):
    mock_cursor = MagicMock()
    mock_redis_manager = MagicMock()

    raw_bool = client_note_data['shared']
    client_note_data['shared'] = str(client_note_data['shared'])
    mock_redis_manager.get_hset.return_value = client_note_data

    mocker.patch('note_app.helpers.decorators.psycopg2.connect').return_value.cursor.return_value = mock_cursor
    mocker.patch('note_app.helpers.caching_functions.RedisManager', return_value=mock_redis_manager)

    response = authenticated_client.get('/notes/get-note?note_id=1')

    client_note_data['shared'] = raw_bool

    assert response.status_code == 200
    assert response.json['message'] == client_note_data

def test_get_note_success_cache_miss(authenticated_client, raw_note_data, mocker):
    mock_cursor = MagicMock()
    mock_redis_manager = MagicMock()

    mock_cursor.fetchone.return_value = tuple(raw_note_data.values())
    mock_redis_manager.get_hset.return_value = None

    mocker.patch('note_app.routes.notes.add_note_hset', return_value=True)
    mocker.patch('note_app.helpers.decorators.psycopg2.connect').return_value.cursor.return_value = mock_cursor
    mocker.patch('note_app.helpers.caching_functions.RedisManager', return_value=mock_redis_manager)

    response = authenticated_client.get('/notes/get-note?note_id=1')

    raw_note_data['last_accessed'] = datetime.isoformat(raw_note_data['last_accessed'])

    assert response.status_code == 200
    assert response.json['message'] == raw_note_data

def test_get_note_database_failure_cache_miss(authenticated_client, mocker):
    mock_cursor = MagicMock()
    mock_redis_manager = MagicMock()

    mock_cursor.execute.return_value = OperationalError
    mock_redis_manager.get_hset.return_value = None

    mocker.patch('note_app.helpers.decorators.psycopg2.connect').return_value.cursor.return_value = mock_cursor
    mocker.patch('note_app.helpers.caching_functions.RedisManager', return_value=mock_redis_manager)

    response = authenticated_client.get('/notes/get-note?note_id=1')

    assert response.status_code == 200
    assert response.json['message'] ==  "Sorry! We couldn't get that note"

def test_auto_save_success(authenticated_client, client_note_data, mocker):
    mock_redis_manager = MagicMock()

    mock_redis_manager.add_hset.return_value = True
    mocker.patch('note_app.routes.notes.add_note_hset', return_value=True)
    mocker.patch('note_app.helpers.caching_functions.RedisManager', return_value=mock_redis_manager)

    response = authenticated_client.post('/notes/auto-save', json=client_note_data)

    assert response.status_code == 200
    assert response.json['message'] == 'saved'

def test_auto_save_failure(authenticated_client, client_note_data, mocker):
    mock_redis_manager = MagicMock()

    mock_redis_manager.add_hset.return_value = False
    mocker.patch('note_app.routes.notes.add_note_hset', return_value=False)
    mocker.patch('note_app.helpers.caching_functions.RedisManager', return_value=mock_redis_manager)

    response = authenticated_client.post('/notes/auto-save', json=client_note_data)

    with pytest.raises(Exception):
        assert response.status_code == 500
        assert response.json['message'] == 'Offline'

def test_save_success(authenticated_client, client_note_data, mocker):
    mock_cursor = MagicMock()
    mock_redis_manager = MagicMock()

    mock_redis_manager.add_hset.return_value = True
    mocker.patch('note_app.routes.notes.add_note_hset', return_value=True)

    mocker.patch('note_app.helpers.decorators.psycopg2.connect').return_value.cursor.return_value = mock_cursor
    mocker.patch('note_app.helpers.caching_functions.RedisManager', return_value=mock_redis_manager)

    response = authenticated_client.post('/notes/save', json=client_note_data)

    assert response.status_code == 200
    assert response.json['message'] == 'Your note was saved!'

def test_save_caching_failure(authenticated_client, client_note_data, mocker):
    mock_redis_manager = MagicMock()

    mock_redis_manager.add_hset.return_value = False
    mocker.patch('note_app.routes.notes.add_note_hset', return_value=False)
    mocker.patch('note_app.helpers.caching_functions.RedisManager', return_value=mock_redis_manager)

    response = authenticated_client.post('/notes/save', json=client_note_data)

    assert response.status_code == 500
    assert response.json['message'] == "Your note could not be saved"

def test_save_database_failure(authenticated_client, client_note_data, mocker):
    mock_cursor = MagicMock()
    mock_redis_manager = MagicMock()

    mock_cursor.execute.return_value = OperationalError
    mock_redis_manager.add_hset.return_value = True
    mocker.patch('note_app.routes.notes.add_note_hset', return_value=True)

    mocker.patch('note_app.helpers.decorators.psycopg2.connect').return_value.cursor.return_value = mock_cursor
    mocker.patch('note_app.helpers.caching_functions.RedisManager', return_value=mock_redis_manager)

    response = authenticated_client.post('/notes/save', json=client_note_data)

    with pytest.raises(Exception):
        assert response.status_code == 500
        assert response.json['message'] == "We'll try again"

def test_delete_success(authenticated_client, mocker):
    mock_cursor = MagicMock()
    mock_redis_manager = MagicMock()

    mock_redis_manager.delete_hset.return_value = True
    mock_cursor.fetchone.return_value = (True,)

    mocker.patch('note_app.routes.notes.delete_note_hset', return_value=True)

    mocker.patch('note_app.helpers.decorators.psycopg2.connect').return_value.cursor.return_value = mock_cursor
    mocker.patch('note_app.helpers.caching_functions.RedisManager', return_value=mock_redis_manager)

    response = authenticated_client.delete('/notes/delete?note_id=1')

    assert response.status_code == 200
    assert response.json['message'] == 'Note deleted'

def test_delete_success_shared_note(authenticated_client, mocker):
    mock_cursor = MagicMock()
    mock_redis_manager = MagicMock()

    mock_cursor.fetchone.return_value = (False,)

    mocker.patch('note_app.helpers.decorators.psycopg2.connect').return_value.cursor.return_value = mock_cursor
    mocker.patch('note_app.helpers.caching_functions.RedisManager', return_value=mock_redis_manager)

    response = authenticated_client.delete('/notes/delete?note_id=1')

    assert response.status_code == 200
    assert response.json['message'] == 'Note deleted'

def test_delete_database_failure(authenticated_client, mocker):
    mock_cursor = MagicMock()
    mock_redis_manager = MagicMock()

    mock_cursor.execute.return_value = OperationalError

    mocker.patch('note_app.helpers.decorators.psycopg2.connect').return_value.cursor.return_value = mock_cursor
    mocker.patch('note_app.helpers.caching_functions.RedisManager', return_value=mock_redis_manager)

    response = authenticated_client.delete('/notes/delete?note_id=1')

    with pytest.raises(Exception):
        assert response.status_code == 500
        assert response.json['message'] == 'Could not delete this note'

    

