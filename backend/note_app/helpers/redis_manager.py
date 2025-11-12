import redis
from collections import deque
from datetime import datetime, timedelta
from note_app.helpers.helper_utils import REDIS_USER, REDIS_PASSWORD, REDIS_PORT


class RedisManager:

    connection_pool = deque()
    max_pool_size = 20

    def __init__(self):
        self.r = redis.Redis(
            host=f'redis-{REDIS_PORT}.crce204.eu-west-2-3.ec2.redns.redis-cloud.com',
            port=int(REDIS_PORT),
            decode_responses=True,
            username=REDIS_USER,
            password=REDIS_PASSWORD,
        )
    
    def add_session_key(self, session_id: str, user_id: str, refresh_token: str):
        try:
            self.r.hset(f'session_id:{session_id}', mapping={
                'user_id': user_id,
                'refresh_token': refresh_token
            })
            self.r.expire(f'session_id:{session_id}', time=timedelta(days=30))

        except Exception as ex:
            print('didnt work')
