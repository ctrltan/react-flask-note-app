import pytest, pytest_pgsql
import psycopg2
from dotenv import load_dotenv
import os
from note_app.decorators import db_connector

load_dotenv(dotenv_path='/backend/.env')

@pytest.fixture
def test_db():
    conn = psycopg2.connect(database="postgres", host="localhost", user="postgres", password=os.environ['DB_PASSWORD'])
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS test (id serial PRIMARY KEY, title VARCHAR(50), contents VARCHAR(1000));''')
    conn.commit()

    yield cur

    cur.execute('''DROP TABLE IF EXISTS test''')
    conn.commit()
    cur.close()
    conn.close()

def test_db_connector():
    @db_connector("postgres")
    def some_route_function():
        cur.execute('''SELECT COUNT(*) FROM test''')
        (count,) = cur.fetchone()
        assert count == 1
    
    some_route_function()
    
    

    