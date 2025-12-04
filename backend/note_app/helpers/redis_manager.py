import redis
from redis.cache import CacheConfig
from collections import deque
from datetime import datetime, timedelta
from note_app.helpers.helper_utils import REDIS_USER, REDIS_PASSWORD, REDIS_PORT
import logging

redisLogger = logging.getLogger('redis manager')

def start_redis_pool():
    return redis.ConnectionPool(
                host=f'redis-{REDIS_PORT}.crce204.eu-west-2-3.ec2.redns.redis-cloud.com',
                port=int(REDIS_PORT),
                decode_responses=True,
                username=REDIS_USER,
                password=REDIS_PASSWORD,
            )

class RedisManager:

    pool = start_redis_pool()

    def __init__(self):
        self.r = redis.Redis(connection_pool=RedisManager.pool)

    def add_hset(self, key: str, value: dict) -> bool:
        try:
            expiryRequired = True
            occurrences = self.r.exists(key)
            if occurrences == 1:
                expiryRequired = False
            
            self.r.hset(key, mapping=value)
            if expiryRequired:
                self.r.expire(key, time=timedelta(days=10))
            return True
        except Exception as ex:
            redisLogger.exception(ex)
            return False
        
    def get_hset(self, key: str) -> dict | None:
        try:
            mapping = self.r.hgetall(key)
            return mapping
        except Exception as ex:
            redisLogger.exception(ex)
            return None

    def add_session_key(self, session_id: str, user_id: str, refresh_token: str):
        try:
            self.r.hset(f'session_id:{session_id}', mapping={
                'user_id': user_id,
                'refresh_token': refresh_token
            })
            self.r.expire(f'session_id:{session_id}', time=timedelta(days=30))
        except Exception as ex:
            redisLogger.exception(ex)
    
    def get_session(self, session_id: str) -> dict | None:
        try:
            occurrences = self.r.exists(f'session_id:{session_id}')
            if occurrences == 0:
                return None
        
            return self.r.hkeys(f'session_id:{session_id}')
        except Exception as ex:
            redisLogger.exception(ex)
            return None
    
    def valid_session(self, session_id: str) -> bool:
        try:
            occurrences = self.r.exists(f'session_id:{session_id}')
            if occurrences == 0:
                return False
            
            return True
        except Exception as ex:
            redisLogger.exception(ex)
            return False


    def delete_session(self, session_id: str):
        try:
            self.r.expire(f'session_id:{session_id}', -1)
            return True
        except Exception as ex:
            redisLogger.exception(ex)
            return False
