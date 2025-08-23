from flask import Flask, request
from decorators import db_connector


app = Flask(__name__)

@db_connector
@app.route('/')
def index():
    return "hello world"

@app.route('/new_note', methods=['POST'])
def addNote():
    pass

@app.route('/notes/<id>', methods=['GET', 'POST'])
def getNote(id):
    pass

@app.route('/notes', methods=['GET'])
def getAllNotes():
    pass

@app.route('/notes/delete/<id>', methods=['DELETE'])
def deleteNote(id):
    pass



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)