from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

conn = psycopg2.connect(database=os.environ['POSTGRES_DBNAME'], host=os.environ['POSTGRES_HOST'], user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'])
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS users (user_id serial PRIMARY KEY, username VARCHAR(15), password VARCHAR(50));''')
cur.execute('''CREATE TABLE IF NOT EXISTS notes (note_id serial PRIMARY KEY, title VARCHAR(50), contents VARCHAR(1000), user_id INT);''')
cur.execute('''ALTER TABLE notes ADD CONSTRAINT user_id FOREIGN KEY (user_id) REFERENCES users(user_id);''')

conn.commit()
cur.close()
conn.close()

