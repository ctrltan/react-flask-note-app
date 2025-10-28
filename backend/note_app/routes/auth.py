from flask import Blueprint, request

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    return { 'message': 'hello' }