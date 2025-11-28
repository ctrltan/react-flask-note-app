from flask import Blueprint, request, make_response, jsonify
from note_app.helpers.decorators import db_connector
from note_app.helpers.auth_functions import token_decoder
from datetime import datetime, timezone
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
            notes[note_id] = {'title': note[1], 'contents': note[2], 'last_accessed': note[3].isoformat(), 'created_by': note[4], 'shared': note[5]}
        
        response = make_response(jsonify({'message': notes}))

        return response, 200
    except Exception as ex:
        noteLogger.exception(ex)
        return {'message': "Sorry! We couldn't get your notes at this time. Try this page later"}

@notes.route('/notes/new_note', methods=['GET'])
@db_connector()
def create_new_note(cur=None):
    access_token = request.cookies.get('access_token')
    payload = token_decoder(access_token)

    username = payload['username']

    try:
        last_accessed = datetime.now(timezone.utc)
        created_by = username

        cur.execute('''INSERT INTO notes (last_accessed, created_by) VALUES (%s, %s) RETURNING *;''', (last_accessed, created_by))
        raw_note = cur.fetchone()[0]

        note_id = raw_note[0]
        title = f'Note #{note_id}'
        contents = None

        note_data = {'note_id': note_id, 'title': title, 'contents': contents, 'created_by': created_by}

        response = make_response(jsonify({'message': note_data}))

        return response, 200
    except Exception as ex:
        noteLogger.exception(ex)
        return {'message': "Sorry! We couldn't create your note at this moment. Try again later"}

@notes.route('/notes/save', methods=['POST'])
@db_connector()
def save_note(cur=None):
    access_token = request.cookies.get('access_token')
    payload = token_decoder(access_token)

    user_id = payload['user_id']

    try:
        pass
    except Exception as ex:
        noteLogger.exception(ex)
        pass

@notes.route('/notes/<int:note_id>', methods=['GET', 'POST'])
@db_connector()
def get_note(id):
    pass
    
@notes.route('/notes/delete/<int:note_id>', methods=['DELETE'])
@db_connector()
def delete_note(id):
    pass