from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

conn = psycopg2.connect(database=os.environ['POSTGRES_DBNAME'], host=os.environ['POSTGRES_HOST'], user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'])
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS users (user_id VARCHAR(36) PRIMARY KEY, username VARCHAR(15) NOT NULL UNIQUE, email VARCHAR(300) NOT NULL UNIQUE, password VARCHAR(80) NOT NULL UNIQUE);''')
cur.execute('''CREATE TABLE IF NOT EXISTS notes (note_id serial PRIMARY KEY, title VARCHAR(240), contents TEXT, last_accessed TIMESTAMPTZ NOT NULL, created_by VARCHAR(36) REFERENCES users(username) ON UPDATE CASCADE ON DELETE CASCADE, shared BOOLEAN NOT NULL DEFAULT false);''')
cur.execute('''CREATE TABLE IF NOT EXISTS note_owners (note_id INT REFERENCES notes(note_id), user_id VARCHAR(36) REFERENCES users(user_id), CONSTRAINT note_owners_pkey PRIMARY KEY (user_id, note_id));''')

conn.commit()
cur.close()
conn.close()

