from celery import shared_task, Celery
from note_app.server import app
from celery.exceptions import MaxRetriesExceededError
from note_app.helpers.decorators import db_connector
from datetime import datetime
from psycopg2.errors import OperationalError
from note_app.helpers.caching_functions import get_note_hset



@shared_task(bind=True)
@db_connector()
def save_retry(self, note_id: int, cur=None):
    try:
        print('attempting save...')
        note_data = get_note_hset(note_id)

        client_last_access = note_data['last_accessed']
        last_accessed = datetime.fromisoformat(client_last_access)

        cur.execute('''UPDATE notes SET title=%s, contents=%s, last_accessed=%s, shared=%s WHERE note_id=%s;''', (note_data['title'], note_data['contents'], last_accessed, note_data['shared'], note_data['note_id']))
    except MaxRetriesExceededError as ex:
        print('rescheduling...')
        save_retry.delay(note_id)
    except Exception as exc:
        print('retrying...')
        self.retry(exc=exc, countdown=60)

    


    

