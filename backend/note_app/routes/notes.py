from flask import Blueprint

notes = Blueprint('notes', __name__)

@notes.route('/<id>/new_note', methods=['POST'])
def addNote():
    pass

@notes.route('/<id>/notes/<id>', methods=['GET', 'POST'])
def getNote(id):
    pass

@notes.route('/<id>/notes', methods=['GET'])
def getAllNotes():
    pass

@notes.route('/<id>/notes/delete/<id>', methods=['DELETE'])
def deleteNote(id):
    pass