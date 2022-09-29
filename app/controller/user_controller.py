from flask import jsonify, request, current_app
from app.controller.token_required_controller import token_required
from app.exc.exc import NonAuthenticated, SessionExpired
from app.model.user_model import User
from sqlalchemy.exc import InvalidRequestError, DataError, ProgrammingError, IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
from psycopg2.errors import UniqueViolation, NotNullViolation, InvalidTextRepresentation
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from os import environ

def get_all_users():
    users = User.query.all()

    return jsonify(users)

def get_user_by_id(user_id: str):
    try:
        user = User.query.filter_by(id = user_id).first()

        if not user:
            return {"msg": "Usuário não encontrado"}, 404

        return jsonify(user)
    except DataError as err:
        if isinstance(err.orig, InvalidTextRepresentation):
            return {"msg": "Usuário não encontrado"}, 404

def delete_user(user_id: str):
    try:
        user = User.query.get(user_id)

        current_app.db.session.delete(user)
        current_app.db.session.commit()

        return jsonify(user), 201
    
    except UnmappedInstanceError:
        return {"msg": "Usuário não encontrado"}, 404


def update_user_info(user_id: str):
    try:
        token_required()

        new_data = request.json
        User.query.filter_by(id=user_id).update(new_data)

        current_app.db.session.commit()

        updated_user = User.query.get(user_id)

        return jsonify(updated_user)

    except InvalidRequestError:
        return {"msg": "Chave(s) inválida(s) na requisição"}, 400
    except DataError:
        return {"msg": "Tipo de dado inválido"}, 400
    except ProgrammingError:
        return {"msg": "Chave(s) faltando na requisição"}, 400
    except IntegrityError as err:
        if isinstance(err.orig, UniqueViolation):
            return {"msg": "Nome ou e-mail já cadastrados"}, 403
    except NonAuthenticated as err:
        return {"msg": "Precisa estar logado"}, 401
    except SessionExpired as err:
        return {"msg": "Sessão expirada"}, 400

def create_user():
    try:
        new_user_data = request.json
        invalid_keys = set(new_user_data.keys()) - User.infos
        
        if invalid_keys:
            raise(InvalidRequestError)

        # Check if there already is a user with that name
        existing_user = User.query.filter_by(name=new_user_data['name']).first()
        if existing_user:
            raise UniqueViolation 

        # Check if there already is a user with that email
        existing_user = User.query.filter_by(email=new_user_data['email']).first()
        if existing_user:
            raise UniqueViolation

        new_user_data['password'] = generate_password_hash(new_user_data['password'])

        new_user = User(**new_user_data)

        session = current_app.db.session
        session.add(new_user)
        session.commit()

        new_user_created = User.query.filter_by(email=new_user.email).first()

        return jsonify(new_user_created)
    except IntegrityError as err:
        if isinstance(err.orig, NotNullViolation):
            return {"msg": "Faltando nome, email ou senha"}, 400
    except InvalidRequestError as err:
        return {"msg": "Chave(s) inválida(s) na requisição"}, 400
    except UniqueViolation as err:
        return {"msg": "Nome ou email já cadastrados"}, 400


def login_user():
    login_data = request.json

    user_found = User.query.filter_by(email=login_data['email']).first()

    if not user_found:
        return {"msg": "Email ou senha inválidos"}, 400

    password_match = check_password_hash(user_found.password, login_data['password'])

    if password_match:
        token = jwt.encode({
            "user_id": str(user_found.id),
            "expiration": str(datetime.utcnow() + timedelta(hours = 2))
        }, environ.get('SECRET_KEY'))

        return jsonify({"token": token.decode('utf-8')}) 

    else:
        return {"msg": "Email ou senha inválidos"}, 400