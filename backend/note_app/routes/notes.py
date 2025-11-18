from flask import Blueprint, request
from note_app.helpers.decorators import db_connector
from note_app.helpers.auth_functions import token_decoder

notes = Blueprint('notes', __name__)

@notes.before_request
def check_tokens():
    access_token = request.cookies.get('access_token')
    payload = token_decoder(access_token)

    if not payload:
        return { 'message': 'Invalid access token' }, 401

@notes.route('/notes/new_note', methods=['POST'])
def addNote():
    pass

@notes.route('/notes/<int:note_id>', methods=['GET', 'POST'])
def getNote(id):
    pass

@notes.route('/notes', methods=['GET'])
@db_connector()
def getAllNotes():
    pass
    

@notes.route('/notes/delete/<int:note_id>', methods=['DELETE'])
def deleteNote(id):
    pass