import psycopg2
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='..env')

def db_connector(database_name="note_db"):
    def decorator(f):
        def wrapper(*args, **kwargs):
            conn = psycopg2.connect(database=database_name, host="localhost", user="postgres", password=os.getenv('POSTGRES_PASSWORD'))
            cur = conn.cursor()

            try:
                res = f(cur=cur, *args, **kwargs)
            except:
                conn.rollback()
                print("Could not perform action")
                raise
            else:
                conn.commit()
            finally:
                cur.close()
                conn.close()
            
            return res
        return wrapper
    return decorator