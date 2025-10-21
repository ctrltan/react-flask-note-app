from flask import Flask, request, jsonify
from note_app.decorators import db_connector
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "hello world"})

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
    app.run(host="localhost", port=8000)