from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from flask_jwt_extended import create_refresh_token, create_access_token, decode_token
from note_app.helpers.redis_manager import RedisManager
from datetime import timedelta
import base64
from note_app.helpers.helper_utils import AES_ENCRYPTION_KEY, AES_INITIALISATION_VECTOR

def email_validation(email):
    pass

def email_encryption(email: str) -> str:
    key = bytes.fromhex(AES_ENCRYPTION_KEY)
    iv = bytes.fromhex(AES_INITIALISATION_VECTOR)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    byte_email = pad(email.encode('utf-8'), cipher.block_size)
    encrypted_email = cipher.encrypt(byte_email)

    encrypted_email = base64.b64encode(encrypted_email).decode('utf-8')

    return encrypted_email

def token_creator(payload: dict) -> tuple[str, str]:
    access_claims = {'user_id': payload['user_id'], 'session_id': payload['session_id'], 'username': payload['username']}
    
    access_token = create_access_token(payload['user_id'], expires_delta=timedelta(minutes=15), additional_claims=access_claims)
    refresh_token = create_refresh_token(payload['session_id'], expires_delta=False)

    return refresh_token, access_token

def token_decoder(token: str) -> dict | None:
    try:
        payload = decode_token(token, allow_expired=True)
        
        return payload
    except:
        return None

def create_session(session_id: str, user_id: str, refresh_token: str) -> bool:
    try:
        r_conn = RedisManager()
        r_conn.add_session_key(session_id, user_id, refresh_token)

        return True
    except Exception as ex:
        print(ex)
        return False


def remove_session(session_id: str) -> bool:
    try:
        r_conn = RedisManager()
        session_data = r_conn.valid_session(session_id)

        if not session_data:
            return True
        
        r_conn.delete_session(session_id)

        return True
    except Exception as ex:
        print(ex)
        return False
    
def is_valid_session(session_id: str) -> bool:
    try:
        r_conn = RedisManager()
        valid = r_conn.valid_session(session_id)

        if not valid:
            raise Exception('Invalid session')
        
        return True
    except Exception as ex:
        print(ex)
        return False