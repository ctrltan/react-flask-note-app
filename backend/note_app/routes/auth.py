from flask import Blueprint, request, make_response, jsonify
from datetime import timedelta
from flask_cors import CORS
from note_app.helpers.decorators import db_connector
from note_app.helpers.auth_functions import email_encryption, token_creator, create_session, token_decoder, remove_session, is_valid_session
from note_app.server import bcrypt
from uuid import uuid4
import ulid
import re

auth = Blueprint('auth', __name__)

PASSWORD_PATTERN = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"

@auth.route('/signup', methods=['POST'])
@db_connector()
def signup(cur=None):
    req_data = request.get_json()

    username = req_data['username']
    email = req_data['email']
    password = req_data['password']
    
    try:
        cur.execute('''SELECT * FROM users WHERE username=%s OR email=%s;''', (username, email))
        associated_usernames_emails = cur.fetchall()

        password_match = re.fullmatch(PASSWORD_PATTERN, password)

        if associated_usernames_emails:
            raise Exception('Username or email already in use!')

        password_match = re.fullmatch(PASSWORD_PATTERN, password)

        if password_match == None:
            raise Exception('Invalid password')
        
        try:
            user_id = str(ulid.new())
            encrypted_password = bcrypt.generate_password_hash(password).decode('utf-8')
            encrypted_email = email_encryption(email)

            cur.execute('''INSERT INTO users (user_id, username, email, password) VALUES (%s, %s, %s, %s);''', (user_id, username, encrypted_email, encrypted_password))

            cur.execute('''SELECT user_id FROM users WHERE username=%s;''', (username,))
            user_id = cur.fetchone()[0]

            session_id = str(uuid4())
            refresh_token, access_token = token_creator({'session_id': session_id, 'user_id': user_id, 'username': username})
            
            create_session(session_id, user_id, refresh_token)

            response = make_response(jsonify({'message': { 'user_id': user_id, 'username': username }}))

            response.set_cookie('access_token', access_token, max_age=timedelta(minutes=15), httponly=True, samesite='None', secure=True, path='/')
            response.set_cookie('refresh_token', refresh_token, max_age=timedelta(days=30), httponly=True, samesite='None', secure=True, path='/')

            return response, 200
        except Exception as e:
            print(e)
            raise Exception('Could not create this account. Try again later')

    except Exception as ex:
        return { 'status': 500, 'message': ex.args[0] }


@auth.route('/login', methods=['POST'])
@db_connector()
def login(cur=None):
    req_data = request.get_json()

    username = req_data['username']
    password = req_data['password']

    try:
        cur.execute('''SELECT * FROM users WHERE username=%s;''', (username,))

        user = cur.fetchone()
        user_password = user[3] if user != None else None

        if user_password == None:
            raise Exception('Account does not exist')
        
        password_match = bcrypt.check_password_hash(user_password, password)

        if not password_match:
            raise Exception('Incorrect credentials')
        
        user_id = user[0]
        
        session_id = str(uuid4())
        refresh_token, access_token = token_creator({'session_id': session_id, 'user_id': user_id, 'username': username})
            
        create_session(session_id, user_id, refresh_token)

        response = make_response(jsonify({'message': { 'user_id': user_id, 'username': username }}))

        response.set_cookie('access_token', access_token, max_age=timedelta(minutes=15), httponly=True, samesite='None', secure=True, path='/')
        response.set_cookie('refresh_token', refresh_token, max_age=timedelta(days=30), httponly=True, samesite='None', secure=True, path='/')

        return response, 200

    except Exception as ex:
        return { 'message': ex.args[0] }
    

@auth.route('/logout', methods=['POST'])
def logout():
    access_token = request.cookies.get('access_token')
    try:
        token_payload = token_decoder(access_token)

        remove_session(token_payload['session_id'])

        response = make_response()
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response, 200
    except Exception as ex:
        print(ex)
        return { 'message': 'Could not log you out at this time' }
    

@auth.route('/auth/refresh', methods=['POST'])
def refresh():
    refresh_token = request.cookies.get('refresh_token')
    req_data = request.get_json()

    user_id = req_data['user_id']
    username = req_data['username']

    try:
        if not refresh_token:
            raise Exception('Invalid refresh token')
        
        token_payload = token_decoder(refresh_token)
        session_id = token_payload['sub']

        valid_session = is_valid_session(session_id)

        if not valid_session:
            raise Exception('Session ended')

        refresh, access_token = token_creator({ 'user_id': user_id, 'session_id': session_id, 'username': username })

        response = make_response()
        response.set_cookie('access_token', access_token, max_age=timedelta(minutes=15), httponly=True, samesite='None', secure=True, path='/')

        return response, 200
    except Exception as ex:
        return { 'message': ex.args[0] }, 401
    