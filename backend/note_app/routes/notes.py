from flask import Blueprint

notes = Blueprint('notes', __name__)

@notes.route('/new_note', methods=['POST'])
def addNote():
    pass

@notes.route('/<int:note_id>', methods=['GET', 'POST'])
def getNote(id):
    pass

@notes.route('/', methods=['GET'])
def getAllNotes():
    pass

@notes.route('/delete/<int:note_id>', methods=['DELETE'])
def deleteNote(id):
    pass