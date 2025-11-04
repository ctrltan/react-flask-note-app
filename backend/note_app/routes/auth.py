from flask import Blueprint, request, make_response
from note_app.decorators import db_connector
from note_app.helpers.auth_functions import email_validation
from note_app.server import bcrypt
import re

auth = Blueprint('auth', __name__)

PASSWORD_PATTERN = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"

@auth.route('/signup', methods=['POST'])
@db_connector()
def signup(cur=None):
    req_data = (request.get_json())['data']

    username = req_data['username']
    email = req_data['email']
    password = req_data['password']
    
    try:
        cur.execute('''SELECT * FROM users WHERE username=%s OR email=%s;''', (username, email))
        associated_usernames_emails = cur.fetchall()

        cur.execute('''SELECT password FROM users;''')
        all_passwords = cur.fetchall()

        password_match = re.fullmatch(PASSWORD_PATTERN, password)



        if associated_usernames_emails != None:
            raise Exception('Username or email already in use!')


        password_match = re.fullmatch(PASSWORD_PATTERN, password)

        if password_match == None:
            return Exception('Password not valid!')
        
        
        
        try:
            encrypted_password = bcrypt.generate_password_hash(password)
            cur.execute('''INSERT INTO users (username, email, password) VALUES (%s, %s, %s);''', (username, email, encrypted_password))

            cur.execute('''SELECT user_id FROM users WHERE username=%s AND email=%s;''', (username, email))
            user_id = cur.fetchone()[0]

            return { 'status': 200, 'message': {user_id, username} }
        except:
            raise Exception('Could not create this account. Try again later')

    except Exception as ex:
        return { 'status': 500, 'message': ex.args[0] }


@auth.route('/login', methods=['POST'])
@db_connector()
def login(cur=None):
    req_data = (request.get_json())['data']

    username = req_data['username']
    password = req_data['password']

    try:
        cur.execute('''SELECT * FROM users WHERE username=%s''', (username,))

        user = cur.fetchone()
        user_password = user[3] if user != None else None

        if user_password != password:
            raise Exception('Account does not exist')
        
        user_id = user[0]
        
        return { 'user_id': user_id, 'username': username }

    except Exception as ex:
        return { 'message': ex.args[0] }