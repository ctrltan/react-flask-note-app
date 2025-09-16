import pytest
import psycopg2
from dotenv import load_dotenv
import os
from note_app.decorators import db_connector

@pytest.fixture
def db():
    conn = psycopg2.connect(database="postgres", host="localhost", user="postgres", password=os.getenv('POSTGRES_PASSWORD'))
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS test (id serial PRIMARY KEY, title VARCHAR(50), contents VARCHAR(1000));''')
    conn.commit()
    cur.execute('''INSERT INTO test (title, contents) VALUES ('My First Note', 'This note is for testing');''')
    conn.commit()

    yield

    cur.execute('''DROP TABLE IF EXISTS test;''')
    conn.commit()
    cur.close()
    conn.close()

def test_db_connector(db):
    @db_connector("postgres")
    def some_route_function(cur=None):
        cur.execute('''SELECT COUNT(*) FROM public.test;''')
        (count,) = cur.fetchone()
        assert count == 1
    
    some_route_function()
    
    

    