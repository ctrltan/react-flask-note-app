from unittest.mock import MagicMock
from datetime import datetime, timezone
import pytest

@pytest.fixture
def client_note_data():
    iso_curr_date = datetime.isoformat(datetime.now(timezone.utc))
    test_note = {'note_id': 1, 'title': 'Test', 'contents': 'this is a test note', 'last_accessed': iso_curr_date, 'created_by': 'testuser', 'shared': False}

    return test_note

@pytest.fixture
def cached_note_data():
    iso_curr_date = datetime.isoformat(datetime.now(timezone.utc))
    test_note = {'note_id': 1, 'title': 'Test', 'contents': 'this is a test note', 'last_accessed': iso_curr_date, 'created_by': 'testuser', 'shared': 'False'}

    return test_note

def test_add_note_hset_success(client_note_data, mocker):
    mock_redis_manager = MagicMock()

    mock_redis_manager.add_hset.return_value = True
    mocker.patch('note_app.helpers.caching_functions.RedisManager', return_value=mock_redis_manager)

    from note_app.helpers.caching_functions import add_note_hset

    res = add_note_hset(1, client_note_data)

    assert res == True
    assert type(client_note_data['shared']) == str

def test_add_note_hset_failure(client_note_data, mocker):
    mock_redis_manager = MagicMock()

    mock_redis_manager.add_hset.return_value = False
    mocker.patch('note_app.helpers.caching_functions.RedisManager', return_value=mock_redis_manager)

    from note_app.helpers.caching_functions import add_note_hset

    res = add_note_hset(1, client_note_data)

    assert res == False

def test_add_note_hset_success_empty_contents_and_title(client_note_data, mocker):
    mock_redis_manager = MagicMock()

    mock_redis_manager.add_hset.return_value = True
    mocker.patch('note_app.helpers.caching_functions.RedisManager', return_value=mock_redis_manager)

    from note_app.helpers.caching_functions import add_note_hset

    client_note_data['title'] = None
    client_note_data['contents'] = None

    res = add_note_hset(1, client_note_data)

    assert res == True
    assert client_note_data['title'] == ''
    assert client_note_data['contents'] == ''

def test_get_note_hset_success(cached_note_data, mocker):
    mock_redis_manager = MagicMock()

    mock_redis_manager.get_hset.return_value = cached_note_data
    mocker.patch('note_app.helpers.caching_functions.RedisManager', return_value=mock_redis_manager)

    from note_app.helpers.caching_functions import get_note_hset

    res = get_note_hset(1)

    assert type(cached_note_data['shared']) == bool
    assert res['note_id'] == cached_note_data['note_id']
    assert res['title'] == cached_note_data['title']
    assert res['contents'] == cached_note_data['contents']
    assert res['last_accessed'] == cached_note_data['last_accessed']
    assert res['created_by'] == cached_note_data['created_by']

def test_get_note_hset_failure(mocker):
    mock_redis_manager = MagicMock()

    mock_redis_manager.get_hset.return_value = None
    mocker.patch('note_app.helpers.caching_functions.RedisManager', return_value=mock_redis_manager)

    from note_app.helpers.caching_functions import get_note_hset

    res = get_note_hset(1)

    assert res == None

def test_delete_note_hset_success(mocker):
    mock_redis_manager = MagicMock()

    mock_redis_manager.delete_hset.return_value = True
    mocker.patch('note_app.helpers.caching_functions.RedisManager', return_value=mock_redis_manager)

    from note_app.helpers.caching_functions import delete_note_hset

    res = delete_note_hset(1)

    assert res == True

def test_delete_note_hset_failure(mocker):
    mock_redis_manager = MagicMock()

    mock_redis_manager.delete_hset.return_value = False
    mocker.patch('note_app.helpers.caching_functions.RedisManager', return_value=mock_redis_manager)

    from note_app.helpers.caching_functions import delete_note_hset

    res = delete_note_hset(1)

    assert res == False