from flask import Blueprint

notes = Blueprint('notes', __name__)

@notes.route('/<user_id>/new_note', methods=['POST'])
def addNote():
    pass

@notes.route('/<user_id>/notes/<note_id>', methods=['GET', 'POST'])
def getNote(id):
    pass

@notes.route('/<user_id>/notes', methods=['GET'])
def getAllNotes():
    pass

@notes.route('/<user_id>/notes/delete/<note_id>', methods=['DELETE'])
def deleteNote(id):
    pass