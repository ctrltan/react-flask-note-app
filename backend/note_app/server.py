from flask import Flask, request
from note_app.helpers.decorators import db_connector
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from note_app.helpers.helper_utils import JWT_SECRET_KEY

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

@app.route('/', methods=['GET'])
def index():
    return { 'status': 200, 'message': 'hello world' }


if __name__ == "__main__":
    from note_app.routes.auth import auth
    from note_app.routes.notes import notes

    app.register_blueprint(notes)
    app.register_blueprint(auth)

    app.run(host="localhost", port=8000)