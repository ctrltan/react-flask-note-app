from flask import Blueprint, request, make_response, jsonify
from note_app.helpers.decorators import db_connector
from note_app.helpers.auth_functions import token_decoder
from datetime import datetime, timezone
from psycopg2.errors import OperationalError
import logging

notes = Blueprint('notes', __name__)

noteLogger = logging.getLogger('notes')

@notes.before_request
def check_tokens():
    access_token = request.cookies.get('access_token')
    payload = token_decoder(access_token)

    if not payload:
        return { 'message': 'Invalid access token' }, 401

@notes.route('/notes', methods=['GET'])
@db_connector()
def get_all_notes(cur=None):
    access_token = request.cookies.get('access_token')
    payload = token_decoder(access_token)

    user_id = payload['user_id']

    try:
        cur.execute('''SELECT * FROM notes WHERE note_id IN (SELECT note_id FROM note_owners WHERE user_id=%s) ORDER BY last_accessed DESC;''', (user_id,))
        raw_notes = cur.fetchall()

        notes = {}
        for note in raw_notes:
            note_id = note[0]
            print(note[1])
            notes[note_id] = {'title': note[1], 'contents': note[2], 'last_accessed': datetime.isoformat(note[3]), 'created_by': note[4], 'shared': note[5]}
        
        response = make_response(jsonify({'message': notes}))

        return response, 200
    except Exception as ex:
        noteLogger.exception(ex)
        return {'message': "Sorry! We couldn't get your notes at this time. Try this page later"}

@notes.route('/notes/new-note', methods=['GET'])
@db_connector()
def create_new_note(cur=None):
    access_token = request.cookies.get('access_token')
    payload = token_decoder(access_token)

    user_id = payload['user_id']
    username = payload['username']

    try:
        last_accessed = datetime.now(timezone.utc)
        created_by = username
        title = 'Untitled'

        cur.execute('''INSERT INTO notes (title, last_accessed, created_by) VALUES (%s, %s, %s) RETURNING note_id;''', (title, last_accessed, created_by))
        raw_note = cur.fetchone()

        note_id = raw_note[0]

        cur.execute('''INSERT INTO note_owners (user_id, note_id) VALUES (%s, %s);''', (user_id, note_id))

        note_data = {'note_id': note_id, 'title': title}

        response = make_response(jsonify({'message': note_data}))

        return response, 200
    except Exception as ex:
        noteLogger.exception(ex)
        return {'message': "Sorry! We couldn't create your note at this moment. Try again later"}

@notes.route('/notes/get-note', methods=['GET', 'POST'])
@db_connector()
def get_note(cur=None):
    access_token = request.cookies.get('access_token')
    payload = token_decoder(access_token)

    user_id = payload['user_id']
    note_id = request.args.get('note_id', type=int)
    
    try:
        cur.execute('''SELECT note_id, title, contents, created_by FROM notes WHERE note_id=%s and note_id IN (SELECT note_id FROM note_owners WHERE user_id=%s);''', (note_id, user_id))
        raw_note = cur.fetchone()

        note_id = raw_note[0]
        title = raw_note[1]
        contents = raw_note[2]
        created_by = raw_note[3]

        note_data = {'note_id': note_id, 'title': title, 'contents': contents, 'created_by': created_by}

        response = make_response(jsonify({'message': note_data}))

        return response, 200
    except Exception as ex:
        noteLogger.exception(ex)
        return {'message': "Sorry! We couldn't get that note"}

@notes.route('/notes/save', methods=['POST'])
@db_connector()
def save_note(cur=None):
    access_token = request.cookies.get('access_token')
    payload = token_decoder(access_token)

    user_id = payload['user_id']

    note_data = request.get_json()

    try:
        client_last_access = note_data['last_accessed']
        last_accessed = datetime.fromisoformat(client_last_access)

        cur.execute('''UPDATE notes SET title=%s, contents=%s, last_accessed=%s, shared=%s WHERE note_id=%s;''', (note_data['title'], note_data['contents'], last_accessed, note_data['shared'], note_data['note_id']))

        '''
        put database in try except block which does retry if no success then do the retry
        if user tries to exit page without retry then prompt save
        '''
    except OperationalError as ex:
        noteLogger.exception(ex)
        '''
        Trigger retry by pushing the note_id to the redis queue under the user's id (should be managed across sessions for one user)
        '''
        return 
    except Exception as ex:
        noteLogger.exception(ex)
        return {'message': "your note could not be saved"}, 500
    
@notes.route('/notes/delete', methods=['DELETE'])
@db_connector()
def delete_note(cur=None):
    pass