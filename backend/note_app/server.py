from flask import Flask, request
from note_app.helpers.decorators import db_connector
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv
import logging

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=os.getenv('FLASK_APP_CLIENT_URL') or '*')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

load_dotenv('.env')

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

@app.route('/', methods=['GET'])
def index():
    return { 'status': 200, 'message': 'hello world' }

def create_app(testing=False):
    from note_app.routes.auth import auth
    from note_app.routes.notes import notes

    app.register_blueprint(notes)
    app.register_blueprint(auth)

    if testing == True:
        app.config['Testing'] = True
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="localhost", port=8000)