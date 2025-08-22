import psycopg2
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='/backend/.env')

def db_connector(f):
    def wrapper(*args, **kwargs):
        conn = psycopg2.connect(database="note_db", host="localhost", user="postgres", password=os.environ['DB_PASSWORD'])
        cur = conn.cursor()

        try:
            res = f(cur, *args, **kwargs)
        except:
            conn.rollback()
        else:
            conn.commit()
        finally:
            conn.close()
        
        return res
    return wrapper