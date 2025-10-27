from flask import Flask, request
from note_app.decorators import db_connector
from routes.auth import auth
from routes.notes import notes
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

app.register_blueprint(notes)
app.register_blueprint(auth)

@app.route('/', methods=['GET'])
def index():
    return {"message": "hello world"}


if __name__ == "__main__":
    app.register_blueprint(notes)
    app.register_blueprint(auth)

    app.run(host="localhost", port=8000)