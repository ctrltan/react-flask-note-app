from note_app.helpers.redis_manager import RedisManager
import logging

cachingLogger = logging.getLogger('caching')

def add_note_hset(note_id: int, data: dict) -> bool:
    try:
        r_conn = RedisManager()
        note_key = f'note_{note_id}'

        data['shared'] = str(data['shared'])
        data['title'] = data['title'] or ''
        data['contents'] = data['contents'] or ''

        success = r_conn.add_hset(note_key, data)
        if not success:
            raise Exception('Could not add note')
        
        return True
    except Exception as ex:
        cachingLogger.exception(ex)
        return False
    
def get_note_hset(note_id: int) -> dict | None:
    try:
        r_conn = RedisManager()
        note_key = f'note_{note_id}'

        cached_note_data = r_conn.get_hset(note_key)
        if not cached_note_data:
            raise Exception('Could not retrieve data')
        
        str_to_bool = {'True': True, 'False': False}

        cached_note_data['note_id'] = int(cached_note_data['note_id'])
        cached_note_data['shared'] = str_to_bool[cached_note_data['shared']]

        return cached_note_data
    except Exception as ex:
        cachingLogger.exception(ex)
        return None
