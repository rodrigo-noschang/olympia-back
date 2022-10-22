from flask import request
import jwt
from os import environ
from datetime import datetime
from app.exc.exc import NonAuthenticated, SessionExpired

def token_required():
    token = request.headers.get('Authorization').split(' ')[1]
    
    try:    
        decoded_token = jwt.decode(token, environ.get('SECRET_KEY'), algorithms=['HS256'])
        expiration_time_string = decoded_token.get('expiration')
        expiration_time = datetime.strptime(expiration_time_string, "%Y-%m-%d %H:%M:%S.%f")
        current_time = datetime.utcnow()

        if current_time > expiration_time:
            raise SessionExpired

        return decoded_token
    except jwt.exceptions.DecodeError as err:
        raise NonAuthenticated