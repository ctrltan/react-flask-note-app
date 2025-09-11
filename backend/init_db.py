from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

conn = psycopg2.connect(database="note_db", host="localhost", user="postgres", password=os.environ['DB_PASSWORD'])
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS notes (id serial PRIMARY KEY, contents VARCHAR(1000));''')

conn.commit()
cur.close()
conn.close()

